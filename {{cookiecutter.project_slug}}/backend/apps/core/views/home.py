"""
Home view for the application.
"""
import platform
from datetime import datetime, timedelta

from django.shortcuts import render
from django.conf import settings
from django.db import connection
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
import django

{% if cookiecutter.use_redis == 'y' -%}
from django.core.cache import cache
{%- endif %}

{% if cookiecutter.use_celery == 'y' -%}
try:
    from {{ cookiecutter.project_slug }}.celery import app as celery_app
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    celery_app = None
{%- endif %}

User = get_user_model()


@cache_page(60)  # Cache for 1 minute
def home_view(request):
    """
    Display API backend status and information.
    """
    # Get environment
    environment = "Production" if not settings.DEBUG else "Development"
    
    # Get Django version
    django_version = django.get_version()
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        database_status = "✅ Connected"
    except Exception:
        database_status = "❌ Disconnected"
    
    {% if cookiecutter.use_redis == 'y' -%}
    # Check cache status
    try:
        cache.set("health_check", "ok", 1)
        if cache.get("health_check") == "ok":
            cache_status = "✅ Connected"
        else:
            cache_status = "⚠️ Issues"
    except Exception:
        cache_status = "❌ Disconnected"
    {% else -%}
    cache_status = "N/A"
    {%- endif %}
    
    {% if cookiecutter.use_celery == 'y' -%}
    # Check Celery status
    if CELERY_AVAILABLE:
        try:
            # Check if celery workers are available
            inspect = celery_app.control.inspect()
            stats = inspect.stats()
            if stats:
                celery_status = f"✅ {len(stats)} worker(s)"
            else:
                celery_status = "⚠️ No workers"
        except Exception:
            celery_status = "❌ Disconnected"
    else:
        celery_status = "Not configured"
    {% else -%}
    celery_status = "N/A"
    {%- endif %}
    
    # Get recent users count
    try:
        recent_users = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=30)
        ).count()
    except Exception:
        recent_users = 0
    
    # API stats
    api_version = "v1"
    uptime = datetime.now()
    
    context = {
        "project_name": "{{ cookiecutter.project_name }}",
        "environment": environment,
        "debug": settings.DEBUG,
        "django_version": django_version,
        "python_version": platform.python_version(),
        "database_status": database_status,
        "cache_status": cache_status,
        {% if cookiecutter.use_celery == 'y' -%}
        "celery_status": celery_status,
        {%- endif %}
        "api_version": api_version,
        "recent_users": recent_users,
        "server_time": timezone.now().isoformat(),
        "timezone": str(timezone.get_current_timezone()),
    }
    
    # Return JSON response for API calls
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse(context)
    
    # Return HTML template for browser access
    return render(request, "home.html", context)