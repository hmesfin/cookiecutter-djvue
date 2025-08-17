"""
Development settings for {{ cookiecutter.project_name }} project.
"""
from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Additional apps for development
INSTALLED_APPS += [
    {% if cookiecutter.use_debug_toolbar == 'y' -%}
    'debug_toolbar',
    {%- endif %}
    'django_extensions',
]

# Additional middleware for development
MIDDLEWARE = [
    {% if cookiecutter.use_debug_toolbar == 'y' -%}
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    {%- endif %}
] + MIDDLEWARE

# Django Debug Toolbar
{% if cookiecutter.use_debug_toolbar == 'y' -%}
INTERNAL_IPS = ['127.0.0.1', 'localhost']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
}
{%- endif %}

# CORS for development
{% if cookiecutter.use_cors == 'y' -%}
CORS_ALLOWED_ORIGINS = [
    'http://localhost:{{ cookiecutter.frontend_port }}',
    'http://127.0.0.1:{{ cookiecutter.frontend_port }}',
]
{%- endif %}

# Email backend for development
{% if cookiecutter.use_mailhog == 'y' -%}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Use 'mailhog' hostname when running in Docker, 'localhost' otherwise
EMAIL_HOST = config('EMAIL_HOST', default='mailhog' if config('DJANGO_ENV', default='') == 'development' else 'localhost')
EMAIL_PORT = config('EMAIL_PORT', default=1025, cast=int)
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
{% else -%}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
{%- endif %}

# Static files
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging
LOGGING['loggers']['django']['level'] = 'DEBUG'

# Simple cache configuration for development
# Override the base settings if Redis is not available
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Use database sessions in development for simplicity
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Allow all origins in development (be careful!)
{% if cookiecutter.use_cors == 'y' -%}
# Uncomment for very permissive CORS in development
# CORS_ALLOW_ALL_ORIGINS = True
{%- endif %}