"""Django settings for the MILA collectivo app."""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# TODO Go through https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
SECRET_KEY = os.environ['SECRET_KEY']

# TODO Set to False
DEBUG = True

# TODO Adapt for production
ALLOWED_HOSTS = ['*',"0.0.0.0","127.0.0.1", "localhost", "testserver"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'collectivo',
    'collectivo.menus',
    'collectivo.dashboard',
    'collectivo.auth',
    'collectivo.extensions',
    'collectivo.members',

    'rest_framework',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'collectivo.auth.middleware.KeycloakMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
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


# CUSTOM SETTINGS FOR COLLECTIVO

DEVELOPMENT = True

# Django Rest Framework (DRF)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ]
}


# DRF Spectacular (OpenAPI)

SPECTACULAR_SETTINGS = {
    # Allow for authentication via token in the SwaggerUI interface
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], }],
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timeandname': {
            'format': '[{name}] {message}',  # {asctime},
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'dataflair-debug.log',
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'timeandname',
        },
    },
    'loggers': {
        'collectivo': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'test_extension': {
            'handlers': ['console'],  # 'file',
            'level': 'DEBUG',  # os.getenv('DJANGO_LOG_LEVEL', 'DEBUG')
            'propagate': True,
        },
    },
}


# General settings for collectivo

COLLECTIVO = {

    # Define user groups and their respective roles
    'auth_groups_and_roles': {
        'members': ['members_user'],
        'members_active': ['shifts_user'],
        'superusers': ['collectivo_admin', 'members_admin', 'shifts_admin']
    },

    # Configuration for auth.middleware.KeycloakMiddleware
    'auth_keycloak_config': {
        'SERVER_URL': os.environ.get('KEYCLOAK_SERVER_URL'),
        'REALM_NAME': os.environ.get('KEYCLOAK_REALM_NAME'),
        'CLIENT_ID': os.environ.get('KEYCLOAK_CLIENT_ID'),
        'CLIENT_SECRET_KEY': os.environ.get('KEYCLOAK_CLIENT_SECRET_KEY')
    },

    # Path to default models
    'default_auth_manager': 'collectivo.auth.manager.KeycloakAuthManager',
    'default_user_model': 'collectivo.members.models.Member',
    'default_extension_model': 'collectivo.extensions.models.Extension',

}

