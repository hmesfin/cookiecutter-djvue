"""
Signals for User model.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    """
    Handle actions when a new user is created.
    Note: Welcome email is now sent after email verification, not on user creation.
    """
    if created and not instance.is_superuser:
        # Log new user creation
        logger.info(f"New user created: {instance.email}")
        
        # Note: We don't send welcome email here anymore.
        # Welcome email is sent after email verification in the verify_email endpoint.
        # This prevents users from receiving a welcome email before verifying their email.
        
        # You can add other initial setup tasks here if needed
        # For example: creating user preferences, initializing user stats, etc.


@receiver(post_save, sender=User)
def create_user_profile_directories(sender, instance, created, **kwargs):
    """
    Create user-specific directories when a new user is created.
    This is useful for organizing user uploads.
    """
    if created:
        import os
        from django.conf import settings
        
        if hasattr(settings, "MEDIA_ROOT"):
            # Create user-specific upload directory
            user_dir = os.path.join(settings.MEDIA_ROOT, "users", str(instance.id))
            os.makedirs(user_dir, exist_ok=True)
            
            # Create subdirectories for different file types
            for subdir in ["avatars", "documents", "temp"]:
                os.makedirs(os.path.join(user_dir, subdir), exist_ok=True)