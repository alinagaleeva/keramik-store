import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.timezone import now

from .models import EmailVerification, User


class UsersLoginFrom(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'login__input', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login__input', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'login__input',
            'placeholder': 'Confirm password'
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=24)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        return user
