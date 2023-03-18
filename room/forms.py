from captcha.fields import ReCaptchaField
from django import forms
from .models import Room


class RoomCreateForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Room
        fields = ["title", "main_message"]

