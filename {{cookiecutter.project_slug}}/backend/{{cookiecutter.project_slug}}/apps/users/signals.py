"""
Signals for User model.
"""
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

from .tasks import send_email_task

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    """
    Handle actions when a new user is created.
    Sends welcome email either via Celery task or synchronously.
    """
    if created and not instance.is_superuser:
        # Check if welcome emails are enabled
        send_welcome = getattr(settings, "SEND_WELCOME_EMAIL", True)
        
        if send_welcome:
            try:
                # This will use Celery if available, otherwise run synchronously
                result = send_email_task(
                    user_id=instance.id,
                    email_type="welcome"
                )
                
                {% if cookiecutter.use_celery == 'y' -%}
                # Log task ID if using Celery
                if hasattr(result, "id"):
                    logger.info(f"Welcome email queued for {instance.email} (Task ID: {result.id})")
                else:
                    logger.info(f"Welcome email sent synchronously to {instance.email}")
                {% else -%}
                if result:
                    logger.info(f"Welcome email sent to {instance.email}")
                {%- endif %}
                    
            except Exception as e:
                # Log the error but don't break the user creation
                logger.error(f"Failed to queue/send welcome email for {instance.email}: {str(e)}")


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