"""
Custom managers for User model.
"""
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        if not username:
            raise ValueError(_("The Username field must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_verified", False)
        
        # If username is not provided, use email prefix as username
        if username is None:
            username = email.split("@")[0]
            # Ensure username is unique
            base_username = username
            counter = 1
            while self.model.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
        
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        # If username is not provided, use email prefix as username
        if username is None:
            username = email.split("@")[0]
            # For superuser, add _admin suffix if username exists
            if self.model.objects.filter(username=username).exists():
                username = f"{username}_admin"

        return self._create_user(email, username, password, **extra_fields)

    def get_by_email(self, email):
        """
        Get a user by email address.
        """
        return self.get(email__iexact=email)

    def active(self):
        """
        Return only active users.
        """
        return self.filter(is_active=True)

    def verified(self):
        """
        Return only verified users.
        """
        return self.filter(is_verified=True)