from django import forms
from django.contrib.auth.models import Group, Permission
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm, SignupForm
from django.contrib.auth.hashers import make_password
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Field
from django.contrib.auth import get_user_model

from .models import CustomUser, CustomerUser,StaffUser
from crispy_forms.layout import Layout, Row, Column, HTML, Submit


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')



class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['placeholder'] = self.fields[fieldname].label
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('login', placeholder='Mobile No', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column('password', placeholder='Password', css_class='form-group col-md-12 mb-0'),
            ),
            Row(
                Column(
                    HTML('<label class="checkbox"><input type="checkbox" checked="checked" name="remember">'
                         '<span></span> &nbsp;Remember Me</label>'),
                    css_class='form-group text-left col-md-6 mb-5'),
                Column(
                    HTML('<a href="{}" class="kt-link kt-login__link-forgot">Forgot Password ?</a>'.format(
                        reverse_lazy('account_reset_password'))), css_class='text-right col-md-6 mb-5'
                ),
            ),
            Row(
                Column(
                    Submit('submit', 'Submit'), css_class='kt-login__actions'
                )
            )
        )





class GroupPermissionForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Select Group")


class StaffUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = StaffUser
        fields = ('name', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['email'].disabled = True
            self.fields['password'].required = False
            self.fields['password'].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'email', 'password',),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary', onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        # Only hash password if provided
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        elif self.instance and self.instance.pk:
            # Keep the existing password if no new password is provided
            user.password = self.instance.password
        if commit:
            user.save()
        return user


class StaffUserFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-2 mb-0'),
              

                Column(HTML("""<button class='btn btn-sm btn-primary'>Filter</button>"""),
                       css_class='form-group col-md-2 p-2 mb-0 mt-7'),
            ),
        )



class CustomerUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomerUser
        fields = ('name', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Disable email and hide password field if editing an existing instance
        if self.instance and self.instance.pk:
            self.fields['email'].disabled = True  # Disable the email field in edit mode
            self.fields['password'].required = False
            self.fields['password'].widget = forms.HiddenInput()
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', 'email', 'password',),
            ),
            Row(
                Column(
                    Submit('submit', 'Save', css_class='btn btn-primary', onclick="return confirm('Are you sure you want to submit?');")
                ),
            )
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        # Only hash password if provided
        if self.cleaned_data['password']:
            user.password = make_password(self.cleaned_data['password'])
        elif self.instance and self.instance.pk:
            # Keep the existing password if no new password is provided
            user.password = self.instance.password
        if commit:
            user.save()
        return user
