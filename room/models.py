from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.db import models

from room.validators import validate_html_tag


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



class BaseModel(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    email = models.EmailField()
    image = models.FileField(blank=True, null=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("date_added",)

    def clean(self):
        validate_html_tag(self.text)

    def save(self, *args, **kwargs):
        self.clean()
        super(BaseModel, self).save(*args, **kwargs)


class Message(BaseModel):
    answers = models.ManyToManyField("Answer", related_name="messages")


class Answer(BaseModel):
    pass