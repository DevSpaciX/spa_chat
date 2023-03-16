from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from spa_chat import settings

urlpatterns = [
    path("user/", include("user.urls",namespace="user")),
    path("", include("room.urls",namespace="room")),
    path("admin/site", admin.site.urls),
]

