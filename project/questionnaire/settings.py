import os
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent
# create necessary dirs and files
folders_to_create = ['logs/celery', 'logs/django', 'logs/postgre',
                     'media', 'staticfiles', 'questionnaireapp/migrations',
                     'Users/migrations', 'postgres_data']

for folder in folders_to_create:
    path_f = os.path.join(BASE_DIR, folder)
    os.makedirs(path_f, exist_ok=True)

inits_to_create = ['questionnaireapp/migrations/__init__.py', 'Users/migrations/__init__.py']

for path_init in inits_to_create:
    path_f = os.path.join(BASE_DIR, path_init)
    if not os.path.exists(path_f):
        Path(path_f).touch()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'django_filters',
    'crispy_forms',
    'Users',
    'questionnaireapp',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'questionnaire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'questionnaire.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

#authorization
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
SITE_ID = 1

AUTH_USER_MODEL = 'Users.CustomUser'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

LOGIN_URL = "/enter/login"
LOGIN_REDIRECT_URL = '/'
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_LOGOUT_REDIRECT_URL = "/enter/login"

# ACCOUNT_FORMS = {'login': 'base.forms.CustomLoginForm'}
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Silk
# SILKY_AUTHENTICATION = True  # User must login
# SILKY_AUTHORISATION = True  # User must have permissions
# SILKY_PERMISSIONS = lambda user: user.is_superuser
# SILKY_SENSITIVE_KEYS = {'username', 'api', 'token', 'key', 'secret', 'password', 'signature'}

# restfarmework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    # 'ROTATE_REFRESH_TOKENS': False,
    # 'BLACKLIST_AFTER_ROTATION': True,
    # 'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': 'your-secret-key',
    # 'VERIFYING_KEY': None,
    # 'AUTH_HEADER_TYPES': ('Bearer',),
    # 'USER_ID_FIELD': 'id',
    # 'AUTH_TOKEN_CLASSES': ('Users.views.CustomJWTAuthentication',),
    # 'TOKEN_USER_CLASS': 'django.contrib.auth.models.CustomUser',
}


# CELERY
CELERY_BROKER_URL = os.environ.get("REDIS_HOST", 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get("REDIS_HOST", 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERY_BEAT_SCHEDULE = {
    # 'parse_file_starter': {
    #     'task': 'questionnaireapp.tasks.my_function',
    #     'schedule': 60.0
    # },
}
# if not DEBUG:
#     CELERY_BEAT_SCHEDULE['my_task'] = {
#         'task': 'questionnaireapp.tasks.my_task',
#         'schedule': 3600.0  # execute every 1 hour
#     }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django/', 'django.log'),
            'formatter': 'verbose',
            'when': 'D',
            'backupCount': 30,
            'interval': 1,
        },
        'my_logger': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django/', 'my_logger.log'),
            'formatter': 'verbose',
            'when': 'D',
            'backupCount': 30,
            'interval': 1,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': 'ERROR',
            'propagate': True,
        },
        'my_logger': {
            'handlers': ['my_logger', ],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True