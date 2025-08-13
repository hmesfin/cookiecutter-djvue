"""
User models for {{ cookiecutter.project_name }}.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    """
    Custom User model for {{ cookiecutter.project_name }}.
    Email is required and must be unique.
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        blank=True,
        help_text=_("Contact phone number"),
    )
    bio = models.TextField(
        _("biography"),
        blank=True,
        help_text=_("A short bio about the user"),
    )
    avatar = models.ImageField(
        _("avatar"),
        upload_to="avatars/%Y/%m/%d/",
        null=True,
        blank=True,
        help_text=_("User profile picture"),
    )
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether this user has verified their email address."),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )
    
    # Use custom manager
    objects = UserManager()
    
    # Make email required
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]  # Required when creating superuser (username is USERNAME_FIELD by default)
    
    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
            models.Index(fields=["-created_at"]),
        ]
        
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        If no full name is set, return the username or email.
        """
        full_name = super().get_full_name()
        return full_name or self.username or self.email
    
    def get_short_name(self):
        """
        Return the short name for the user.
        If no first name is set, return the username.
        """
        return self.first_name or self.username.split("@")[0]
    
    @property
    def is_complete_profile(self):
        """
        Check if user has completed their profile.
        """
        return all([
            self.first_name,
            self.last_name,
            self.phone_number,
            self.date_of_birth,
        ])