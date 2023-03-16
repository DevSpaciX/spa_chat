from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.frontpage, name="homepage"),
    path("signup/", views.signup, name="signup"),
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "user"