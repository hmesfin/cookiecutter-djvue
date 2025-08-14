"""
Base Django settings for {{ cookiecutter.project_name }} project.
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    {% if cookiecutter.api_authentication == 'jwt' -%}
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    {%- endif %}
    {% if cookiecutter.use_cors == 'y' -%}
    'corsheaders',
    {%- endif %}
    {% if cookiecutter.use_drf_spectacular == 'y' -%}
    'drf_spectacular',
    {%- endif %}
    {% if cookiecutter.use_celery == 'y' -%}
    'django_celery_beat',
    'django_celery_results',
    {%- endif %}
    {% if cookiecutter.use_channels == 'y' -%}
    'channels',
    {%- endif %}
]

LOCAL_APPS = [
    '{{ cookiecutter.project_slug }}.apps.core',
    '{{ cookiecutter.project_slug }}.apps.users',
    '{{ cookiecutter.project_slug }}.apps.api',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    {% if cookiecutter.use_whitenoise == 'y' -%}
    'whitenoise.middleware.WhiteNoiseMiddleware',
    {%- endif %}
    {% if cookiecutter.use_cors == 'y' -%}
    'corsheaders.middleware.CorsMiddleware',
    {%- endif %}
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom middleware
    '{{ cookiecutter.project_slug }}.apps.core.middleware.APIMetricsMiddleware',
    '{{ cookiecutter.project_slug }}.apps.core.middleware.HealthCheckMiddleware',
]

ROOT_URLCONF = '{{ cookiecutter.project_slug }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

{% if cookiecutter.use_channels == 'y' -%}
ASGI_APPLICATION = '{{ cookiecutter.project_slug }}.asgi.application'
{% else -%}
WSGI_APPLICATION = '{{ cookiecutter.project_slug }}.wsgi.application'
{%- endif %}

# Database
# Supports DATABASE_URL for easy configuration
import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL', None)

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    {% if cookiecutter.database == 'postgresql' -%}
    # PostgreSQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', '{{ cookiecutter.project_slug }}'),
            'USER': os.environ.get('POSTGRES_USER', '{{ cookiecutter.project_slug }}'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'changeme'),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
    {% elif cookiecutter.database == 'mysql' -%}
    # MySQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE', '{{ cookiecutter.project_slug }}'),
            'USER': os.environ.get('MYSQL_USER', '{{ cookiecutter.project_slug }}'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'changeme'),
            'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
            'PORT': os.environ.get('MYSQL_PORT', '3306'),
        }
    }
    {% else -%}
    # SQLite configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    {%- endif %}

# Password validation
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

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Authentication backends - allow login with username or email
AUTHENTICATION_BACKENDS = [
    '{{ cookiecutter.project_slug }}.apps.users.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',  # Keep default as fallback
]

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = '{{ cookiecutter.timezone }}'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
{%- endif %}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    {% if cookiecutter.api_authentication == 'jwt' -%}
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    {% elif cookiecutter.api_authentication == 'token' -%}
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    {% else -%}
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    {%- endif %}
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    {% if cookiecutter.use_drf_spectacular == 'y' -%}
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    {%- endif %}
}

{% if cookiecutter.api_authentication == 'jwt' -%}
# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
{%- endif %}

{% if cookiecutter.use_cors == 'y' -%}
# CORS Settings
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True
{%- endif %}

{% if cookiecutter.use_drf_spectacular == 'y' -%}
# API Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': '{{ cookiecutter.project_name }} API',
    'DESCRIPTION': '{{ cookiecutter.project_description }}',
    'VERSION': '{{ cookiecutter.version }}',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
}
{%- endif %}

{% if cookiecutter.use_celery == 'y' -%}
# Celery Configuration
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
{%- endif %}

{% if cookiecutter.use_redis == 'y' -%}
# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/1'),
    }
}
{%- endif %}

{% if cookiecutter.use_channels == 'y' -%}
# Channels Configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379/2')],
        },
    },
}
{%- endif %}

# Frontend URL for email links
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:{{ cookiecutter.frontend_port }}')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@{{ cookiecutter.domain_name }}')

# Email Task Configuration
SEND_WELCOME_EMAIL = os.environ.get('SEND_WELCOME_EMAIL', 'True') == 'True'
SEND_VERIFICATION_EMAIL = os.environ.get('SEND_VERIFICATION_EMAIL', 'True') == 'True'
{% if cookiecutter.use_celery == 'y' -%}
USE_CELERY = os.environ.get('USE_CELERY', 'True') == 'True'  # Can disable Celery for emails
{%- endif %}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}