from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from api.user.decorators import sensitive_post_parameters_m
from api.user.serializers import SignInSerializer, UserCreateSerializer
from rest_framework.exceptions import ValidationError, NotFound
from api.utils.otp import generate_random_otp_code
from api.utils.required import validate_required_fields
from api.utils.response import CustomResponse
from apps.ecom.models import CustomerProfile
from apps.mailersend_utils import send_mailersend_email
from apps.user.models import CustomUser, Otp
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={"errors": serializer.errors},
            )

        try:
            user = serializer.save()

            # create otp for user
            otp_code = generate_random_otp_code()
            Otp.objects.create(user=user, otp=otp_code)

            # send otp to user email
            email = user.email
            to_list = [email]
            subject = "SignUp OTP Verification"
            body = f"Hello {getattr(user, 'name', '')},\n\nYour OTP code is: {otp_code}\nPlease use this code to verify your email address."
            result = send_mailersend_email(to_list, subject, body)

            signup_data = {
                "user_id": user.id,
                "user_name": getattr(user, "name", ""),
                "email": user.email,
                "is_active": user.is_active,
                "requires_otp": True,
            }
            return CustomResponse.successfully_created(
                data=signup_data,
                message="User created successfully, please validate your email by entering the OTP sent to your email",
                status_code=201,
            )
        except Exception as e:
            return CustomResponse.error(
                message="User creation failed",
                status_code=400,
                extra_fields={"errors": {"message": [str(e)]}},
            )


class OtpVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get("otp")
        email = request.data.get("email")

        if not otp_code or not email:
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={
                    "errors": {
                        **({"otp": ["This field is required."]} if not otp_code else {}),
                        **({"email": ["This field is required."]} if not email else {}),
                    }
                },
            )

        try:
            otp = Otp.objects.get(otp=otp_code, user__email=email)

            # actiavte user
            otp.user.is_active = True
            otp.user.save()

            # create token for user
            token, created = Token.objects.get_or_create(user=otp.user)

            name = otp.user.name
            # delete otp
            otp.delete()
            return CustomResponse.success(
                data={"token": token.key, "user_name": name},
                message="OTP verified successfully",
            )
        except Otp.DoesNotExist:
            return CustomResponse.error(
                message="Invalid OTP",
                status_code=400,
                extra_fields={"errors": {"message": ["Invalid or expired OTP."]}},
            )
        except Exception as e:
            return CustomResponse.error(
                message="OTP verification failed",
                status_code=500,
                extra_fields={"errors": {"message": [str(e)]}},
            )


class UserSignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)

        if not serializer.is_valid():
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={"errors": serializer.errors},
            )

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        try:
            user = CustomUser.objects.get(email=email, is_active=True)
            photo = user.profile.photo.url if user.profile.photo else None
            name = user.profile.first_name if user.profile else ""
            last_name = user.profile.last_name if user.profile else ""
            full_name = str(name).strip() + str(last_name).strip()

            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                user_name = user.name
                return CustomResponse.success(
                    data={
                        "token": token.key,
                        "user_name": user_name,
                        "full_name": full_name,
                        "email": user.email,
                        "photo": photo
                    },
                    message="User signed in successfully"
                )
            else:
                return CustomResponse.error(
                    message="Invalid password",
                    status_code=401,
                    extra_fields={"errors": {"password": ["Invalid credentials."]}},
                )

        except CustomUser.DoesNotExist:
            return CustomResponse.error(
                message="User does not exist",
                status_code=404,
                extra_fields={"errors": {"message": ["No active account found with the given credentials."]}},
            )

        except Exception as e:
            return CustomResponse.error(
                message="An error occurred",
                status_code=500,
                extra_fields={"errors": {"message": [str(e)]}},
            )


from rest_framework import generics, status
from rest_framework import serializers


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'phone', 'photo']
        extra_kwargs = {
            'photo': {'required': False}
        }


class UpdateUserInfoAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        if CustomerProfile.objects.filter(user=self.request.user).exists():
            return self.request.user.profile
        else:
            profile = CustomerProfile.objects.create(user=self.request.user)
            return profile


from django.contrib.auth.forms import SetPasswordForm
from django.conf import settings


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        self.old_password_field_enabled = getattr(
            settings, 'OLD_PASSWORD_FIELD_ENABLED', True
        )
        self.logout_on_password_change = getattr(
            settings, 'LOGOUT_ON_PASSWORD_CHANGE', False
        )
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

        if not self.old_password_field_enabled:
            self.fields.pop('old_password')

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError('Invalid password')
        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(self.request, self.user)
        else:
            self.user.auth_token.delete()


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # unified validation error shape
        if not serializer.is_valid():
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={"errors": serializer.errors},
            )
        serializer.save()
        return CustomResponse.success(message="New password has been saved.")


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={"errors": serializer.errors},
            )
        email = serializer.validated_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            return CustomResponse.error(
                message="User not found",
                status_code=404,
                extra_fields={"errors": {"message": ["No user found with this email."]}},
            )

        user = CustomUser.objects.get(email=email)
        otp_code = generate_random_otp_code()
        Otp.objects.create(user=user, otp=otp_code)
        # send otp to user email
        # send otp to user email
        email = user.email
        to_list = [email]
        subject = "Password Reset OTP Verification"
        body = f"Hello {getattr(user, 'name', '')},\n\nYour OTP code is: {otp_code}\nPlease use this code to verify your email address."
        result = send_mailersend_email(to_list, subject, body)

        return CustomResponse.success(
            message="OTP sent successfully",
            status_code=200,
        )


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128)
    email = serializers.EmailField()

    class Meta:
        model = Otp
        fields = ('email', 'otp', 'password')


class PasswordResetConfirmView(APIView):
    authentication_classes = ()
    permission_classes = ()
    queryset = Otp.objects.all()
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        otp = request.data.get("otp")
        email = request.data.get("email")
        password = request.data.get("password")

        # basic required-field validation
        missing = {}
        if not email:
            missing["email"] = ["This field is required."]
        if not otp:
            missing["otp"] = ["This field is required."]
        if not password:
            missing["password"] = ["This field is required."]
        if missing:
            return CustomResponse.error(
                message="Validation error",
                status_code=400,
                extra_fields={"errors": missing},
            )

        otp_obj = Otp.objects.filter(otp=otp, user__email=email).last()

        if otp_obj:
            try:
                user = otp_obj.user
                user.set_password(password)
                user.save()
                otp_obj.delete()
            except CustomUser.DoesNotExist:
                return CustomResponse.error(
                    message="User not exists",
                    status_code=404,
                    extra_fields={"errors": {"message": ["User not exists"]}},
                )
            return CustomResponse.success(
                message="Password has been reset with the new password."
            )

        return CustomResponse.error(
            message="Invalid OTP",
            status_code=400,
            extra_fields={"errors": {"message": ["Invalid or expired OTP."]}},
        )
