"""GraphQL URL configuration."""
from django.urls import path
from .views import public_graphql_view, private_graphql_view, graphql_playground

app_name = 'graphql'

urlpatterns = [
    path('', public_graphql_view, name='graphql'),
    path('private/', private_graphql_view, name='graphql-private'),
    path('playground/', graphql_playground, name='playground'),
]