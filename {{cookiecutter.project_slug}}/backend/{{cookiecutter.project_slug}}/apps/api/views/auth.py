"""
Authentication views.
"""
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
{% if cookiecutter.api_authentication == 'jwt' -%}
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
{% elif cookiecutter.api_authentication == 'token' -%}
from rest_framework.authtoken.models import Token
{%- endif %}

from {{ cookiecutter.project_slug }}.apps.users.models import User
from {{ cookiecutter.project_slug }}.apps.users.utils import (
    email_verification_token,
    generate_verification_token,
    send_verification_email_to_user
)
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
        
        # Send verification email
        send_verification_email_to_user(user, request)
        
        {% if cookiecutter.api_authentication == 'jwt' -%}
        refresh = RefreshToken.for_user(user)
        data = {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'message': 'Registration successful! Please check your email to verify your account.',
            'email_verification_required': True
        }
        {% elif cookiecutter.api_authentication == 'token' -%}
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Registration successful! Please check your email to verify your account.',
            'email_verification_required': True
        }
        {% else -%}
        data = {
            'user': UserSerializer(user).data,
            'message': 'Registration successful! Please check your email to verify your account.',
            'email_verification_required': True
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
            # Check if email is verified
            if not user.is_verified:
                return Response({
                    'error': 'Email not verified',
                    'message': 'Please verify your email address before logging in.',
                    'email_verification_required': True,
                    'email': user.email
                }, status=status.HTTP_403_FORBIDDEN)
            
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


class VerifyEmailView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, uidb64, token):
        """
        Verify email with GET request (for email links).
        """
        return self.verify_email(uidb64, token)
    
    def post(self, request, uidb64, token):
        """
        Verify email with POST request (for frontend forms).
        """
        return self.verify_email(uidb64, token)
    
    def verify_email(self, uidb64, token):
        """
        Verify user's email address.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Invalid verification link',
                'message': 'The verification link is invalid or has expired.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_verified:
            return Response({
                'message': 'Email already verified',
                'already_verified': True
            }, status=status.HTTP_200_OK)
        
        if email_verification_token.check_token(user, token):
            user.is_verified = True
            user.save()
            
            # Send welcome email
            from {{ cookiecutter.project_slug }}.apps.users.tasks import send_email_task
            send_email_task(user_id=user.id, email_type="welcome")
            
            return Response({
                'message': 'Email verified successfully!',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid or expired token',
                'message': 'The verification link is invalid or has expired. Please request a new one.'
            }, status=status.HTTP_400_BAD_REQUEST)


class ResendVerificationEmailView(APIView):
    """
    Resend verification email endpoint.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Resend verification email to user.
        """
        email = request.data.get('email')
        
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({
                'message': 'If an account exists with this email, a verification email has been sent.'
            }, status=status.HTTP_200_OK)
        
        if user.is_verified:
            return Response({
                'message': 'Email is already verified',
                'already_verified': True
            }, status=status.HTTP_200_OK)
        
        # Send verification email
        send_verification_email_to_user(user, request)
        
        return Response({
            'message': 'Verification email has been sent. Please check your inbox.'
        }, status=status.HTTP_200_OK)