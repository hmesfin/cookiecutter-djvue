"""
User serializers.
"""
from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'bio', 'avatar', 'date_of_birth',
            'is_verified', 'is_staff', 'date_joined', 'last_login'
        )
        read_only_fields = ('id', 'is_verified', 'is_staff', 'date_joined', 'last_login')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating User model.
    """
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone_number', 'bio',
            'avatar', 'date_of_birth'
        )