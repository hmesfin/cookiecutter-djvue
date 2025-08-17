"""
Testing settings for {{ cookiecutter.project_name }} project.
"""
from .base import *

# Override settings for testing
DEBUG = False
TESTING = True

# Use in-memory SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Use simpler password hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Media files
MEDIA_ROOT = BASE_DIR / 'test_media'

# Disable cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Celery - use synchronous mode for testing
{% if cookiecutter.use_celery == 'y' -%}
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
{%- endif %}