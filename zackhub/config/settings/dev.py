from .base import *

DEBUG = True

SECRET_KEY = 'abc'

ALLOWED_HOSTS = ['*'] 

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
