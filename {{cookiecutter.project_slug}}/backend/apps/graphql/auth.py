"""GraphQL authentication with Strawberry."""
import jwt
import strawberry
from datetime import datetime, timedelta
from typing import Optional, List
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from strawberry.types import Info
from functools import wraps

from apps.graphql.types import (
    UserType, AuthPayload, MutationResult,
    LoginInput, RegisterInput, UserProfileInput
)

User = get_user_model()


def login_required(func):
    """Decorator to require authentication for GraphQL resolvers."""
    @wraps(func)
    def wrapper(self, info: Info, *args, **kwargs):
        user = info.context.request.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")
        return func(self, info, *args, **kwargs)
    return wrapper


def create_token(user) -> str:
    """Create JWT token for user."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def create_refresh_token(user) -> str:
    """Create refresh token for user."""
    payload = {
        'user_id': user.id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> Optional[User]:
    """Verify JWT token and return user."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
        return None


@strawberry.type
class AuthMutations:
    """Authentication mutations."""
    
    @strawberry.mutation
    def login(self, info: Info, input: LoginInput) -> AuthPayload:
        """Authenticate user and return tokens."""
        user = authenticate(
            request=info.context.request,
            email=input.email,
            password=input.password
        )
        if not user:
            raise Exception("Invalid credentials")
        
        return AuthPayload(
            user=user,
            token=create_token(user),
            refresh_token=create_refresh_token(user)
        )
    
    @strawberry.mutation
    def register(self, info: Info, input: RegisterInput) -> AuthPayload:
        """Register a new user."""
        # Validate
        if User.objects.filter(email=input.email).exists():
            raise Exception("Email already registered")
        if User.objects.filter(username=input.username).exists():
            raise Exception("Username already taken")
        if len(input.password) < 8:
            raise Exception("Password must be at least 8 characters")
        
        # Create user
        user = User.objects.create_user(
            email=input.email,
            username=input.username,
            password=input.password,
            first_name=input.first_name or '',
            last_name=input.last_name or ''
        )
        
        # Send welcome email if configured
        if getattr(settings, 'SEND_WELCOME_EMAIL', True):
            try:
                from apps.emails.services import send_welcome_email
                send_welcome_email(user)
            except ImportError:
                pass
        
        return AuthPayload(
            user=user,
            token=create_token(user),
            refresh_token=create_refresh_token(user)
        )
    
    @strawberry.mutation
    @login_required
    def change_password(
        self,
        info: Info,
        old_password: str,
        new_password: str
    ) -> MutationResult:
        """Change user password."""
        user = info.context.request.user
        
        if not user.check_password(old_password):
            return MutationResult(
                success=False,
                message="Invalid old password"
            )
        
        if len(new_password) < 8:
            return MutationResult(
                success=False,
                message="Password must be at least 8 characters"
            )
        
        user.set_password(new_password)
        user.save()
        
        return MutationResult(
            success=True,
            message="Password changed successfully"
        )
    
    @strawberry.mutation
    def request_password_reset(self, info: Info, email: str) -> MutationResult:
        """Request password reset email."""
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Send password reset email
            try:
                from apps.emails.services import send_password_reset_email
                frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
                reset_url = f"{frontend_url}/reset-password/{uid}/{token}"
                send_password_reset_email(user, reset_url)
            except ImportError:
                pass
            
            return MutationResult(
                success=True,
                message="Password reset email sent"
            )
        except User.DoesNotExist:
            # Don't reveal if email exists
            return MutationResult(
                success=True,
                message="If the email exists, a reset link has been sent"
            )
    
    @strawberry.mutation
    def reset_password(
        self,
        info: Info,
        uid: str,
        token: str,
        new_password: str
    ) -> MutationResult:
        """Reset password with token."""
        try:
            # Decode user ID
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            
            # Verify token
            if not default_token_generator.check_token(user, token):
                return MutationResult(
                    success=False,
                    message="Invalid or expired token"
                )
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            return MutationResult(
                success=True,
                message="Password reset successfully"
            )
        except (User.DoesNotExist, ValueError, TypeError):
            return MutationResult(
                success=False,
                message="Invalid reset link"
            )
    
    @strawberry.mutation
    def verify_token(self, info: Info, token: str) -> Optional[UserType]:
        """Verify JWT token and return user."""
        user = verify_token(token)
        return user if user else None
    
    @strawberry.mutation
    def refresh_token(self, info: Info, refresh_token: str) -> AuthPayload:
        """Refresh JWT token."""
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                raise Exception("Invalid token type")
            
            user = User.objects.get(id=payload['user_id'])
            return AuthPayload(
                user=user,
                token=create_token(user),
                refresh_token=create_refresh_token(user)
            )
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise Exception("Invalid refresh token")
    
    @strawberry.mutation
    @login_required
    def update_profile(
        self,
        info: Info,
        input: UserProfileInput
    ) -> UserType:
        """Update user profile."""
        user = info.context.request.user
        
        # Update fields
        if input.first_name is not None:
            user.first_name = input.first_name
        if input.last_name is not None:
            user.last_name = input.last_name
        if input.bio is not None:
            user.bio = input.bio
        if input.phone_number is not None:
            user.phone_number = input.phone_number
        if input.date_of_birth is not None:
            user.date_of_birth = input.date_of_birth
        
        user.save()
        return user