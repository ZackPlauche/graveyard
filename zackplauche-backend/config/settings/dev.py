from .base import *

SECRET_KEY = 'django-insecure-%7yc@n-liy272*k!o#15r$(pw=q+uh18f^69rvm3l_5a&25usb'

DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

STATIC_URL = 'static/'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'
