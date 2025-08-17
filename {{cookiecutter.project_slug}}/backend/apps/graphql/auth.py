"""GraphQL authentication schema."""
import graphene
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from functools import wraps
from apps.graphql.types import UserType

User = get_user_model()


def login_required(func):
    """Decorator to require authentication for GraphQL resolvers."""
    @wraps(func)
    def wrapper(root, info, *args, **kwargs):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise Exception("Authentication required")
        return func(root, info, *args, **kwargs)
    return wrapper


def create_token(user):
    """Create JWT token for user."""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def create_refresh_token(user):
    """Create refresh token for user."""
    payload = {
        'user_id': user.id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class ObtainJSONWebToken(graphene.Mutation):
    """JWT token mutation."""
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(UserType)
    
    def mutate(self, info, email, password):
        """Authenticate and return tokens."""
        user = authenticate(email=email, password=password)
        if not user:
            raise Exception("Invalid credentials")
        
        return ObtainJSONWebToken(
            token=create_token(user),
            refresh_token=create_refresh_token(user),
            user=user
        )


class RegisterUser(graphene.Mutation):
    """Register a new user."""
    
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
    
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, email, username, password, **kwargs):
        """Register user mutation."""
        errors = []
        
        # Validate
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered")
        if User.objects.filter(username=username).exists():
            errors.append("Username already taken")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        
        if errors:
            return RegisterUser(
                user=None,
                token=None,
                refresh_token=None,
                success=False,
                errors=errors
            )
        
        try:
            # Create user
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=kwargs.get('first_name', ''),
                last_name=kwargs.get('last_name', '')
            )
            
            # Generate tokens
            token = create_token(user)
            refresh_token = create_refresh_token(user)
            
            return RegisterUser(
                user=user,
                token=token,
                refresh_token=refresh_token,
                success=True,
                errors=[]
            )
        except Exception as e:
            return RegisterUser(
                user=None,
                token=None,
                refresh_token=None,
                success=False,
                errors=[str(e)]
            )


class ChangePassword(graphene.Mutation):
    """Change user password."""
    
    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @login_required
    def mutate(self, info, old_password, new_password):
        """Change password mutation."""
        user = info.context.user
        
        if not user.check_password(old_password):
            return ChangePassword(
                success=False,
                message="Invalid old password"
            )
        
        if len(new_password) < 8:
            return ChangePassword(
                success=False,
                message="Password must be at least 8 characters"
            )
        
        user.set_password(new_password)
        user.save()
        
        return ChangePassword(
            success=True,
            message="Password changed successfully"
        )


class RequestPasswordReset(graphene.Mutation):
    """Request password reset email."""
    
    class Arguments:
        email = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, email):
        """Request password reset mutation."""
        try:
            user = User.objects.get(email=email)
            
            # Send password reset email
            from apps.emails.services import send_password_reset_email
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"http://localhost:5173/reset-password/{uid}/{token}"
            
            send_password_reset_email(user, reset_url)
            
            return RequestPasswordReset(
                success=True,
                message="Password reset email sent"
            )
        except User.DoesNotExist:
            # Don't reveal if email exists
            return RequestPasswordReset(
                success=True,
                message="If the email exists, a reset link has been sent"
            )


class ResetPassword(graphene.Mutation):
    """Reset password with token."""
    
    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, uid, token, new_password):
        """Reset password mutation."""
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        
        try:
            # Decode user ID
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
            
            # Verify token
            if not default_token_generator.check_token(user, token):
                return ResetPassword(
                    success=False,
                    message="Invalid or expired token"
                )
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            return ResetPassword(
                success=True,
                message="Password reset successfully"
            )
        except (User.DoesNotExist, ValueError, TypeError):
            return ResetPassword(
                success=False,
                message="Invalid reset link"
            )


class VerifyToken(graphene.Mutation):
    """Verify JWT token."""
    class Arguments:
        token = graphene.String(required=True)
    
    valid = graphene.Boolean()
    user = graphene.Field(UserType)
    
    def mutate(self, info, token):
        """Verify token mutation."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            return VerifyToken(valid=True, user=user)
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            return VerifyToken(valid=False, user=None)


class RefreshToken(graphene.Mutation):
    """Refresh JWT token."""
    class Arguments:
        refresh_token = graphene.String(required=True)
    
    token = graphene.String()
    refresh_token = graphene.String()
    
    def mutate(self, info, refresh_token):
        """Refresh token mutation."""
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('type') != 'refresh':
                raise Exception("Invalid token type")
            
            user = User.objects.get(id=payload['user_id'])
            return RefreshToken(
                token=create_token(user),
                refresh_token=create_refresh_token(user)
            )
        except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
            raise Exception("Invalid refresh token")


class AuthMutation(graphene.ObjectType):
    """Authentication mutations."""
    token_auth = ObtainJSONWebToken.Field()
    verify_token = VerifyToken.Field()
    refresh_token = RefreshToken.Field()
    
    register = RegisterUser.Field()
    change_password = ChangePassword.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()