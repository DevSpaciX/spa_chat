import json
import os
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.files import File

from channels.generic.websocket import AsyncWebsocketConsumer

from room.validators import validate_file
from spa_chat import settings
from room.models import Room, Message, Answer
from room.validators import my_websocket_handler


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomid = self.scope["url_route"]["kwargs"]["roomID"]
        self.room_group_name = "chat_%s" % self.roomid

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, data):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        errors = []
        data = json.loads(text_data)

        message_text = data["message"]
        username = data["username"]
        room = data["room"]
        avatar = data["userImage"]
        answer_to = data["answer_to"]
        file_path = file_path_socket = None

        if data.get("file"):
            file_name = data["file"]["name"]
            file_content = data["file"]["content"]

            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            file_path_socket = os.path.join(settings.MEDIA_URL, file_name)
            with open(file_path, "wb") as file:
                file.write(bytes(file_content))

            file_errors = validate_file(file_path)
            errors.extend(file_errors)

        websocket_errors = my_websocket_handler(message_text)
        errors.extend(websocket_errors)

        if errors:
            await self.send_error(errors)
            return

        await self.save_message(username, room, message_text, file_path, answer_to)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "username": username,
                "avatar": avatar,
                "file": file_path_socket,
                "answer": answer_to,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        avatar = event["avatar"]
        file = event["file"]
        answer = event["answer"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "avatar": avatar,
                    "file": file,
                    "answer": answer,
                }
            )
        )

    @sync_to_async
    def save_message(self, username, room, message, file_path, answer_to):
        user = get_user_model().objects.get(username=username)
        room = Room.objects.get(pk=room)
        self.create_message_or_answer(user, room, message, file_path, answer_to)

    @staticmethod
    def create_message_or_answer(user, room, message, file_path, answer_to=None):
        model = Answer if answer_to else Message
        kwargs = {"user": user, "room": room, "text": message, "email": user.email}
        if file_path:
            with open(file_path, "rb") as file:
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

    async def send_error(self, errors):
        await self.send(
            text_data=json.dumps({"error": errors}),
        )
