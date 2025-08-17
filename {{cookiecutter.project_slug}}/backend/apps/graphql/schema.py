"""GraphQL schema definition."""
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile
from apps.graphql.auth import login_required

User = get_user_model()


# Types
class UserType(DjangoObjectType):
    """User GraphQL type."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'is_active', 'date_joined', 'profile']
        filter_fields = {
            'email': ['exact', 'icontains'],
            'username': ['exact', 'icontains'],
            'is_active': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class UserProfileType(DjangoObjectType):
    """UserProfile GraphQL type."""
    
    class Meta:
        model = UserProfile
        fields = '__all__'


# Input Types
class UserInput(graphene.InputObjectType):
    """Input type for user creation/update."""
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()


class UserProfileInput(graphene.InputObjectType):
    """Input type for user profile update."""
    bio = graphene.String()
    avatar = graphene.String()
    phone_number = graphene.String()
    date_of_birth = graphene.Date()


# Queries
class Query(graphene.ObjectType):
    """Root query object."""
    
    # Single object queries
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    
    # List queries with pagination
    all_users = DjangoFilterConnectionField(UserType)
    
    # Custom queries
    search_users = graphene.List(
        UserType,
        query=graphene.String(required=True),
        limit=graphene.Int(default_value=10)
    )
    
    @login_required
    def resolve_me(self, info):
        """Get current authenticated user."""
        return info.context.user
    
    @login_required
    def resolve_user(self, info, id):
        """Get user by ID."""
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
    
    @login_required
    def resolve_all_users(self, info, **kwargs):
        """Get all users with filtering."""
        return User.objects.filter(is_active=True)
    
    @login_required
    def resolve_search_users(self, info, query, limit):
        """Search users by email or username."""
        from django.db.models import Q
        
        return User.objects.filter(
            Q(email__icontains=query) | 
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).filter(is_active=True)[:limit]


# Mutations
class CreateUser(graphene.Mutation):
    """Create a new user."""
    
    class Arguments:
        user_data = UserInput(required=True)
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    def mutate(self, info, user_data):
        """Create user mutation."""
        errors = []
        
        # Validate unique fields
        if User.objects.filter(email=user_data.email).exists():
            errors.append("Email already exists")
        if User.objects.filter(username=user_data.username).exists():
            errors.append("Username already exists")
        
        if errors:
            return CreateUser(user=None, success=False, errors=errors)
        
        try:
            user = User.objects.create_user(
                email=user_data.email,
                username=user_data.username,
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
                password=user_data.get('password', 'defaultpass123')
            )
            
            return CreateUser(user=user, success=True, errors=[])
        except Exception as e:
            return CreateUser(user=None, success=False, errors=[str(e)])


class UpdateUser(graphene.Mutation):
    """Update user information."""
    
    class Arguments:
        id = graphene.ID(required=True)
        user_data = UserInput(required=True)
    
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, id, user_data):
        """Update user mutation."""
        try:
            user = User.objects.get(pk=id)
            
            # Check permissions
            if info.context.user != user and not info.context.user.is_staff:
                return UpdateUser(
                    user=None, 
                    success=False, 
                    errors=["Permission denied"]
                )
            
            # Update fields
            for field, value in user_data.items():
                if field != 'password' and value is not None:
                    setattr(user, field, value)
            
            # Handle password separately
            if user_data.get('password'):
                user.set_password(user_data.password)
            
            user.save()
            
            return UpdateUser(user=user, success=True, errors=[])
        except User.DoesNotExist:
            return UpdateUser(
                user=None, 
                success=False, 
                errors=["User not found"]
            )
        except Exception as e:
            return UpdateUser(
                user=None, 
                success=False, 
                errors=[str(e)]
            )


class UpdateProfile(graphene.Mutation):
    """Update user profile."""
    
    class Arguments:
        profile_data = UserProfileInput(required=True)
    
    profile = graphene.Field(UserProfileType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)
    
    @login_required
    def mutate(self, info, profile_data):
        """Update profile mutation."""
        try:
            profile = info.context.user.profile
            
            # Update fields
            for field, value in profile_data.items():
                if value is not None:
                    setattr(profile, field, value)
            
            profile.save()
            
            return UpdateProfile(profile=profile, success=True, errors=[])
        except Exception as e:
            return UpdateProfile(
                profile=None, 
                success=False, 
                errors=[str(e)]
            )


class DeleteUser(graphene.Mutation):
    """Delete (deactivate) a user."""
    
    class Arguments:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()
    
    @login_required
    def mutate(self, info, id):
        """Delete user mutation."""
        try:
            user = User.objects.get(pk=id)
            
            # Check permissions
            if info.context.user != user and not info.context.user.is_superuser:
                return DeleteUser(
                    success=False, 
                    message="Permission denied"
                )
            
            # Soft delete (deactivate)
            user.is_active = False
            user.save()
            
            return DeleteUser(
                success=True, 
                message="User deactivated successfully"
            )
        except User.DoesNotExist:
            return DeleteUser(success=False, message="User not found")


class Mutation(graphene.ObjectType):
    """Root mutation object."""
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    update_profile = UpdateProfile.Field()
    delete_user = DeleteUser.Field()


# Create schema
schema = graphene.Schema(query=Query, mutation=Mutation)