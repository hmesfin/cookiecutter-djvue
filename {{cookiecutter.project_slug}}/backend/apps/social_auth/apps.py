{% if cookiecutter.use_social_auth == 'y' -%}
from django.apps import AppConfig


class SocialAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.social_auth'
    verbose_name = 'Social Authentication'
{%- endif %}