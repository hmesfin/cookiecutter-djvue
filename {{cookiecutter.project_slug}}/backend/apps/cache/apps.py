"""Cache app configuration."""
from django.apps import AppConfig


class CacheConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cache'
    verbose_name = 'Cache Management'