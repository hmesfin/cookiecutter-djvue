"""
Tests for user tasks.
"""
{% if cookiecutter.use_pytest == 'y' -%}
import pytest
from unittest.mock import patch, MagicMock
from django.core import mail
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.apps.users.tasks import (
    send_welcome_email,
    send_verification_email,
    send_password_reset_email,
    send_email_task,
)

User = get_user_model()


@pytest.mark.django_db
class TestEmailTasks:
    """Test email tasks work both with and without Celery."""
    
    def test_send_welcome_email_sync(self):
        """Test welcome email sends synchronously."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        # Clear any emails from signal
        mail.outbox = []
        
        # Send email synchronously
        result = send_welcome_email(user_id=user.id)
        
        assert result is True
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["test@example.com"]
        assert "Welcome" in mail.outbox[0].subject
    
    def test_send_welcome_email_invalid_user(self):
        """Test handling of invalid user ID."""
        result = send_welcome_email(user_id=99999)
        assert result is False
    
    def test_send_verification_email_sync(self):
        """Test verification email sends synchronously."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        mail.outbox = []
        
        verification_url = "http://example.com/verify/token"
        result = send_verification_email(
            user_id=user.id,
            verification_url=verification_url
        )
        
        assert result is True
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["test@example.com"]
        assert "Verify" in mail.outbox[0].subject
        assert verification_url in mail.outbox[0].body
    
    def test_send_verification_email_already_verified(self):
        """Test that verified users don't get verification emails."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        user.is_verified = True
        user.save()
        
        mail.outbox = []
        
        result = send_verification_email(
            user_id=user.id,
            verification_url="http://example.com/verify"
        )
        
        assert result is True
        assert len(mail.outbox) == 0  # No email sent
    
    def test_send_password_reset_email_sync(self):
        """Test password reset email sends synchronously."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        mail.outbox = []
        
        reset_url = "http://example.com/reset/token"
        result = send_password_reset_email(
            user_id=user.id,
            reset_url=reset_url
        )
        
        assert result is True
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["test@example.com"]
        assert "Reset" in mail.outbox[0].subject
        assert reset_url in mail.outbox[0].body
    
    {% if cookiecutter.use_celery == 'y' -%}
    @patch('{{ cookiecutter.project_slug }}.apps.users.tasks.CELERY_AVAILABLE', True)
    @patch('{{ cookiecutter.project_slug }}.apps.users.tasks.send_welcome_email.delay')
    def test_send_email_task_with_celery(self, mock_delay, settings):
        """Test that emails are queued with Celery when available."""
        settings.USE_CELERY = True
        settings.CELERY_TASK_ALWAYS_EAGER = False
        
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        mock_delay.return_value = MagicMock(id="task-123")
        
        result = send_email_task(user_id=user.id, email_type="welcome")
        
        mock_delay.assert_called_once_with(user_id=user.id)
        assert hasattr(result, 'id')
    
    @patch('{{ cookiecutter.project_slug }}.apps.users.tasks.CELERY_AVAILABLE', False)
    def test_send_email_task_without_celery(self):
        """Test that emails are sent synchronously when Celery is not available."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        mail.outbox = []
        
        result = send_email_task(user_id=user.id, email_type="welcome")
        
        assert result is True
        assert len(mail.outbox) == 1
    {%- endif %}
    
    def test_send_email_task_invalid_type(self):
        """Test handling of invalid email type."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        result = send_email_task(user_id=user.id, email_type="invalid")
        assert result is False
    
    @patch('{{ cookiecutter.project_slug }}.apps.users.tasks.send_mail')
    def test_email_failure_handling(self, mock_send_mail):
        """Test that email failures are handled gracefully."""
        mock_send_mail.side_effect = Exception("SMTP error")
        
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        result = send_welcome_email(user_id=user.id)
        assert result is False
{% else -%}
from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.apps.users.tasks import (
    send_welcome_email,
    send_email_task,
)

User = get_user_model()


class TestEmailTasks(TestCase):
    """Test email tasks."""
    
    def test_send_welcome_email_sync(self):
        """Test welcome email sends synchronously."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        # Clear any emails from signal
        mail.outbox = []
        
        # Send email synchronously
        result = send_welcome_email(user_id=user.id)
        
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["test@example.com"])
        self.assertIn("Welcome", mail.outbox[0].subject)
    
    def test_send_email_task(self):
        """Test email task helper."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        
        mail.outbox = []
        
        result = send_email_task(user_id=user.id, email_type="welcome")
        
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
{%- endif %}