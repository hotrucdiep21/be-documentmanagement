# developement.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.User'
# SQLite đơn giản cho dev
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

CORS_ALLOW_ALL_ORIGINS = True  # Cho phép tất cả origins trong dev
