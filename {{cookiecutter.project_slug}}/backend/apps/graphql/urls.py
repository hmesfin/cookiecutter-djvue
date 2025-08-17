"""GraphQL URL configuration."""
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import PublicGraphQLView, graphql_playground

app_name = 'graphql'

urlpatterns = [
    path('', csrf_exempt(PublicGraphQLView.as_view(graphiql=False)), name='graphql'),
    path('playground/', graphql_playground, name='playground'),
]