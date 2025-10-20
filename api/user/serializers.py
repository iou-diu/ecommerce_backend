from django.core.validators import FileExtensionValidator

from apps.ecom.models import CustomerProfile
from rest_framework import serializers
from django.db import transaction
from apps.user.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)
    photo = serializers.FileField(validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'name', 'phone', 'photo')
        extra_kwargs = {'password': {'write_only': True}}

    @transaction.atomic
    def create(self, validated_data):

        phone = validated_data.pop('phone')
        photo = validated_data.pop('photo', None)

        user = CustomUser(
            email=validated_data['email'],
            is_active=False,
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()

        name_parts = validated_data['name'].split()

        if len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = ''
        else:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])

        CustomerProfile.objects.create(
            user=user,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            photo=photo if photo else None
        )

        return user


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
