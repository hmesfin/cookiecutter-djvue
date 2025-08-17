"""WebSocket routing configuration."""
from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    # Notification WebSocket
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    
    # Chat WebSocket with room name
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    
    # Live data WebSocket
    path('ws/data/', consumers.LiveDataConsumer.as_asgi()),
]