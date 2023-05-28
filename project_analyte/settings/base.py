import os
from datetime import timedelta
from pathlib import Path
import environ
from celery.schedules import crontab

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PARENT_DIR = Path(__file__).resolve().parent.parent.parent


environ.Env.read_env(os.path.join(PARENT_DIR, '.envs/.django'))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # if DEBUG else environ.get('ALLOWED_HOSTS')
# print(f'AllowedHosts : {ALLOWED_HOSTS}')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key' if DEBUG else env('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',
    'django_filters',
    'django_celery_beat',

    # Local APPs
    'apps.user',
    'apps.file_handler',
    'apps.adminka',
    'apps.notification',
    'apps.payments'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_analyte.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project_analyte.wsgi.application'

ASGI_APPLICATION = 'project_analyte.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),  # 'analyte_development' if DEBUG else environ.get('NAME'),
        'USER': env('DB_USER'),  # 'analyte' if DEBUG else environ.get('USER'),
        'PASSWORD': env('DB_PASSWORD'),  # 'analyte' if DEBUG else environ.get('PASSWORD'),
        'HOST': env('DB_HOST'),  # 'localhost' if DEBUG else environ.get('HOST'),
        'PORT': env('DB_PORT'),  # '5432' if DEBUG else environ.get('PORT'),
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('127.0.0.1', 36376)]  # avoid port number conflict
#         }
#     }
# }



# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'api/v1/user/activation/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALIZERS': {
        "user_create": "apps.user.serializers.SimpleUserSerializer",
    },
    'PERMISSIONS': {
        "user_list": ["apps.user.permissions.IsAdmin"],
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Analytics Assistant API',
    'DESCRIPTION': 'Analytics Assistant API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'COMPONENT_SPLIT_REQUEST': True,

    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR'
}

CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST')  # [] if DEBUG else environ.get('CORS_ORIGIN_WHITELIST')
CORS_ORIGIN_ALLOW_ALL = env.bool('CORS_ORIGIN_ALLOW_ALL')  # False if DEBUG else environ.get('CORS_ORIGIN_ALLOW_ALL')
CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS')  # False if DEBUG else environ.get('CORS_ALLOW_CREDENTIALS')
CORS_ALLOW_HEADERS = env.list('CORS_ALLOW_HEADERS')  # [] if DEBUG else environ.get('CORS_ALLOW_HEADERS')

MEDIA_ROOT = os.path.join(PARENT_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PARENT_DIR, 'static')

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CELERY_BEAT_SCHEDULE = {
    "update_all_service_plan_status": {
        "task": "apps.payments.tasks.update_all_service_plan_status",
        "schedule": crontab(minute=0, hour=0),
    },
}

