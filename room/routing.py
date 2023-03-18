from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/<int:roomID>/", consumers.ChatConsumer.as_asgi()),
]
