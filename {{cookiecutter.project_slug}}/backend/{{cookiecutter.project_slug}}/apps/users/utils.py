"""
Utility functions for User app.
"""
from typing import Optional

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for email verification.
    Uses Django's built-in PasswordResetTokenGenerator with a different key.
    """
    
    def _make_hash_value(self, user, timestamp):
        """
        Create hash value including user's verification status.
        Token becomes invalid after email is verified.
        """
        return (
            str(user.pk) + 
            str(timestamp) + 
            str(user.is_verified) +
            str(user.email)
        )


# Create instances
email_verification_token = EmailVerificationTokenGenerator()


def generate_verification_token(user: User) -> tuple[str, str]:
    """
    Generate a verification token for a user.
    
    Args:
        user: User instance
        
    Returns:
        tuple: (uid, token) - Base64 encoded user ID and verification token
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    return uid, token


def verify_token(uidb64: str, token: str) -> Optional[User]:
    """
    Verify a token and return the user if valid.
    
    Args:
        uidb64: Base64 encoded user ID
        token: Verification token
        
    Returns:
        User instance if token is valid, None otherwise
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None
    
    if email_verification_token.check_token(user, token):
        return user
    
    return None


def send_verification_email_to_user(user: User, request=None) -> bool:
    """
    Send verification email to a user.
    
    Args:
        user: User instance
        request: Optional HTTP request for building absolute URLs
        
    Returns:
        bool: True if email was queued/sent successfully
    """
    from .tasks import send_email_task
    
    if user.is_verified:
        return True
    
    # Generate verification token
    uid, token = generate_verification_token(user)
    
    # Build verification URL
    if request:
        from django.urls import reverse
        verification_path = reverse('api:verify_email', kwargs={'uidb64': uid, 'token': token})
        verification_url = request.build_absolute_uri(verification_path)
    else:
        from django.conf import settings
        domain = getattr(settings, 'DOMAIN_NAME', 'example.com')
        protocol = 'https' if not settings.DEBUG else 'http'
        verification_url = f"{protocol}://{domain}/verify-email/{uid}/{token}/"
    
    # Send email (will use Celery if available)
    result = send_email_task(
        user_id=user.id,
        email_type="verification",
        verification_url=verification_url
    )
    
    return bool(result)