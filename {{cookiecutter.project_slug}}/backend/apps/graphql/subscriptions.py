"""GraphQL subscriptions for real-time updates."""
import graphene
import channels_graphql_ws
from graphql_jwt.decorators import login_required
from apps.graphql.schema import UserType
from django.contrib.auth import get_user_model

User = get_user_model()


class OnUserUpdate(channels_graphql_ws.Subscription):
    """Subscribe to user updates."""
    
    # Subscription payload
    user = graphene.Field(UserType)
    event_type = graphene.String()
    
    class Arguments:
        user_id = graphene.ID()
    
    @staticmethod
    @login_required
    def subscribe(root, info, user_id=None):
        """Subscribe to user updates."""
        # Return channel group name to subscribe to
        if user_id:
            return [f"user_{user_id}"]
        else:
            # Subscribe to current user's updates
            return [f"user_{info.context.user.id}"]
    
    @staticmethod
    def publish(payload, info, user_id=None):
        """Process subscription payload."""
        return OnUserUpdate(
            user=payload.get('user'),
            event_type=payload.get('event_type', 'update')
        )
    
    @classmethod
    def broadcast(cls, group, payload):
        """Broadcast update to subscribers."""
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group,
            {
                'type': 'graphql.subscription',
                'payload': payload
            }
        )


class OnNotification(channels_graphql_ws.Subscription):
    """Subscribe to notifications."""
    
    # Subscription payload
    message = graphene.String()
    type = graphene.String()
    data = graphene.JSONString()
    timestamp = graphene.DateTime()
    
    class Arguments:
        types = graphene.List(graphene.String)
    
    @staticmethod
    @login_required
    def subscribe(root, info, types=None):
        """Subscribe to notifications."""
        user = info.context.user
        groups = [f"notifications_{user.id}"]
        
        # Subscribe to specific notification types if provided
        if types:
            for notification_type in types:
                groups.append(f"notifications_{user.id}_{notification_type}")
        
        return groups
    
    @staticmethod
    def publish(payload, info, types=None):
        """Process notification payload."""
        return OnNotification(
            message=payload.get('message'),
            type=payload.get('type'),
            data=payload.get('data'),
            timestamp=payload.get('timestamp')
        )


class OnlineUsersSubscription(channels_graphql_ws.Subscription):
    """Subscribe to online users list."""
    
    # Subscription payload
    online_users = graphene.List(UserType)
    user_joined = graphene.Field(UserType)
    user_left = graphene.Field(UserType)
    
    @staticmethod
    @login_required
    def subscribe(root, info):
        """Subscribe to online users updates."""
        return ["online_users"]
    
    @staticmethod
    def publish(payload, info):
        """Process online users payload."""
        return OnlineUsersSubscription(
            online_users=payload.get('online_users', []),
            user_joined=payload.get('user_joined'),
            user_left=payload.get('user_left')
        )
    
    @classmethod
    def notify_user_joined(cls, user):
        """Notify when user comes online."""
        from django.core.cache import cache
        
        # Update online users in cache
        online_users = cache.get('online_users', [])
        if user.id not in [u.id for u in online_users]:
            online_users.append(user)
            cache.set('online_users', online_users, 300)  # 5 minutes TTL
        
        # Broadcast update
        cls.broadcast('online_users', {
            'online_users': online_users,
            'user_joined': user
        })
    
    @classmethod
    def notify_user_left(cls, user):
        """Notify when user goes offline."""
        from django.core.cache import cache
        
        # Update online users in cache
        online_users = cache.get('online_users', [])
        online_users = [u for u in online_users if u.id != user.id]
        cache.set('online_users', online_users, 300)
        
        # Broadcast update
        cls.broadcast('online_users', {
            'online_users': online_users,
            'user_left': user
        })


class Subscription(graphene.ObjectType):
    """Root subscription object."""
    on_user_update = OnUserUpdate.Field()
    on_notification = OnNotification.Field()
    online_users = OnlineUsersSubscription.Field()