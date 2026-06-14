from .base import *
from decouple import config

# حتماً این خطوط بالا باشند تا مقدار پیش‌فرض بیس رو بازنویسی کنند:
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '::1']

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}