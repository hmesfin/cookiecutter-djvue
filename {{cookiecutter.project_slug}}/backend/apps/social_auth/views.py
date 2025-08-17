{% if cookiecutter.use_social_auth == 'y' -%}
"""Social authentication views."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.social_serializers import TwitterLoginSerializer

from .serializers import SocialAccountSerializer, ConnectSocialAccountSerializer


# Social Login Views for each provider
{% if 'google' in cookiecutter.social_auth_providers -%}
class GoogleLogin(SocialLoginView):
    """Google OAuth2 login."""
    adapter_class = GoogleOAuth2Adapter
    # Callback URL will be configured in OAuth app settings
    client_class = None  # OAuth2Client can be used if needed
{% endif %}

{% if 'github' in cookiecutter.social_auth_providers -%}
class GitHubLogin(SocialLoginView):
    """GitHub OAuth2 login."""
    adapter_class = GitHubOAuth2Adapter
    # Callback URL will be configured in OAuth app settings
    client_class = None
{% endif %}

{% if 'facebook' in cookiecutter.social_auth_providers -%}
class FacebookLogin(SocialLoginView):
    """Facebook OAuth2 login."""
    adapter_class = FacebookOAuth2Adapter
    # Callback URL will be configured in OAuth app settings
    client_class = None
{% endif %}

{% if 'twitter' in cookiecutter.social_auth_providers -%}
class TwitterLogin(SocialLoginView):
    """Twitter OAuth login."""
    adapter_class = TwitterOAuthAdapter
    serializer_class = TwitterLoginSerializer
    # Callback URL will be configured in OAuth app settings
    client_class = None
{% endif %}


class SocialAccountListView(APIView):
    """List user's connected social accounts."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get list of connected social accounts."""
        social_accounts = SocialAccount.objects.filter(user=request.user)
        serializer = SocialAccountSerializer(social_accounts, many=True)
        return Response(serializer.data)


class SocialAccountDisconnectView(APIView):
    """Disconnect a social account."""
    
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, provider):
        """Disconnect social account by provider."""
        try:
            social_account = SocialAccount.objects.get(
                user=request.user,
                provider=provider
            )
            
            # Check if user has other login methods
            has_usable_password = request.user.has_usable_password()
            other_social_accounts = SocialAccount.objects.filter(
                user=request.user
            ).exclude(provider=provider).exists()
            
            if not has_usable_password and not other_social_accounts:
                return Response(
                    {"error": "Cannot disconnect the only login method. Please set a password first."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            social_account.delete()
            
            return Response(
                {"message": f"Successfully disconnected {provider} account."},
                status=status.HTTP_200_OK
            )
            
        except SocialAccount.DoesNotExist:
            return Response(
                {"error": f"No {provider} account connected."},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def social_auth_providers(request):
    """Return list of available social auth providers."""
    providers = [
        {% for provider in cookiecutter.social_auth_providers.split(',') -%}
        {
            "id": "{{ provider.strip() }}",
            "name": "{{ provider.strip().title() }}",
            "auth_url": f"{request.build_absolute_uri('/api/auth/social/')}{{ provider.strip() }}/",
        },
        {% endfor -%}
    ]
    
    return Response({"providers": providers})
{%- endif %}