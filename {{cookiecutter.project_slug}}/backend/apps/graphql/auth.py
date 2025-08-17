"""GraphQL authentication schema."""
import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth import get_user_model
from apps.graphql.schema import UserType

User = get_user_model()


class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    """Custom JWT token mutation with user data."""
    user = graphene.Field(UserType)
    
    @classmethod
    def resolve(cls, root, info, **kwargs):
        """Add user to response."""
        return cls(user=info.context.user)


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
            from graphql_jwt.shortcuts import get_token, get_refresh_token
            token = get_token(user)
            refresh_token = get_refresh_token(user)
            
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


class AuthMutation(graphene.ObjectType):
    """Authentication mutations."""
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    
    register = RegisterUser.Field()
    change_password = ChangePassword.Field()
    request_password_reset = RequestPasswordReset.Field()
    reset_password = ResetPassword.Field()