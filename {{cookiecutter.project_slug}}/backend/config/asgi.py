"""
ASGI config for {{ cookiecutter.project_name }} project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early
django_asgi_app = get_asgi_application()

{% if cookiecutter.use_channels == 'y' -%}
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Import websocket routing after Django setup
{% if cookiecutter.use_websockets_enhanced == 'y' -%}
from apps.websockets.routing import websocket_urlpatterns
from apps.websockets.middleware import JWTAuthMiddleware, WebSocketLoggingMiddleware

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        WebSocketLoggingMiddleware(
            JWTAuthMiddleware(
                URLRouter(websocket_urlpatterns)
            )
        )
    ),
})
{% else -%}
# Basic channels setup without enhanced websockets
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Add basic websocket support here if needed
})
{%- endif %}
{% else -%}
application = django_asgi_app
{%- endif %}