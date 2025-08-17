"""WebSocket middleware for authentication."""
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
import jwt
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@database_sync_to_async
def get_user_from_token(token_key):
    """Get user from JWT token."""
    try:
        # Decode JWT token
        payload = jwt.decode(
            token_key,
            settings.SECRET_KEY,
            algorithms=['HS256']
        )
        
        # Get user from payload
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist) as e:
        logger.error(f"WebSocket auth error: {e}")
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """JWT authentication middleware for WebSockets."""
    
    async def __call__(self, scope, receive, send):
        """Process WebSocket connection."""
        # Get token from query string
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        
        if token:
            # Authenticate user
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)


class WebSocketLoggingMiddleware(BaseMiddleware):
    """Logging middleware for WebSocket connections."""
    
    async def __call__(self, scope, receive, send):
        """Log WebSocket activity."""
        path = scope.get('path', '')
        user = scope.get('user', AnonymousUser())
        
        if user.is_authenticated:
            logger.info(f"WebSocket connection: {path} by user {user.id}")
        else:
            logger.info(f"WebSocket connection: {path} by anonymous user")
        
        return await super().__call__(scope, receive, send)