
import os
from pathlib import Path
import socket

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-x&-+o6xae!b1oe^%9zr37+ob_is=g@qrhxbf@=j7jdxt6n_5mt"

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0","127.0.0.1"]

INTERNAL_IPS = [
    "127.0.0.1",
]



INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "room",
    "channels",
    "django_filters",
    "captcha",
    "debug_toolbar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "spa_chat.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spa_chat.wsgi.application"
ASGI_APPLICATION = "spa_chat.asgi.application"



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "cache:11211",
    }
}



CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_URL = "redis://redis:6379"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
AUTH_USER_MODEL = "user.User"
LOGOUT_REDIRECT_URL = "user:homepage"
LOGIN_URL = "/login/"
RECAPTCHA_PUBLIC_KEY = "6Lcwn_okAAAAAO8vyB9D3_ORDwgbFiyj7AoRfTMi"
RECAPTCHA_PRIVATE_KEY = "6Lcwn_okAAAAAIn-w0DtJZop1QP4e5ndeJ9LQwDY"
