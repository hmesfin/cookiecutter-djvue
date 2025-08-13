"""
Token generators for email verification and password reset.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for email verification links.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Create a hash value including the user's verification status.
        This ensures the token is invalidated once the email is verified.
        """
        return (
            six.text_type(user.pk) + 
            six.text_type(timestamp) + 
            six.text_type(user.is_verified) +
            six.text_type(user.email)
        )


# Create instances to be imported
email_verification_token = EmailVerificationTokenGenerator()