from .base import *

SECRET_KEY = 'abc'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Staticfiles Dirs

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'
