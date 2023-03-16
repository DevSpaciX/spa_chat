import re
from django.core.files import File
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

def validate_html_tag(value):
    allowed_tags = ["a", "code", "i", "strong"]
    pattern = re.compile(r'<(/)?\w+[^>]*>')

    # Escape HTML tags that are not allowed
    value = re.escape(value)

    # Validate allowed HTML tags and check for closing tags
    match = pattern.search(value)
    if match:
        tag, closing = match.group(0), match.group(1)
        if tag[1:-1] not in allowed_tags:
            raise ValidationError(f"Invalid HTML tag: {tag}")
        elif closing:
            if tag[1:-1] not in allowed_tags:
                raise ValidationError(f"Invalid HTML tag: {tag}")
        elif value.count(f"<{tag[1:-1]}>") != value.count(f"</{tag[1:-1]}>"):
            raise ValidationError(f"Unclosed HTML tag: {tag}")


class Room(models.Model):
    title = models.CharField(max_length=255)
    main_message = models.TextField(default="hi")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        validate_html_tag(self.main_message)

    def save(self, *args, **kwargs):
        self.clean()
        super(Room, self).save(*args, **kwargs)



class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="user_messages", on_delete=models.CASCADE)
    email = models.EmailField()
    image = models.FileField(blank=True,null=True)
    text = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_added",)

    def clean(self):
        validate_html_tag(self.text)


    def save(self, *args, **kwargs):
        self.clean()
        super(Message, self).save(*args, **kwargs)