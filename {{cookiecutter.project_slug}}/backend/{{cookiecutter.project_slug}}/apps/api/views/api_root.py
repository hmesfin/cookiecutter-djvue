"""
API root view showing available endpoints.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def APIRootView(request, format=None):
    """
    API Root - Lists all available API endpoints.
    
    This is the entry point for the {{ cookiecutter.project_name }} API.
    Browse the available endpoints below to explore the API functionality.
    """
    endpoints = {
        "description": "{{ cookiecutter.project_name }} API v{{ cookiecutter.version }}",
        "endpoints": {
            "authentication": {
                {% if cookiecutter.api_authentication == 'jwt' -%}
                "login": reverse("api:login", request=request, format=format),
                "logout": reverse("api:logout", request=request, format=format),
                "register": reverse("api:register", request=request, format=format),
                "refresh": reverse("api:token_refresh", request=request, format=format),
                {% elif cookiecutter.api_authentication == 'token' -%}
                "login": reverse("api:login", request=request, format=format),
                "logout": reverse("api:logout", request=request, format=format),
                "register": reverse("api:register", request=request, format=format),
                {% else -%}
                "login": request.build_absolute_uri("/api/auth/login/"),
                "logout": request.build_absolute_uri("/api/auth/logout/"),
                {%- endif %}
            },
            "user": {
                "current_user": reverse("api:current_user", request=request, format=format),
                "users_list": reverse("api:user-list", request=request, format=format),
            },
            {% if cookiecutter.use_drf_spectacular == 'y' -%}
            "documentation": {
                "schema": reverse("schema", request=request, format=format),
                "swagger": reverse("swagger-ui", request=request, format=format),
                "redoc": reverse("redoc", request=request, format=format),
            },
            {%- endif %}
            "health": {
                "health_check": reverse("health_check", request=request, format=format),
            }
        },
        "info": {
            "version": "{{ cookiecutter.version }}",
            "environment": "production" if not request.META.get("DEBUG", False) else "development",
            "authentication": "{% if cookiecutter.api_authentication == 'jwt' %}JWT Bearer Token{% elif cookiecutter.api_authentication == 'token' %}Token Authentication{% else %}Session Authentication{% endif %}",
            {% if cookiecutter.api_authentication == 'jwt' -%}
            "auth_header": "Authorization: Bearer <access_token>",
            {% elif cookiecutter.api_authentication == 'token' -%}
            "auth_header": "Authorization: Token <token>",
            {%- endif %}
        }
    }
    
    return Response(endpoints)