import json
import os
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.files.storage import default_storage

from room.models import validate_html_tag
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from spa_chat import settings
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.roomid = self.scope["url_route"]["kwargs"]["roomID"]
        self.room_group_name = "chat_%s" % self.roomid

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, data):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        errors = []
        data = json.loads(text_data)
        message_text = data["message"]
        username = data["username"]
        room = data["room"]
        avatar = data["userImage"]
        file_path = file_path_socket = None

        if data.get("file"):
            file_name = data['file']['name']
            file_content = data['file']['content']

            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            file_path_socket = os.path.join(settings.MEDIA_URL, file_name)
            print(file_path_socket)
            with open(file_path, 'wb') as file:
                file.write(bytes(file_content))

            file_errors = self.validate_file(file_path)
            errors.extend(file_errors)

        # вызываем первую функцию и добавляем ее ошибки в список errors
        websocket_errors = self.my_websocket_handler(message_text)
        errors.extend(websocket_errors)

        # если есть ошибки, отправляем их клиенту
        if errors:
            await self.send_error(errors)
            return

        await self.save_message(username, room, message_text, file_path)

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message_text, "username": username, "avatar": avatar,
             "file": file_path_socket},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        avatar = event["avatar"]
        file = event["file"]

        await self.send(
            text_data=json.dumps({"message": message, "username": username, "avatar": avatar, "file": file})
        )

    @sync_to_async
    def save_message(self, username, room, message, file_path):
        user = get_user_model().objects.get(username=username)
        room = Room.objects.get(pk=room)
        if file_path:
            with open(file_path, 'rb') as file:
                message = Message.objects.create(user=user, room=room, text=message, email=user.email)
                print(os.path.basename(file_path))
                message.image.save(os.path.basename(file_path), File(file))
                message.save()
        else:
            Message.objects.create(user=user, room=room, text=message, email=user.email)

    async def send_error(self, errors):
        await self.send(
            text_data=json.dumps({"error": errors}),
        )

    @staticmethod
    def my_websocket_handler(message):
        errors = []
        try:
            validate_html_tag(message)
        except ValidationError as e:
            errors.append(e.message)
        return errors

    @staticmethod
    def validate_file(file_path):
        errors = []
        max_image_size = (320, 240)
        max_file_size = 100 * 1024  # 100 KB
        allowed_image_formats = ['.jpg', '.jpeg', '.gif', '.png']
        allowed_text_formats = ['.txt']
        print(file_path)

        file_ext = os.path.splitext(file_path)[-1].lower()

        if file_ext in allowed_image_formats:
            with Image.open(file_path) as img:
                if img.size[0] > max_image_size[0] or img.size[1] > max_image_size[1]:
                    img.thumbnail(max_image_size)
                    img.save(file_path)

        elif file_ext in allowed_text_formats:
            if os.path.getsize(file_path) > max_file_size:
                errors.append("Text file size too large.")

        else:
            errors.append("File format not allowed.")

        return errors
