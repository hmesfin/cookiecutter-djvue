"""GraphQL app configuration."""
from django.apps import AppConfig


class GraphQLConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.graphql'
    verbose_name = 'GraphQL API'