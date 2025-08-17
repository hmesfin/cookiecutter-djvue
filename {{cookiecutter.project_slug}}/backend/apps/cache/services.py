"""Advanced caching services and utilities."""
import hashlib
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps
from django.core.cache import cache, caches
from django.conf import settings
from django.utils import timezone
from django.db.models import Model, QuerySet
from django.http import HttpRequest
import redis

logger = logging.getLogger(__name__)


class CacheService:
    """Advanced cache service with multiple strategies."""
    
    def __init__(self, cache_alias: str = 'default'):
        """Initialize cache service.
        
        Args:
            cache_alias: Name of the cache backend to use
        """
        self.cache = caches[cache_alias]
        self.redis_client = self._get_redis_client()
    
    def _get_redis_client(self) -> Optional[redis.Redis]:
        """Get Redis client if available."""
        try:
            from django_redis import get_redis_connection
            return get_redis_connection("default")
        except Exception:
            return None
    
    def make_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments.
        
        Args:
            *args: Positional arguments to include in key
            **kwargs: Keyword arguments to include in key
        
        Returns:
            Hashed cache key
        """
        key_parts = [str(arg) for arg in args]
        key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
        key_string = ":".join(key_parts)
        
        # Hash long keys to avoid key length limits
        if len(key_string) > 200:
            key_hash = hashlib.md5(key_string.encode()).hexdigest()
            return f"hashed:{key_hash}"
        
        return key_string
    
    def get_or_set(
        self,
        key: str,
        callable_or_value: Union[Callable, Any],
        timeout: Optional[int] = None,
        version: Optional[int] = None,
    ) -> Any:
        """Get from cache or set if not exists.
        
        Args:
            key: Cache key
            callable_or_value: Value or callable to generate value
            timeout: Cache timeout in seconds
            version: Cache key version
        
        Returns:
            Cached or computed value
        """
        value = self.cache.get(key, version=version)
        
        if value is None:
            if callable(callable_or_value):
                value = callable_or_value()
            else:
                value = callable_or_value
            
            if value is not None:
                self.cache.set(key, value, timeout=timeout, version=version)
        
        return value
    
    def invalidate_pattern(self, pattern: str):
        """Invalidate all cache keys matching pattern.
        
        Args:
            pattern: Pattern to match (supports * wildcard)
        """
        if self.redis_client:
            # Use Redis SCAN for efficient pattern matching
            cursor = 0
            while True:
                cursor, keys = self.redis_client.scan(
                    cursor, match=pattern, count=100
                )
                if keys:
                    self.redis_client.delete(*keys)
                if cursor == 0:
                    break
        else:
            # Fallback for non-Redis backends
            logger.warning(f"Pattern invalidation not supported for non-Redis backend")
    
    def invalidate_tags(self, tags: List[str]):
        """Invalidate cache entries by tags.
        
        Args:
            tags: List of tags to invalidate
        """
        for tag in tags:
            tag_key = f"tag:{tag}"
            keys = self.cache.get(tag_key, [])
            
            if keys:
                self.cache.delete_many(keys)
                self.cache.delete(tag_key)
    
    def set_with_tags(
        self,
        key: str,
        value: Any,
        tags: List[str],
        timeout: Optional[int] = None,
    ):
        """Set cache value with tags for group invalidation.
        
        Args:
            key: Cache key
            value: Value to cache
            tags: List of tags for this entry
            timeout: Cache timeout in seconds
        """
        self.cache.set(key, value, timeout=timeout)
        
        # Store key under each tag
        for tag in tags:
            tag_key = f"tag:{tag}"
            tagged_keys = self.cache.get(tag_key, [])
            if key not in tagged_keys:
                tagged_keys.append(key)
                self.cache.set(tag_key, tagged_keys, timeout=86400)  # 24 hours


class QuerySetCache:
    """Cache for Django QuerySets with automatic invalidation."""
    
    def __init__(self, model: Model, cache_service: Optional[CacheService] = None):
        """Initialize QuerySet cache.
        
        Args:
            model: Django model class
            cache_service: CacheService instance
        """
        self.model = model
        self.cache_service = cache_service or CacheService()
        self.model_name = model._meta.label_lower.replace('.', '_')
    
    def get_or_set(
        self,
        queryset: QuerySet,
        key_suffix: str = "",
        timeout: int = 300,
    ) -> List[Model]:
        """Cache QuerySet results.
        
        Args:
            queryset: QuerySet to cache
            key_suffix: Additional key suffix
            timeout: Cache timeout in seconds
        
        Returns:
            List of model instances
        """
        # Generate cache key from query SQL
        query_hash = hashlib.md5(str(queryset.query).encode()).hexdigest()
        cache_key = f"qs:{self.model_name}:{query_hash}:{key_suffix}"
        
        def fetch_data():
            return list(queryset)
        
        return self.cache_service.get_or_set(
            cache_key,
            fetch_data,
            timeout=timeout
        )
    
    def invalidate_model(self):
        """Invalidate all cache entries for this model."""
        pattern = f"qs:{self.model_name}:*"
        self.cache_service.invalidate_pattern(pattern)


class ViewCache:
    """Cache decorator for Django views."""
    
    @staticmethod
    def cache_page(
        timeout: int = 60,
        key_prefix: str = "",
        vary_on_headers: List[str] = None,
        vary_on_cookies: List[str] = None,
    ):
        """Cache entire view response.
        
        Args:
            timeout: Cache timeout in seconds
            key_prefix: Prefix for cache key
            vary_on_headers: Headers to include in cache key
            vary_on_cookies: Cookies to include in cache key
        
        Returns:
            Decorated view function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(request: HttpRequest, *args, **kwargs):
                # Build cache key
                cache_service = CacheService()
                key_parts = [key_prefix, request.path, request.method]
                
                # Add header variations
                if vary_on_headers:
                    for header in vary_on_headers:
                        value = request.META.get(f"HTTP_{header.upper()}", "")
                        key_parts.append(f"{header}:{value}")
                
                # Add cookie variations
                if vary_on_cookies:
                    for cookie in vary_on_cookies:
                        value = request.COOKIES.get(cookie, "")
                        key_parts.append(f"cookie_{cookie}:{value}")
                
                cache_key = cache_service.make_key(*key_parts)
                
                # Try to get from cache
                response = cache.get(cache_key)
                if response is not None:
                    return response
                
                # Generate response
                response = func(request, *args, **kwargs)
                
                # Cache successful responses only
                if hasattr(response, 'status_code') and response.status_code == 200:
                    cache.set(cache_key, response, timeout=timeout)
                
                return response
            
            return wrapper
        return decorator
    
    @staticmethod
    def cache_control(
        private: bool = False,
        public: bool = False,
        no_cache: bool = False,
        no_store: bool = False,
        max_age: Optional[int] = None,
        s_maxage: Optional[int] = None,
        must_revalidate: bool = False,
    ):
        """Set Cache-Control headers on response.
        
        Args:
            private: Set Cache-Control: private
            public: Set Cache-Control: public
            no_cache: Set Cache-Control: no-cache
            no_store: Set Cache-Control: no-store
            max_age: Set max-age value
            s_maxage: Set s-maxage value
            must_revalidate: Set must-revalidate
        
        Returns:
            Decorated view function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(request: HttpRequest, *args, **kwargs):
                response = func(request, *args, **kwargs)
                
                directives = []
                
                if private:
                    directives.append("private")
                elif public:
                    directives.append("public")
                
                if no_cache:
                    directives.append("no-cache")
                if no_store:
                    directives.append("no-store")
                if must_revalidate:
                    directives.append("must-revalidate")
                
                if max_age is not None:
                    directives.append(f"max-age={max_age}")
                if s_maxage is not None:
                    directives.append(f"s-maxage={s_maxage}")
                
                if directives:
                    response["Cache-Control"] = ", ".join(directives)
                
                return response
            
            return wrapper
        return decorator


class APICacheMiddleware:
    """Middleware for automatic API response caching."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache_service = CacheService()
    
    def __call__(self, request):
        # Only cache GET requests to API endpoints
        if request.method == "GET" and request.path.startswith("/api/"):
            cache_key = self._make_cache_key(request)
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache hit for {request.path}")
                return cached_response
        
        response = self.get_response(request)
        
        # Cache successful GET API responses
        if (
            request.method == "GET"
            and request.path.startswith("/api/")
            and hasattr(response, 'status_code')
            and response.status_code == 200
        ):
            timeout = self._get_cache_timeout(request.path)
            cache.set(cache_key, response, timeout=timeout)
            logger.debug(f"Cached response for {request.path}")
        
        return response
    
    def _make_cache_key(self, request):
        """Generate cache key for request."""
        key_parts = [
            "api_cache",
            request.path,
            request.GET.urlencode(),
        ]
        
        # Include user ID for authenticated requests
        if hasattr(request, 'user') and request.user.is_authenticated:
            key_parts.append(f"user:{request.user.id}")
        
        return self.cache_service.make_key(*key_parts)
    
    def _get_cache_timeout(self, path: str) -> int:
        """Get cache timeout based on endpoint.
        
        Args:
            path: Request path
        
        Returns:
            Timeout in seconds
        """
        # Define custom timeouts for specific endpoints
        timeout_map = {
            "/api/config/": 3600,  # 1 hour for config
            "/api/products/": 300,  # 5 minutes for products
            "/api/users/me/": 60,  # 1 minute for user profile
        }
        
        for pattern, timeout in timeout_map.items():
            if path.startswith(pattern):
                return timeout
        
        return 60  # Default 1 minute


# Convenience decorators
def cache_result(timeout: int = 300, key_prefix: str = ""):
    """Cache function results decorator.
    
    Args:
        timeout: Cache timeout in seconds
        key_prefix: Prefix for cache key
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_service = CacheService()
            
            # Build cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
            
            cache_key = cache_service.make_key(*key_parts)
            
            return cache_service.get_or_set(
                cache_key,
                lambda: func(*args, **kwargs),
                timeout=timeout
            )
        
        return wrapper
    return decorator


def invalidate_cache(patterns: List[str] = None, tags: List[str] = None):
    """Invalidate cache entries.
    
    Args:
        patterns: List of key patterns to invalidate
        tags: List of tags to invalidate
    """
    cache_service = CacheService()
    
    if patterns:
        for pattern in patterns:
            cache_service.invalidate_pattern(pattern)
    
    if tags:
        cache_service.invalidate_tags(tags)


# Cache warming utilities
class CacheWarmer:
    """Utilities for warming cache."""
    
    @staticmethod
    def warm_queryset_cache(model: Model, querysets: List[QuerySet]):
        """Pre-populate cache with QuerySet results.
        
        Args:
            model: Django model class
            querysets: List of QuerySets to cache
        """
        qs_cache = QuerySetCache(model)
        
        for queryset in querysets:
            qs_cache.get_or_set(queryset)
            logger.info(f"Warmed cache for {model.__name__} queryset")
    
    @staticmethod
    def warm_api_endpoints(endpoints: List[str]):
        """Pre-populate cache for API endpoints.
        
        Args:
            endpoints: List of endpoint URLs to warm
        """
        from django.test import Client
        
        client = Client()
        
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    logger.info(f"Warmed cache for {endpoint}")
                else:
                    logger.warning(f"Failed to warm cache for {endpoint}: {response.status_code}")
            except Exception as e:
                logger.error(f"Error warming cache for {endpoint}: {str(e)}")