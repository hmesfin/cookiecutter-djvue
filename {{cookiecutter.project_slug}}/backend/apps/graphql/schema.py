"""GraphQL schema definition using Strawberry."""
import strawberry
from typing import List, Optional
from django.contrib.auth import get_user_model
from django.db.models import Q
from strawberry.types import Info

from apps.graphql.types import UserType, UserInput, MutationResult
from apps.graphql.auth import AuthMutations, login_required

User = get_user_model()


@strawberry.type
class Query:
    """Root query object."""
    
    @strawberry.field
    def me(self, info: Info) -> Optional[UserType]:
        """Get current authenticated user."""
        user = info.context.request.user
        if user.is_authenticated:
            return user
        return None
    
    @strawberry.django.field
    def user(self, info: Info, id: int) -> Optional[UserType]:
        """Get user by ID."""
        try:
            return User.objects.get(pk=id, is_active=True)
        except User.DoesNotExist:
            return None
    
    @strawberry.django.field
    def users(
        self,
        info: Info,
        search: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[UserType]:
        """Get all users with optional search."""
        queryset = User.objects.filter(is_active=True)
        
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return list(queryset[offset:offset + limit])
    
    @strawberry.field
    def user_count(self, info: Info) -> int:
        """Get total number of active users."""
        return User.objects.filter(is_active=True).count()


@strawberry.type
class UserMutations:
    """User-related mutations."""
    
    @strawberry.mutation
    def create_user(self, info: Info, input: UserInput) -> UserType:
        """Create a new user (admin only)."""
        if not info.context.request.user.is_staff:
            raise Exception("Permission denied")
        
        # Validate unique fields
        if User.objects.filter(email=input.email).exists():
            raise Exception("Email already exists")
        if User.objects.filter(username=input.username).exists():
            raise Exception("Username already exists")
        
        user = User.objects.create_user(
            email=input.email,
            username=input.username,
            first_name=input.first_name or '',
            last_name=input.last_name or '',
            password=input.password or 'defaultpass123'
        )
        
        return user
    
    @strawberry.mutation
    @login_required
    def update_user(
        self,
        info: Info,
        id: int,
        input: UserInput
    ) -> UserType:
        """Update user information."""
        try:
            user = User.objects.get(pk=id)
            
            # Check permissions
            if info.context.request.user != user and not info.context.request.user.is_staff:
                raise Exception("Permission denied")
            
            # Update fields
            user.email = input.email
            user.username = input.username
            if input.first_name is not None:
                user.first_name = input.first_name
            if input.last_name is not None:
                user.last_name = input.last_name
            
            # Handle password separately
            if input.password:
                user.set_password(input.password)
            
            user.save()
            return user
        except User.DoesNotExist:
            raise Exception("User not found")
    
    @strawberry.mutation
    @login_required
    def delete_user(self, info: Info, id: int) -> MutationResult:
        """Delete (deactivate) a user."""
        try:
            user = User.objects.get(pk=id)
            
            # Check permissions
            if info.context.request.user != user and not info.context.request.user.is_superuser:
                return MutationResult(
                    success=False,
                    message="Permission denied"
                )
            
            # Soft delete (deactivate)
            user.is_active = False
            user.save()
            
            return MutationResult(
                success=True,
                message="User deactivated successfully"
            )
        except User.DoesNotExist:
            return MutationResult(
                success=False,
                message="User not found"
            )


@strawberry.type
class Mutation(AuthMutations, UserMutations):
    """Root mutation object combining all mutations."""
    pass


# Create the schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        # Add any Strawberry extensions here
    ]
)