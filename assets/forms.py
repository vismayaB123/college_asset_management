from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings

class SystemAdminRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary border-end-0', 'id': 'id_password'}), required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary border-end-0', 'id': 'id_password_confirm'}), required=True, label="Confirm Password")
    admin_registration_code = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg bg-body-tertiary border-end-0', 'id': 'id_admin_code'}), required=True, label="Administrator Registration Code")

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            raise ValidationError("An account with this username already exists.")
        return username

    def clean_admin_registration_code(self):
        code = self.cleaned_data.get('admin_registration_code')
        if code != settings.ADMIN_REGISTRATION_CODE:
            raise ValidationError("Invalid administrator registration code.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                self.add_error('password_confirm', "Passwords do not match.")
            else:
                try:
                    validate_password(password, self.instance)
                except ValidationError as e:
                    self.add_error('password', e)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class ApprovalAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        user = self.get_user()
        if user is not None:
            status = user.profile.account_status
            if status == 'PENDING':
                raise ValidationError('Your account is awaiting administrator approval. Please contact the system administrator.')
            elif status == 'REJECTED':
                raise ValidationError('Your administrator registration request was not approved. Please contact the system administrator for more information.')
            elif status == 'DISABLED':
                raise ValidationError('Your account has been disabled. Please contact the system administrator.')
        return cleaned_data
