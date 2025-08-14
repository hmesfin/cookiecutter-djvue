"""
Async tasks for User app.
Gracefully handles both Celery and synchronous execution.
"""
import logging
import os
from typing import Optional

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

{% if cookiecutter.use_celery == 'y' -%}
try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
{% else -%}
CELERY_AVAILABLE = False
{%- endif %}

logger = logging.getLogger(__name__)


def task_decorator(func):
    """
    Decorator that makes a function a Celery task if available,
    otherwise returns the function as-is for synchronous execution.
    """
    {% if cookiecutter.use_celery == 'y' -%}
    if CELERY_AVAILABLE:
        return shared_task(
            bind=True,
            autoretry_for=(Exception,),
            retry_backoff=True,
            retry_kwargs={"max_retries": 3},
        )(func)
    {%- endif %}
    return func


@task_decorator
def send_welcome_email(self=None, user_id: int = None) -> bool:
    """
    Send welcome email to a new user.
    
    This function works both as a Celery task and as a regular function.
    When Celery is available, it will be executed asynchronously.
    Otherwise, it will run synchronously.
    
    Args:
        self: Celery task instance (only when running as task)
        user_id: ID of the user to send email to
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    from {{ cookiecutter.project_slug }}.apps.users.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        # Prepare email context
        context = {
            "user": user,
            "project_name": "{{ cookiecutter.project_name }}",
            "domain": getattr(settings, "DOMAIN_NAME", "{{ cookiecutter.domain_name }}"),
            "protocol": "https" if not settings.DEBUG else "http",
        }
        
        # Render email templates (we'll create these next)
        subject = f"Welcome to {{ cookiecutter.project_name }}, {user.get_short_name()}!"
        
        # Try to use HTML template if it exists
        try:
            html_message = render_to_string("emails/users/welcome.html", context)
            plain_message = strip_tags(html_message)
        except Exception:
            # Fallback to plain text
            plain_message = f"""
            Hi {user.get_short_name()},
            
            Welcome to {{ cookiecutter.project_name }}! We're excited to have you on board.
            
            Your account has been successfully created with the email: {user.email}
            
            Please log in to start exploring our features.
            
            If you have any questions, feel free to reach out to our support team.
            
            Best regards,
            The {{ cookiecutter.project_name }} Team
            """
            html_message = None
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Welcome email sent successfully to {user.email}")
        return True
        
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Failed to send welcome email to user {user_id}: {str(e)}")
        {% if cookiecutter.use_celery == 'y' -%}
        if CELERY_AVAILABLE and self:
            # If running as Celery task, raise to trigger retry
            raise
        {%- endif %}
        return False


@task_decorator
def send_verification_email(self=None, user_id: int = None, verification_url: str = None) -> bool:
    """
    Send email verification link to user.
    
    Args:
        self: Celery task instance (only when running as task)
        user_id: ID of the user to send email to
        verification_url: URL for email verification
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    from {{ cookiecutter.project_slug }}.apps.users.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        if user.is_verified:
            logger.info(f"User {user.email} is already verified")
            return True
        
        context = {
            "user": user,
            "verification_url": verification_url,
            "project_name": "{{ cookiecutter.project_name }}",
        }
        
        subject = "Verify your email address"
        
        try:
            html_message = render_to_string("emails/users/verify_email.html", context)
            plain_message = strip_tags(html_message)
        except Exception:
            plain_message = f"""
            Hi {user.get_short_name()},
            
            Please verify your email address by clicking the link below:
            
            {verification_url}
            
            This link will expire in 24 hours.
            
            If you didn't create an account, please ignore this email.
            
            Best regards,
            The {{ cookiecutter.project_name }} Team
            """
            html_message = None
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Verification email sent successfully to {user.email}")
        return True
        
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Failed to send verification email to user {user_id}: {str(e)}")
        {% if cookiecutter.use_celery == 'y' -%}
        if CELERY_AVAILABLE and self:
            raise
        {%- endif %}
        return False


@task_decorator
def send_password_reset_email(self=None, user_id: int = None, reset_url: str = None) -> bool:
    """
    Send password reset email to user.
    
    Args:
        self: Celery task instance (only when running as task)
        user_id: ID of the user to send email to
        reset_url: URL for password reset
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    from {{ cookiecutter.project_slug }}.apps.users.models import User
    
    try:
        user = User.objects.get(id=user_id)
        
        context = {
            "user": user,
            "reset_url": reset_url,
            "project_name": "{{ cookiecutter.project_name }}",
        }
        
        subject = "Reset your password"
        
        try:
            html_message = render_to_string("emails/users/password_reset.html", context)
            plain_message = strip_tags(html_message)
        except Exception:
            plain_message = f"""
            Hi {user.get_short_name()},
            
            We received a request to reset your password. Click the link below to set a new password:
            
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you didn't request a password reset, please ignore this email.
            
            Best regards,
            The {{ cookiecutter.project_name }} Team
            """
            html_message = None
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Password reset email sent successfully to {user.email}")
        return True
        
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist")
        return False
    except Exception as e:
        logger.error(f"Failed to send password reset email to user {user_id}: {str(e)}")
        {% if cookiecutter.use_celery == 'y' -%}
        if CELERY_AVAILABLE and self:
            raise
        {%- endif %}
        return False


def send_email_task(user_id: int, email_type: str = "welcome", **kwargs) -> bool:
    """
    Helper function to send emails either asynchronously or synchronously.
    
    This function automatically detects if Celery is available and configured.
    If yes, it queues the task. If not, it executes synchronously.
    
    Args:
        user_id: ID of the user to send email to
        email_type: Type of email to send ('welcome', 'verification', 'password_reset')
        **kwargs: Additional arguments for specific email types
        
    Returns:
        bool or AsyncResult: Task result or AsyncResult object if using Celery
    """
    email_functions = {
        "welcome": send_welcome_email,
        "verification": send_verification_email,
        "password_reset": send_password_reset_email,
    }
    
    if email_type not in email_functions:
        logger.error(f"Unknown email type: {email_type}")
        return False
    
    email_func = email_functions[email_type]
    
    {% if cookiecutter.use_celery == 'y' -%}
    logger.debug(f"CELERY_AVAILABLE: {CELERY_AVAILABLE}")
    logger.debug(f"CELERY_TASK_ALWAYS_EAGER: {getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False)}")
    logger.debug(f"USE_CELERY: {getattr(settings, 'USE_CELERY', True)}")
    logger.debug(f"REDIS_URL from env: {os.environ.get('REDIS_URL', 'NOT SET')}")
    logger.debug(f"CELERY_BROKER_URL from settings: {getattr(settings, 'CELERY_BROKER_URL', 'NOT SET')}")
    {%- endif %}
    
    {% if cookiecutter.use_celery == 'y' -%}
    # Check if we should use Celery
    use_celery = (
        CELERY_AVAILABLE
        and getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False) is False
        and getattr(settings, "USE_CELERY", True)
    )
    
    if use_celery:
        try:
            # Queue as Celery task
            logger.info(f"Attempting to queue {email_type} email task for user {user_id} via Celery")
            result = email_func.delay(user_id=user_id, **kwargs)
            logger.info(f"Successfully queued {email_type} email task: {result.id}")
            return result
        except Exception as e:
            logger.error(f"Failed to queue task via Celery, falling back to synchronous: {str(e)}")
            # Fall back to synchronous execution
            return email_func(user_id=user_id, **kwargs)
    else:
        # Execute synchronously
        logger.info(f"Executing {email_type} email task synchronously for user {user_id}")
        return email_func(user_id=user_id, **kwargs)
    {% else -%}
    # Execute synchronously (Celery not configured)
    return email_func(user_id=user_id, **kwargs)
    {%- endif %}