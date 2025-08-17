{% if cookiecutter.use_social_auth == 'y' -%}
"""Social authentication URL configuration."""
from django.urls import path
from . import views

app_name = 'social_auth'

urlpatterns = [
    # Provider list
    path('providers/', views.social_auth_providers, name='providers'),
    
    # Social login endpoints
    {% if 'google' in cookiecutter.social_auth_providers -%}
    path('google/', views.GoogleLogin.as_view(), name='google_login'),
    {% endif -%}
    {% if 'github' in cookiecutter.social_auth_providers -%}
    path('github/', views.GitHubLogin.as_view(), name='github_login'),
    {% endif -%}
    {% if 'facebook' in cookiecutter.social_auth_providers -%}
    path('facebook/', views.FacebookLogin.as_view(), name='facebook_login'),
    {% endif -%}
    {% if 'twitter' in cookiecutter.social_auth_providers -%}
    path('twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    {% endif -%}
    
    # Account management
    path('accounts/', views.SocialAccountListView.as_view(), name='social_accounts'),
    path('accounts/<str:provider>/disconnect/', views.SocialAccountDisconnectView.as_view(), name='disconnect'),
]
{%- endif %}