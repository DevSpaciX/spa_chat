from django.contrib import admin

from room.models import Room, Message, Answer

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Answer)