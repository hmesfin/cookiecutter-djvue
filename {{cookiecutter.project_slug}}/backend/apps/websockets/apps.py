"""WebSockets app configuration."""
from django.apps import AppConfig


class WebSocketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.websockets'
    verbose_name = 'WebSockets'
    
    def ready(self):
        """Initialize WebSocket handlers when app is ready."""
        # Import signal handlers
        try:
            from . import signals
        except ImportError:
            pass