from django.contrib.auth.forms import UserCreationForm

from user.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "username", "image", "password1", "password2"]