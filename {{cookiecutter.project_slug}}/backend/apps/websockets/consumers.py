"""WebSocket consumers for real-time features."""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class BaseConsumer(AsyncWebsocketConsumer):
    """Base WebSocket consumer with authentication."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        # Get user from scope
        self.user = self.scope.get('user', AnonymousUser())
        
        if self.user.is_authenticated:
            # Add to user's personal group
            self.user_group = f'user_{self.user.id}'
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )
            
            # Accept connection
            await self.accept()
            
            # Send welcome message
            await self.send_json({
                'type': 'connection',
                'message': 'Connected successfully',
                'user_id': self.user.id
            })
            
            logger.info(f"WebSocket connected for user {self.user.id}")
        else:
            # Reject connection for unauthenticated users
            await self.close(code=4001)
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        if hasattr(self, 'user_group'):
            # Remove from user's group
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )
            
            logger.info(f"WebSocket disconnected for user {self.user.id}")
    
    async def send_json(self, content, close=False):
        """Send JSON data to WebSocket."""
        await self.send(text_data=json.dumps(content), close=close)
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Route to appropriate handler
            handler = getattr(self, f'handle_{message_type}', None)
            if handler:
                await handler(data)
            else:
                await self.send_json({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                })
        except json.JSONDecodeError:
            await self.send_json({
                'type': 'error',
                'message': 'Invalid JSON data'
            })
        except Exception as e:
            logger.error(f"Error handling WebSocket message: {e}")
            await self.send_json({
                'type': 'error',
                'message': 'Internal server error'
            })


class NotificationConsumer(BaseConsumer):
    """WebSocket consumer for notifications."""
    
    async def connect(self):
        """Handle connection and join notification groups."""
        await super().connect()
        
        if self.user.is_authenticated:
            # Join notification group
            self.notification_group = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(
                self.notification_group,
                self.channel_name
            )
            
            # Send unread notification count
            unread_count = await self.get_unread_notifications_count()
            await self.send_json({
                'type': 'notification_count',
                'count': unread_count
            })
    
    async def disconnect(self, close_code):
        """Handle disconnection."""
        if hasattr(self, 'notification_group'):
            await self.channel_layer.group_discard(
                self.notification_group,
                self.channel_name
            )
        
        await super().disconnect(close_code)
    
    async def handle_mark_read(self, data):
        """Mark notification as read."""
        notification_id = data.get('notification_id')
        if notification_id:
            await self.mark_notification_read(notification_id)
            await self.send_json({
                'type': 'notification_marked_read',
                'notification_id': notification_id
            })
    
    async def handle_mark_all_read(self, data):
        """Mark all notifications as read."""
        await self.mark_all_notifications_read()
        await self.send_json({
            'type': 'all_notifications_marked_read'
        })
    
    # Group message handlers
    async def notification_message(self, event):
        """Handle notification from group."""
        await self.send_json({
            'type': 'notification',
            'notification': event['notification']
        })
    
    # Database operations
    @database_sync_to_async
    def get_unread_notifications_count(self):
        """Get count of unread notifications."""
        # This would connect to your notification model
        # return Notification.objects.filter(user=self.user, is_read=False).count()
        return 0  # Placeholder
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark specific notification as read."""
        # Notification.objects.filter(id=notification_id, user=self.user).update(is_read=True)
        pass  # Placeholder
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all notifications as read."""
        # Notification.objects.filter(user=self.user, is_read=False).update(is_read=True)
        pass  # Placeholder


class ChatConsumer(BaseConsumer):
    """WebSocket consumer for chat functionality."""
    
    async def connect(self):
        """Handle connection and join chat room."""
        # Get room name from URL route
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'general')
        self.room_group_name = f'chat_{self.room_name}'
        
        await super().connect()
        
        if self.user.is_authenticated:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            # Notify room about new user
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_joined',
                    'user_id': self.user.id,
                    'username': self.user.username
                }
            )
            
            # Send recent messages
            recent_messages = await self.get_recent_messages()
            await self.send_json({
                'type': 'recent_messages',
                'messages': recent_messages
            })
    
    async def disconnect(self, close_code):
        """Handle disconnection."""
        if hasattr(self, 'room_group_name'):
            # Notify room about user leaving
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_left',
                    'user_id': self.user.id,
                    'username': self.user.username
                }
            )
            
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        
        await super().disconnect(close_code)
    
    async def handle_message(self, data):
        """Handle chat message."""
        message = data.get('message', '').strip()
        
        if message:
            # Save message to database
            saved_message = await self.save_message(message)
            
            # Broadcast to room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': saved_message
                }
            )
    
    async def handle_typing(self, data):
        """Handle typing indicator."""
        is_typing = data.get('is_typing', False)
        
        # Broadcast typing status to room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_typing': is_typing
            }
        )
    
    # Group message handlers
    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        await self.send_json({
            'type': 'message',
            'message': event['message']
        })
    
    async def user_joined(self, event):
        """Notify about user joining."""
        await self.send_json({
            'type': 'user_joined',
            'user_id': event['user_id'],
            'username': event['username']
        })
    
    async def user_left(self, event):
        """Notify about user leaving."""
        await self.send_json({
            'type': 'user_left',
            'user_id': event['user_id'],
            'username': event['username']
        })
    
    async def typing_indicator(self, event):
        """Send typing indicator."""
        # Don't send typing indicator to the user who is typing
        if event['user_id'] != self.user.id:
            await self.send_json({
                'type': 'typing',
                'user_id': event['user_id'],
                'username': event['username'],
                'is_typing': event['is_typing']
            })
    
    # Database operations
    @database_sync_to_async
    def get_recent_messages(self, limit=50):
        """Get recent messages from database."""
        # This would connect to your message model
        # messages = Message.objects.filter(room=self.room_name).order_by('-created_at')[:limit]
        # return [message.to_dict() for message in reversed(messages)]
        return []  # Placeholder
    
    @database_sync_to_async
    def save_message(self, content):
        """Save message to database."""
        # message = Message.objects.create(
        #     room=self.room_name,
        #     user=self.user,
        #     content=content
        # )
        # return message.to_dict()
        return {
            'id': 1,
            'user_id': self.user.id,
            'username': self.user.username,
            'content': content,
            'timestamp': '2024-01-01T00:00:00Z'
        }  # Placeholder


class LiveDataConsumer(BaseConsumer):
    """WebSocket consumer for live data updates."""
    
    async def connect(self):
        """Handle connection and subscribe to data streams."""
        await super().connect()
        
        if self.user.is_authenticated:
            # Join live data group
            self.data_group = 'live_data'
            await self.channel_layer.group_add(
                self.data_group,
                self.channel_name
            )
            
            # Send initial data
            await self.send_initial_data()
    
    async def disconnect(self, close_code):
        """Handle disconnection."""
        if hasattr(self, 'data_group'):
            await self.channel_layer.group_discard(
                self.data_group,
                self.channel_name
            )
        
        await super().disconnect(close_code)
    
    async def handle_subscribe(self, data):
        """Subscribe to specific data streams."""
        streams = data.get('streams', [])
        
        for stream in streams:
            stream_group = f'data_{stream}'
            await self.channel_layer.group_add(
                stream_group,
                self.channel_name
            )
        
        await self.send_json({
            'type': 'subscribed',
            'streams': streams
        })
    
    async def handle_unsubscribe(self, data):
        """Unsubscribe from data streams."""
        streams = data.get('streams', [])
        
        for stream in streams:
            stream_group = f'data_{stream}'
            await self.channel_layer.group_discard(
                stream_group,
                self.channel_name
            )
        
        await self.send_json({
            'type': 'unsubscribed',
            'streams': streams
        })
    
    # Group message handlers
    async def data_update(self, event):
        """Send data update to WebSocket."""
        await self.send_json({
            'type': 'data_update',
            'stream': event['stream'],
            'data': event['data']
        })
    
    async def send_initial_data(self):
        """Send initial data snapshot."""
        # Get initial data from cache or database
        initial_data = await self.get_initial_data()
        
        await self.send_json({
            'type': 'initial_data',
            'data': initial_data
        })
    
    @database_sync_to_async
    def get_initial_data(self):
        """Get initial data snapshot."""
        # This would fetch initial data from your models
        return {
            'users_online': 0,
            'server_time': '2024-01-01T00:00:00Z'
        }  # Placeholder