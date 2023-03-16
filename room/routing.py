from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    path("ws/<int:roomID>/", consumers.ChatConsumer.as_asgi()),
]
