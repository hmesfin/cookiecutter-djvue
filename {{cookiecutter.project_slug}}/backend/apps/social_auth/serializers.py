{% if cookiecutter.use_social_auth == 'y' -%}
"""Social authentication serializers."""
from rest_framework import serializers
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.serializers import SocialLoginSerializer


class SocialAuthSerializer(SocialLoginSerializer):
    """Custom social authentication serializer."""
    
    provider = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        """Add custom validation if needed."""
        attrs = super().validate(attrs)
        return attrs


class SocialAccountSerializer(serializers.ModelSerializer):
    """Serializer for social account details."""
    
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SocialAccount
        fields = ['id', 'provider', 'provider_display', 'uid', 'avatar_url', 'date_joined']
        read_only_fields = fields
    
    def get_avatar_url(self, obj):
        """Extract avatar URL from social account data."""
        extra_data = obj.extra_data or {}
        
        # Different providers store avatar URLs differently
        if obj.provider == 'google':
            return extra_data.get('picture')
        elif obj.provider == 'github':
            return extra_data.get('avatar_url')
        elif obj.provider == 'facebook':
            picture_data = extra_data.get('picture', {})
            if isinstance(picture_data, dict):
                return picture_data.get('data', {}).get('url')
        elif obj.provider == 'twitter':
            return extra_data.get('profile_image_url_https')
        
        return None


class ConnectSocialAccountSerializer(serializers.Serializer):
    """Serializer for connecting a social account to existing user."""
    
    access_token = serializers.CharField(required=True)
    provider = serializers.ChoiceField(
        choices=[
            {% for provider in cookiecutter.social_auth_providers.split(',') -%}
            ('{{ provider.strip() }}', '{{ provider.strip().title() }}'),
            {% endfor -%}
        ]
    )
{%- endif %}