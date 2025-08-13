"""
API URL configuration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
{% if cookiecutter.api_authentication == 'jwt' -%}
from rest_framework_simplejwt.views import TokenRefreshView
from .views.auth import (
    LoginView, 
    LogoutView, 
    RegisterView,
    VerifyEmailView,
    ResendVerificationEmailView
)
{% elif cookiecutter.api_authentication == 'token' -%}
from .views.auth import (
    LoginView, 
    LogoutView, 
    RegisterView,
    VerifyEmailView,
    ResendVerificationEmailView
)
{% else -%}
from .views.auth import (
    VerifyEmailView,
    ResendVerificationEmailView
)
{%- endif %}
from .views.users import UserViewSet, CurrentUserView
from .views import APIRootView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = 'api'

urlpatterns = [
    # API Root
    path('', APIRootView, name='api-root'),
    
    # Authentication
    {% if cookiecutter.api_authentication == 'jwt' -%}
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),
    {% elif cookiecutter.api_authentication == 'token' -%}
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),
    {% else -%}
    path('auth/', include('rest_framework.urls')),
    path('auth/verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),
    {%- endif %}
    
    # Current user
    path('me/', CurrentUserView.as_view(), name='current_user'),
    
    # Router URLs
    path('', include(router.urls)),
]