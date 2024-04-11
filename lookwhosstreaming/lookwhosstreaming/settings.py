import os
import django_heroku
import dj_database_url
import dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(__file__)

# Local Environment Variable Initialization

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
print(f"SETTING DEBUG MODE TO {DEBUG}")

ALLOWED_HOSTS = [
    'lookwhosstreaming.herokuapp.com',
    'www.lookwhosstreaming.com',
    'lookwhosstreaming.com',
    '127.0.0.1',
    'localhost',
]

# Application definition
PLATFORMS = [
    'YouTube',
    'Instagram',
    'Twitch',
    'Twitter'
]

INSTALLED_APPS = [
    'base',
    'storages',
    'streams',
    'tinymce', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lookwhosstreaming.urls'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'streams:admin'
LOGOUT_REDIRECT_URL = 'streams:home'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['lookwhosstreaming/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': ['django.templatetags.static'],
            'libraries' : {
                'handler' : 'streams.handler'
            }
        },
    },
]

WSGI_APPLICATION = 'lookwhosstreaming.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


# Local Settings

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS S3 Settings

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
# AWS_DOMAIN_NAME = f'http://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# AWS_LOCATION = 'static'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = AWS_DOMAIN_NAME + '/static/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "lookwhosstreaming/media/")
# MEDIA_URL = '/media/'


# Heroku Settings
try:
    django_heroku.settings(locals())
    del DATABASES['default']['OPTIONS']['sslmode']
    
    # Database
    # https://docs.djangoproject.com/en/3.0/ref/settings/#databases

    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=False)
    
except:  # if not deployed on heroku
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'project'),
        'USER': os.getenv('DATABASE_USER', 'project'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'fakepassword'),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        }
    }

# Tiny MCE Settings

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "menubar": False,
    "plugins": 'lists, link, anchor',
    "toolbar": 'undo redo | formatselect | '
    'bold italic underline link anchor backcolor | alignleft aligncenter '
    'alignright alignjustify | bullist numlist outdent indent | '
    'removeformat | help',
}

# Celery Configuration
# http://docs.celeryproject.org/en/4.4.1/userguide/configuration.html

REDIS_URL = os.environ.get('REDIS_URL', 'amqp://lookwhosstreaming:terminator@localhost/lookwhosstreaming')
CELERY_BROKER_URL = REDIS_URL
# CELERY_RESULT_BACKEND = REDIS_URL.replace('amqp', 'rpc')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE
CELERY_IMPORTS = ("broadcasts.monitor", "broadcasts.alert", "lookwhosstreaming.celery")  # "django_celery_site.tasks",
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 10 - 20
CELERY_TASK_TIME_LIMIT = 60 * 10
 
# Django Logging

LOGGING = {
    'version': 1, 
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': ' {asctime:>23} {funcName:<20} [{levelname:<9}    ] : {message}',
            'style': '{',
        },
        'monitor_format': {
            'format': ' {asctime:>23} broadcasts.{funcName:<18} [{levelname:<9}    ] : {message}',
            'style': '{',
        },
            
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'django-core': {
            'level': 'DEBUG', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB) 
            'filename': 'logs/django-core.log',
            'formatter': 'default'
        },
        'django-uploads': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB) 
            'filename': 'logs/user-uploads.log',
            'formatter': 'default'
        },
        'instagram': {
            'level': 'DEBUG', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB)  
            'filename': 'logs/broadcasts/instagram.log',
            'formatter': 'monitor_format'
        },
        'youtube': {
            'level': 'DEBUG', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB)  
            'filename': 'logs/broadcasts/youtube.log',
            'formatter': 'monitor_format'
        },
        'twitch': {
            'level': 'DEBUG', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB)  
            'filename': 'logs/broadcasts/twitch.log',
            'formatter': 'monitor_format'
        },
        'broadcasts': {
            'level': 'INFO', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB)  
            'filename': 'logs/broadcasts/all-platforms.log',
            'formatter': 'monitor_format'
        },
        'broadcasts-errors': {
            'level': 'WARNING', 
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10, 
            'maxBytes': 5242880, # (5MB)  
            'filename': 'logs/broadcasts/errors.log',
            'formatter': 'monitor_format'
        }
    },
    
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console',  'django-core'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'uploads' : {
            'handler' : ['django-uploads'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'broadcasts': {
            'handlers': ['broadcasts', 'broadcasts-errors'],
            'level': 'INFO',
        },
        'broadcasts.instagram': {
            'handlers': ['instagram'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'broadcasts.youtube': {
            'handlers': ['youtube'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'broadcasts.twitch': {
            'handlers': ['twitch'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
