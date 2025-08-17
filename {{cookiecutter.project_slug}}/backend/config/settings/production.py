"""
Production settings for {{ cookiecutter.project_name }} project.
"""
import os
from .base import *

# Security
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '{{ cookiecutter.domain_name }}').split(',')

# Security Settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CORS Settings
{% if cookiecutter.use_cors == 'y' -%}
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True
{%- endif %}

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 60

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
{% if cookiecutter.use_whitenoise == 'y' -%}
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
{%- endif %}

# Media files - should use cloud storage in production
MEDIA_ROOT = BASE_DIR / 'media'

{% if cookiecutter.use_sentry == 'y' -%}
# Sentry Configuration
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN = os.environ.get('SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production'
    )
{%- endif %}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@{{ cookiecutter.domain_name }}')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# Admin Configuration
ADMINS = [
    (os.environ.get('ADMIN_NAME', '{{ cookiecutter.author_name }}'), 
     os.environ.get('ADMIN_EMAIL', '{{ cookiecutter.author_email }}')),
]
MANAGERS = ADMINS