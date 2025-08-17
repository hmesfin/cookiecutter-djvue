"""
Tests for User model and manager.
"""
{% if cookiecutter.use_pytest == 'y' -%}
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


@pytest.mark.django_db
class TestUserManager:
    """Test custom UserManager methods."""
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.check_password("testpass123")
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_verified
        assert user.is_active
    
    def test_create_user_without_email(self):
        """Test that creating a user without email raises error."""
        with pytest.raises(ValueError, match="Email field must be set"):
            User.objects.create_user(
                email=None,
                username="testuser",
                password="testpass123"
            )
    
    def test_create_user_auto_username(self):
        """Test that username is auto-generated from email if not provided."""
        user = User.objects.create_user(
            email="john.doe@example.com",
            password="testpass123"
        )
        assert user.username == "john.doe"
    
    def test_create_user_unique_auto_username(self):
        """Test that auto-generated username is unique."""
        user1 = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        user2 = User.objects.create_user(
            email="test@different.com",
            password="testpass123"
        )
        assert user1.username == "test"
        assert user2.username == "test1"
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass123"
        )
        assert user.email == "admin@example.com"
        assert user.username == "admin"
        assert user.check_password("adminpass123")
        assert user.is_staff
        assert user.is_superuser
        assert user.is_verified
        assert user.is_active
    
    def test_get_by_email(self):
        """Test getting user by email (case-insensitive)."""
        user = User.objects.create_user(
            email="Test@Example.com",
            password="testpass123"
        )
        found_user = User.objects.get_by_email("test@example.com")
        assert found_user.id == user.id
    
    def test_active_queryset(self):
        """Test active() queryset method."""
        active_user = User.objects.create_user(
            email="active@example.com",
            password="testpass123"
        )
        inactive_user = User.objects.create_user(
            email="inactive@example.com",
            password="testpass123"
        )
        inactive_user.is_active = False
        inactive_user.save()
        
        active_users = User.objects.active()
        assert active_user in active_users
        assert inactive_user not in active_users
    
    def test_verified_queryset(self):
        """Test verified() queryset method."""
        verified_user = User.objects.create_user(
            email="verified@example.com",
            password="testpass123"
        )
        verified_user.is_verified = True
        verified_user.save()
        
        unverified_user = User.objects.create_user(
            email="unverified@example.com",
            password="testpass123"
        )
        
        verified_users = User.objects.verified()
        assert verified_user in verified_users
        assert unverified_user not in verified_users


@pytest.mark.django_db
class TestUserModel:
    """Test User model methods and properties."""
    
    def test_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        assert str(user) == "test@example.com"
    
    def test_get_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        assert user.get_full_name() == "John Doe"
    
    def test_get_full_name_fallback(self):
        """Test get_full_name fallback to username/email."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        assert user.get_full_name() == "testuser"
    
    def test_get_short_name(self):
        """Test get_short_name method."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John"
        )
        assert user.get_short_name() == "John"
    
    def test_get_short_name_fallback(self):
        """Test get_short_name fallback to username."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        assert user.get_short_name() == "testuser"
    
    def test_is_complete_profile(self):
        """Test is_complete_profile property."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        assert not user.is_complete_profile
        
        user.first_name = "John"
        user.last_name = "Doe"
        user.phone_number = "+1234567890"
        user.date_of_birth = "1990-01-01"
        user.save()
        
        assert user.is_complete_profile
    
    def test_email_uniqueness(self):
        """Test that email must be unique."""
        User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="test@example.com",
                username="different",
                password="testpass123"
            )
    
    def test_avatar_upload_path(self):
        """Test avatar upload path includes date folders."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        from datetime import datetime
        date = datetime.now()
        expected_path = f"avatars/{date.year}/{date.month:02d}/{date.day:02d}/"
        assert expected_path in user.avatar.field.upload_to
{% else -%}
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class TestUserManager(TestCase):
    """Test custom UserManager methods."""
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)
        self.assertTrue(user.is_active)
    
    def test_create_user_without_email(self):
        """Test that creating a user without email raises error."""
        with self.assertRaisesMessage(ValueError, "Email field must be set"):
            User.objects.create_user(
                email=None,
                username="testuser",
                password="testpass123"
            )
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpass123"
        )
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.username, "admin")
        self.assertTrue(user.check_password("adminpass123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_verified)
        self.assertTrue(user.is_active)


class TestUserModel(TestCase):
    """Test User model methods and properties."""
    
    def test_str_representation(self):
        """Test string representation of user."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(str(user), "test@example.com")
    
    def test_get_full_name(self):
        """Test get_full_name method."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.get_full_name(), "John Doe")
    
    def test_is_complete_profile(self):
        """Test is_complete_profile property."""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.assertFalse(user.is_complete_profile)
        
        user.first_name = "John"
        user.last_name = "Doe"
        user.phone_number = "+1234567890"
        user.date_of_birth = "1990-01-01"
        user.save()
        
        self.assertTrue(user.is_complete_profile)
{%- endif %}