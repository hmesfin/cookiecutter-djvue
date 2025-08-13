"""
Core views for the application.
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
    from celery import current_app as celery_app
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
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
    celery_status = "Not configured"
    {%- endif %}
    
    # Get user statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Get API calls from cache (tracked by middleware)
    try:
        today = timezone.now().date()
        cache_key = f"api_calls_{today}"
        api_calls_count = cache.get(cache_key, 0)
        
        # Format the count nicely
        if api_calls_count >= 1000000:
            api_calls_today = f"{api_calls_count / 1000000:.1f}M"
        elif api_calls_count >= 1000:
            api_calls_today = f"{api_calls_count / 1000:.1f}k"
        else:
            api_calls_today = str(api_calls_count)
    except Exception:
        api_calls_today = "N/A"
    
    # Calculate uptime (since server start - simplified)
    try:
        # Get the creation time of the first user or use current time minus 1 day
        first_user = User.objects.first()
        if first_user:
            start_time = first_user.created_at
        else:
            start_time = timezone.now() - timedelta(days=1)
        
        uptime_delta = timezone.now() - start_time
        days = uptime_delta.days
        hours = uptime_delta.seconds // 3600
        
        if days > 0:
            uptime = f"{days}d {hours}h"
        else:
            uptime = f"{hours}h"
    except Exception:
        uptime = "N/A"
    
    context = {
        "environment": environment,
        "django_version": django_version,
        "database_status": database_status,
        "cache_status": cache_status,
        "celery_status": celery_status,
        "total_users": total_users,
        "active_users": active_users,
        "api_calls_today": api_calls_today,
        "uptime": uptime,
    }
    
    return render(request, "home.html", context)


def health_check_view(request):
    """
    Health check endpoint for monitoring services.
    Returns JSON response with service status.
    """
    health_data = {
        "status": "healthy",
        "timestamp": timezone.now().isoformat(),
        "services": {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_data["services"]["database"] = "healthy"
    except Exception as e:
        health_data["services"]["database"] = "unhealthy"
        health_data["status"] = "degraded"
    
    {% if cookiecutter.use_redis == 'y' -%}
    # Check Redis
    try:
        cache.set("health_check_test", "ok", 1)
        if cache.get("health_check_test") == "ok":
            health_data["services"]["cache"] = "healthy"
        else:
            health_data["services"]["cache"] = "unhealthy"
            health_data["status"] = "degraded"
    except Exception:
        health_data["services"]["cache"] = "unhealthy"
        health_data["status"] = "degraded"
    {%- endif %}
    
    {% if cookiecutter.use_celery == 'y' -%}
    # Check Celery
    if CELERY_AVAILABLE:
        try:
            inspect = celery_app.control.inspect()
            stats = inspect.stats()
            if stats:
                health_data["services"]["celery"] = "healthy"
                health_data["services"]["celery_workers"] = len(stats)
            else:
                health_data["services"]["celery"] = "unhealthy"
                health_data["status"] = "degraded"
        except Exception:
            health_data["services"]["celery"] = "unhealthy"
            health_data["status"] = "degraded"
    {%- endif %}
    
    # Add system info
    health_data["system"] = {
        "django_version": django.get_version(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }
    
    # Return appropriate status code
    status_code = 200 if health_data["status"] == "healthy" else 503
    
    return JsonResponse(health_data, status=status_code)