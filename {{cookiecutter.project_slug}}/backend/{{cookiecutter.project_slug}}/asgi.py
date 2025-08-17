"""
ASGI config for {{ cookiecutter.project_name }} project.
"""
import os

from django.core.asgi import get_asgi_application
{% if cookiecutter.use_channels == 'y' -%}
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
{%- endif %}

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project_slug }}.settings')

{% if cookiecutter.use_channels == 'y' -%}
django_asgi_app = get_asgi_application()

# Import websocket routing after Django setup
from apps.api import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        )
    ),
})
{% else -%}
application = get_asgi_application()
{%- endif %}