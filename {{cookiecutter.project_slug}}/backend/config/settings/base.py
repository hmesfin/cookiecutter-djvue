"""
Base Django settings for {{ cookiecutter.project_name }} project.
"""
import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-this-in-production')

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
    {% if cookiecutter.api_authentication == 'token' or cookiecutter.use_social_auth == 'y' -%}
    # Token auth required for dj-rest-auth
    'rest_framework.authtoken',
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
    {% if cookiecutter.use_social_auth == 'y' -%}
    # Social authentication
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    {% if 'google' in cookiecutter.social_auth_providers -%}
    'allauth.socialaccount.providers.google',
    {% endif -%}
    {% if 'github' in cookiecutter.social_auth_providers -%}
    'allauth.socialaccount.providers.github',
    {% endif -%}
    {% if 'facebook' in cookiecutter.social_auth_providers -%}
    'allauth.socialaccount.providers.facebook',
    {% endif -%}
    {% if 'twitter' in cookiecutter.social_auth_providers -%}
    'allauth.socialaccount.providers.twitter',
    {% endif -%}
    'dj_rest_auth',
    'dj_rest_auth.registration',
    {%- endif %}
    {% if cookiecutter.use_graphql == 'y' -%}
    # Strawberry GraphQL Django integration
    'strawberry_django',
    {%- endif %}
]

LOCAL_APPS = [
    'apps.core',
    'apps.users',
    'apps.api',
    {% if cookiecutter.use_social_auth == 'y' -%}
    'apps.social_auth',
    {%- endif %}
    {% if cookiecutter.use_redis == 'y' -%}
    'apps.cache',
    'apps.emails',
    {%- endif %}
    {% if cookiecutter.use_graphql == 'y' -%}
    'apps.graphql',
    {%- endif %}
    {% if cookiecutter.use_websockets_enhanced == 'y' -%}
    'apps.websockets',
    {%- endif %}
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
    {% if cookiecutter.use_social_auth == 'y' -%}
    # Required for django-allauth
    'allauth.account.middleware.AccountMiddleware',
    {%- endif %}
    # Custom middleware
    'apps.core.middleware.APIMetricsMiddleware',
    'apps.core.middleware.HealthCheckMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
ASGI_APPLICATION = 'config.asgi.application'
{% else -%}
WSGI_APPLICATION = 'config.wsgi.application'
{%- endif %}

# Database
# Supports DATABASE_URL for easy configuration
import dj_database_url

DATABASE_URL = config('DATABASE_URL', default=None)

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
            'NAME': config('POSTGRES_DB', default='{{ cookiecutter.project_slug }}'),
            'USER': config('POSTGRES_USER', default='{{ cookiecutter.project_slug }}'),
            'PASSWORD': config('POSTGRES_PASSWORD', default='changeme'),
            'HOST': config('POSTGRES_HOST', default='localhost'),
            'PORT': config('POSTGRES_PORT', default='5432'),
        }
    }
    {% elif cookiecutter.database == 'mysql' -%}
    # MySQL configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DATABASE', default='{{ cookiecutter.project_slug }}'),
            'USER': config('MYSQL_USER', default='{{ cookiecutter.project_slug }}'),
            'PASSWORD': config('MYSQL_PASSWORD', default='changeme'),
            'HOST': config('MYSQL_HOST', default='localhost'),
            'PORT': config('MYSQL_PORT', default='3306'),
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
    'apps.users.backends.EmailOrUsernameBackend',
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

# Cache configuration
{% if cookiecutter.use_redis == 'y' -%}
# Redis cache configuration
USE_REDIS_CACHE = config('USE_REDIS_CACHE', default=True, cast=bool)

if USE_REDIS_CACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                'IGNORE_EXCEPTIONS': True,
            },
            'KEY_PREFIX': '{{ cookiecutter.project_slug }}',
            'TIMEOUT': 300,  # Default 5 minutes
        },
        'session': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/2'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'IGNORE_EXCEPTIONS': True,
            },
            'KEY_PREFIX': '{{ cookiecutter.project_slug }}_session',
        },
        'static': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'static-cache',
            'TIMEOUT': 3600,  # 1 hour for static content
        }
    }
    # Session configuration for Redis
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'session'
else:
    # Fallback to local memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
    # Session configuration for database
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
{% else -%}
# Local memory cache configuration (no Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
# Session configuration for database
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
{%- endif %}

SESSION_COOKIE_AGE = 86400  # 24 hours

# Cache middleware settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = '{{ cookiecutter.project_slug }}_cache'

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
CELERY_BROKER_URL = config('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', 'redis://localhost:6379/0')
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
        'LOCATION': config('REDIS_URL', 'redis://localhost:6379/1'),
    }
}
{%- endif %}

{% if cookiecutter.use_channels == 'y' -%}
# Channels Configuration
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_URL', 'redis://localhost:6379/2')],
        },
    },
}
{%- endif %}

# Frontend URL for email links
FRONTEND_URL = config('FRONTEND_URL', 'http://localhost:{{ cookiecutter.frontend_port }}')

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', 'localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', 'noreply@{{ cookiecutter.domain_name }}')

# Email Task Configuration
SEND_WELCOME_EMAIL = config('SEND_WELCOME_EMAIL', default=True, cast=bool)
SEND_VERIFICATION_EMAIL = config('SEND_VERIFICATION_EMAIL', default=True, cast=bool)
{% if cookiecutter.use_celery == 'y' -%}
USE_CELERY = config('USE_CELERY', default=True, cast=bool)  # Can disable Celery for emails
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
            'level': config('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

{% if cookiecutter.use_social_auth == 'y' -%}
# Django Allauth Configuration
SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_QUERY_EMAIL = True

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    {% if 'google' in cookiecutter.social_auth_providers -%}
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': config('GOOGLE_OAUTH_CLIENT_ID', ''),
            'secret': config('GOOGLE_OAUTH_CLIENT_SECRET', ''),
            'key': ''
        }
    },
    {% endif -%}
    {% if 'github' in cookiecutter.social_auth_providers -%}
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
        'APP': {
            'client_id': config('GITHUB_OAUTH_CLIENT_ID', ''),
            'secret': config('GITHUB_OAUTH_CLIENT_SECRET', ''),
            'key': ''
        }
    },
    {% endif -%}
    {% if 'facebook' in cookiecutter.social_auth_providers -%}
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
        'APP': {
            'client_id': config('FACEBOOK_OAUTH_CLIENT_ID', ''),
            'secret': config('FACEBOOK_OAUTH_CLIENT_SECRET', ''),
            'key': ''
        }
    },
    {% endif -%}
    {% if 'twitter' in cookiecutter.social_auth_providers -%}
    'twitter': {
        'APP': {
            'client_id': config('TWITTER_OAUTH_CLIENT_ID', ''),
            'secret': config('TWITTER_OAUTH_CLIENT_SECRET', ''),
            'key': config('TWITTER_OAUTH_API_KEY', ''),
        }
    },
    {% endif -%}
}
{%- endif %}

{% if cookiecutter.use_graphql == 'y' -%}
# Strawberry GraphQL Configuration
# Strawberry doesn't require special Django settings
# Schema is configured directly in the views

# Custom JWT settings for GraphQL (using PyJWT)
GRAPHQL_JWT_SECRET_KEY = SECRET_KEY
GRAPHQL_JWT_ALGORITHM = 'HS256'
GRAPHQL_JWT_EXPIRATION_DELTA = 24  # hours
GRAPHQL_JWT_REFRESH_EXPIRATION_DELTA = 7  # days
{%- endif %}