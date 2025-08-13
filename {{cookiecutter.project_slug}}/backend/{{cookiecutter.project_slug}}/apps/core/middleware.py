"""
Custom middleware for the application.
"""
import time
import logging
from django.utils import timezone
from django.core.cache import cache

logger = logging.getLogger(__name__)


class APIMetricsMiddleware:
    """
    Middleware to track API metrics like request count and response times.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Track API calls
        if request.path.startswith('/api/'):
            # Increment daily API counter
            today = timezone.now().date()
            cache_key = f"api_calls_{today}"
            
            try:
                current_count = cache.get(cache_key, 0)
                cache.set(cache_key, current_count + 1, 86400)  # Expire after 24 hours
            except Exception:
                pass  # Fail silently if cache is not available
            
            # Track response time
            start_time = time.time()
        
        response = self.get_response(request)
        
        # Log response time for API calls
        if request.path.startswith('/api/'):
            duration = time.time() - start_time
            logger.info(
                f"API Request: {request.method} {request.path} "
                f"Status: {response.status_code} "
                f"Duration: {duration:.3f}s"
            )
        
        return response


class HealthCheckMiddleware:
    """
    Middleware to skip authentication for health check endpoints.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip authentication for health check
        if request.path == '/api/health/':
            request.skip_auth = True
        
        response = self.get_response(request)
        return response