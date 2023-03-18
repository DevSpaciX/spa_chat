
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("user/", include("user.urls", namespace="user")),
    path("", include("room.urls", namespace="room")),
    path("admin/site", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
