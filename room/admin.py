from django.contrib import admin

from room.models import Room, Message

admin.site.register(Room)
admin.site.register(Message)