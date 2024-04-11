from decouple import config
from .base import *

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '*'
]

CSRF_TRUSTED_ORIGINS = ['https://web-production-baa4.up.railway.app']