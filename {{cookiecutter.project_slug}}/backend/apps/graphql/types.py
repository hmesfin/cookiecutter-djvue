"""GraphQL type definitions."""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    """User GraphQL type."""
    is_complete_profile = graphene.Boolean()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 
                 'is_active', 'date_joined', 'created_at', 'updated_at',
                 'phone_number', 'bio', 'avatar', 'date_of_birth', 'is_verified']
        filter_fields = {
            'email': ['exact', 'icontains'],
            'username': ['exact', 'icontains'],
            'is_active': ['exact'],
            'is_verified': ['exact'],
        }
        interfaces = (graphene.relay.Node,)
    
    def resolve_is_complete_profile(self, info):
        """Resolve the is_complete_profile property."""
        return self.is_complete_profile