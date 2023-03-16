from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import ChatRoomsList, RoomCreateView

urlpatterns = [
    path("", ChatRoomsList.as_view(), name="rooms"),
    path("<int:pk>/",views.room, name="room"),
    path('room/create/', RoomCreateView.as_view(), name='room_create'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "room"