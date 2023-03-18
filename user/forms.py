from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "image", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
