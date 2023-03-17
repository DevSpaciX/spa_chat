from celery import shared_task
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Room, Message, Answer
import os
from django.core.files import File
from django.conf import settings


@shared_task
def save_message_task(username, room_id, message, file_path, answer_to):
    user = get_user_model().objects.get(username=username)
    room = Room.objects.get(pk=room_id)
    create_message_or_answer(user, room, message, file_path, answer_to)

@shared_task
def create_message_or_answer(user, room, message, file_path, answer_to=None):
    model = Answer if answer_to else Message
    kwargs = {'user': user, 'room': room, 'text': message, 'email': user.email}
    if file_path:
        with open(file_path, 'rb') as file:
            created_obj = model.objects.create(**kwargs)
            created_obj.image.save(os.path.basename(file_path), File(file))
            if answer_to:
                parent_message = Message.objects.get(pk=answer_to)
                parent_message.answers.add(created_obj)
                parent_message.save()
    elif answer_to:
        answer = model.objects.create(**kwargs)
        parent_message = Message.objects.get(pk=answer_to)
        parent_message.answers.add(answer)
    else:
        model.objects.create(**kwargs)