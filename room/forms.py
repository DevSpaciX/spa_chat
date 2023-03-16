from captcha.fields import ReCaptchaField
from django import forms
from django.core.exceptions import ValidationError

from .models import Room, Message


class RoomCreateForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Room
        fields = ["title","main_message"]

class MessageForm(forms.Form):
    text = forms.CharField()
    file = forms.FileField(required=False)
    captcha = ReCaptchaField()

