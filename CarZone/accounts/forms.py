from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

UserModel = get_user_model()


class CarZoneUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CarZoneUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm password'})

    error_messages = {
        'password_too_short': 'Password too short!',
        'password_mismatch': 'Passwords do not match!',
        'duplicate_username': 'Username already taken!',
        'password_too_common': 'This password is too common!',
        'password_entirely_numeric': 'Password cannot be entirely numeric!'
    }

    class Meta:
        model = UserModel
        fields: tuple = ('username', 'password1', 'password2')


class CarZoneAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CarZoneAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})

    error_messages = {
        'invalid_login': 'Invalid credentials!'
    }

    class Meta:
        model = UserModel
        fields = ('username', 'password')
