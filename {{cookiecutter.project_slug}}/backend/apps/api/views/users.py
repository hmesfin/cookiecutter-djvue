"""
User views.
"""
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import User
from ..serializers.users import UserSerializer, UserUpdateSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User viewset for listing and retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter out inactive users.
        """
        return super().get_queryset().filter(is_active=True)
    
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """
        Follow a user.
        """
        # Implement follow logic here
        return Response({'status': 'following'})
    
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """
        Unfollow a user.
        """
        # Implement unfollow logic here
        return Response({'status': 'unfollowed'})


class CurrentUserView(RetrieveUpdateAPIView):
    """
    Get or update the current user.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer