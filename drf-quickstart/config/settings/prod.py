from .base import *

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False

ALLOWED_HOSTS = [
    'www.mysite.com',
]

CORS_ALLOWED_ORIGINS = [
    'https://www.mysite.com',
]


