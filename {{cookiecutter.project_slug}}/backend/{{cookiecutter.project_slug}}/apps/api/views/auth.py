"""
Authentication views.
"""
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
{% if cookiecutter.api_authentication == 'jwt' -%}
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
{% elif cookiecutter.api_authentication == 'token' -%}
from rest_framework.authtoken.models import Token
{%- endif %}

from {{ cookiecutter.project_slug }}.apps.users.models import User
from ..serializers.auth import LoginSerializer, RegisterSerializer
from ..serializers.users import UserSerializer


class RegisterView(CreateAPIView):
    """
    User registration endpoint.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        {% if cookiecutter.api_authentication == 'jwt' -%}
        refresh = RefreshToken.for_user(user)
        data = {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        {% elif cookiecutter.api_authentication == 'token' -%}
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'user': UserSerializer(user).data,
            'token': token.key,
        }
        {% else -%}
        data = {
            'user': UserSerializer(user).data,
        }
        {%- endif %}
        
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    """
    User login endpoint.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user:
            {% if cookiecutter.api_authentication == 'jwt' -%}
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
            {% elif cookiecutter.api_authentication == 'token' -%}
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user': UserSerializer(user).data,
                'token': token.key,
            }
            {% else -%}
            data = {
                'user': UserSerializer(user).data,
            }
            {%- endif %}
            
            return Response(data, status=status.HTTP_200_OK)
        
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(GenericAPIView):
    """
    User logout endpoint.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        {% if cookiecutter.api_authentication == 'jwt' -%}
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except TokenError:
            pass
        {% elif cookiecutter.api_authentication == 'token' -%}
        try:
            request.user.auth_token.delete()
        except:
            pass
        {%- endif %}
        
        return Response(
            {'detail': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )