"""
Health check views for monitoring.
"""
import time
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.core.cache import cache
{% if cookiecutter.use_redis == 'y' -%}
import redis
from django.conf import settings
{%- endif %}


class HealthCheckView(View):
    """
    Basic health check endpoint for load balancers and monitoring.
    Returns 200 if the application is running.
    """
    
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'timestamp': int(time.time())
        })


class DetailedHealthCheckView(View):
    """
    Detailed health check that verifies all critical components.
    Should be protected and used only for internal monitoring.
    """
    
    def get(self, request):
        health_status = {
            'status': 'healthy',
            'timestamp': int(time.time()),
            'checks': {}
        }
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            health_status['checks']['database'] = {
                'status': 'healthy',
                'response_time_ms': 0
            }
        except Exception as e:
            health_status['status'] = 'unhealthy'
            health_status['checks']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        # Check cache
        try:
            cache_key = 'health_check_test'
            cache.set(cache_key, 'test', 1)
            cache.get(cache_key)
            cache.delete(cache_key)
            health_status['checks']['cache'] = {
                'status': 'healthy'
            }
        except Exception as e:
            health_status['status'] = 'degraded'
            health_status['checks']['cache'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        {% if cookiecutter.use_redis == 'y' -%}
        # Check Redis connection
        try:
            redis_url = settings.REDIS_URL
            r = redis.from_url(redis_url)
            r.ping()
            health_status['checks']['redis'] = {
                'status': 'healthy'
            }
        except Exception as e:
            health_status['status'] = 'degraded'
            health_status['checks']['redis'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        {%- endif %}
        
        # Check disk space
        try:
            import shutil
            import os
            
            stat = shutil.disk_usage("/")
            free_gb = stat.free / (1024 ** 3)
            total_gb = stat.total / (1024 ** 3)
            used_percent = ((stat.total - stat.free) / stat.total) * 100
            
            disk_status = 'healthy'
            if used_percent > 90:
                disk_status = 'critical'
                health_status['status'] = 'degraded'
            elif used_percent > 80:
                disk_status = 'warning'
            
            health_status['checks']['disk'] = {
                'status': disk_status,
                'free_gb': round(free_gb, 2),
                'total_gb': round(total_gb, 2),
                'used_percent': round(used_percent, 2)
            }
        except Exception as e:
            health_status['checks']['disk'] = {
                'status': 'unknown',
                'error': str(e)
            }
        
        # Check memory usage
        try:
            import psutil
            
            memory = psutil.virtual_memory()
            memory_status = 'healthy'
            if memory.percent > 90:
                memory_status = 'critical'
                health_status['status'] = 'degraded'
            elif memory.percent > 80:
                memory_status = 'warning'
            
            health_status['checks']['memory'] = {
                'status': memory_status,
                'percent_used': memory.percent,
                'available_mb': round(memory.available / (1024 ** 2), 2)
            }
        except ImportError:
            # psutil not installed
            health_status['checks']['memory'] = {
                'status': 'unknown',
                'note': 'psutil not installed'
            }
        except Exception as e:
            health_status['checks']['memory'] = {
                'status': 'unknown',
                'error': str(e)
            }
        
        # Return appropriate status code
        status_code = 200
        if health_status['status'] == 'unhealthy':
            status_code = 503
        elif health_status['status'] == 'degraded':
            status_code = 200  # Still return 200 for degraded to keep service in rotation
        
        return JsonResponse(health_status, status=status_code)


class LivenessProbeView(View):
    """
    Kubernetes liveness probe endpoint.
    Returns 200 if the application is alive and can serve requests.
    """
    
    def get(self, request):
        # Simple check - if we can respond, we're alive
        return JsonResponse({'status': 'alive'})


class ReadinessProbeView(View):
    """
    Kubernetes readiness probe endpoint.
    Returns 200 if the application is ready to serve traffic.
    """
    
    def get(self, request):
        # Check if critical components are ready
        try:
            # Check database
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            # Check cache
            cache.set('readiness_check', 'ready', 1)
            cache.get('readiness_check')
            
            return JsonResponse({'status': 'ready'})
        except Exception as e:
            return JsonResponse({
                'status': 'not_ready',
                'error': str(e)
            }, status=503)