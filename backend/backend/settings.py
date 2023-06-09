import locale_settings

import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = locale_settings.secret_key

DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.User'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base',
    'users',
    'accounts',
    'reviews',
    'patientcard',
    'notifications',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'backend.password_validation.PasswordLengthValidation',
    },
    {
        'NAME': 'backend.password_validation.PasswordUppercaseValidation',
    },
    {
        'NAME': 'backend.password_validation.PasswordLowercaseValidation',
    },
    {
        'NAME': 'backend.password_validation.PasswordDigitValidation',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kyiv'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Polyclinic API',
    'DESCRIPTION': 'API for polyclinic',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Celery

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24
REGISTRATION_CONFIRM = 60 * 60 * 24

FRONTEND_HOST = locale_settings.frontend_host
FRONTEND_PASSWORD_RESET_PATH = '/password-reset-confirm/{uid}/{token}'
FRONTEND_REGISTRATION_CONFIRM_PATH = '/register-user-confirm/{uid}/{token}'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#Email sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = locale_settings.email_host_user
EMAIL_HOST_PASSWORD = locale_settings.email_host_password
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
