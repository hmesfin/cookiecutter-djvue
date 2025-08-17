# Caching Strategy Guide

## Overview

This application implements a comprehensive multi-layer caching strategy to optimize performance and reduce server load.

## Backend Caching

### Cache Backends

The application uses multiple cache backends for different purposes:

1. **Default Cache** - Redis-based cache for general application data
2. **Session Cache** - Dedicated Redis database for session storage
3. **Static Cache** - Local memory cache for static content

### Configuration

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 300,  # 5 minutes default
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
    },
    'static': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600,  # 1 hour
    }
}
```

### Using the Cache Service

```python
from apps.cache.services import CacheService, cache_result

# Initialize cache service
cache = CacheService()

# Basic get/set operations
cache.set('my_key', 'my_value', timeout=300)
value = cache.get('my_key')

# Get or set pattern
result = cache.get_or_set(
    'expensive_operation',
    lambda: expensive_computation(),
    timeout=600
)

# Cache function results
@cache_result(timeout=300)
def expensive_function(param1, param2):
    # Expensive computation
    return result

# Invalidate cache patterns
cache.invalidate_pattern('user:*')  # Clear all user cache

# Tag-based invalidation
cache.set_with_tags('product:123', product_data, ['products', 'inventory'])
cache.invalidate_tags(['products'])  # Invalidate all product caches
```

### QuerySet Caching

```python
from apps.cache.services import QuerySetCache
from myapp.models import Product

# Create QuerySet cache
qs_cache = QuerySetCache(Product)

# Cache QuerySet results
products = qs_cache.get_or_set(
    Product.objects.filter(active=True),
    key_suffix='active',
    timeout=300
)

# Invalidate all Product queries
qs_cache.invalidate_model()
```

### View Caching

```python
from apps.cache.services import ViewCache

# Cache entire view response
@ViewCache.cache_page(
    timeout=300,
    vary_on_headers=['Accept-Language'],
    vary_on_cookies=['session_id']
)
def my_view(request):
    return render(request, 'template.html')

# Set Cache-Control headers
@ViewCache.cache_control(
    public=True,
    max_age=3600,
    must_revalidate=True
)
def static_view(request):
    return JsonResponse({'data': 'static'})
```

### API Caching Middleware

The `APICacheMiddleware` automatically caches GET requests to API endpoints:

```python
# settings.py
MIDDLEWARE = [
    # ...
    'apps.cache.services.APICacheMiddleware',
    # ...
]
```

Caching rules:
- Only GET requests are cached
- Successful responses (200 OK) are cached
- Cache keys include user ID for authenticated requests
- Different endpoints have different TTLs

### Management Commands

```bash
# Clear all cache
python manage.py cache_clear --all

# Clear by pattern (Redis only)
python manage.py cache_clear --pattern "user:*"

# Warm cache with common data
python manage.py cache_warm --models auth.User core.Product

# Warm specific API endpoints
python manage.py cache_warm --endpoints /api/config/ /api/products/
```

## Frontend Caching

### Cache Service

```javascript
import { cache, memoryCache } from '@/services/cache'

// Set value with TTL
cache.set('user_preferences', preferences, 300000)  // 5 minutes

// Get value
const preferences = cache.get('user_preferences')

// Get or set pattern
const data = await cache.getOrSet(
  'api_data',
  async () => await fetchFromAPI(),
  600000  // 10 minutes
)

// Clear specific key
cache.remove('user_preferences')

// Clear all cache
cache.clear()

// Get cache statistics
const stats = cache.getStats()
console.log(`Cache size: ${stats.sizeInMB}MB`)
```

### Vue Composables

```javascript
import { useCache, useCachedAPI } from '@/composables/useCache'

// Basic cache composable
const { data, loading, fetch, clear } = useCache('my_key', {
  ttl: 300000,
  storage: 'local'  // or 'session' or 'memory'
})

// Cached API calls
const { data, loading, execute, refresh } = useCachedAPI(
  () => api.getProducts(),
  {
    ttl: 600000,
    immediate: true,
    onSuccess: (data) => console.log('Fetched:', data)
  }
)

// Optimistic updates
const { update } = useOptimisticUpdate(
  (data) => api.updateProduct(data),
  {
    cacheKey: 'products',
    optimisticUpdate: (old, update) => ({ ...old, ...update }),
    rollbackOnError: true
  }
)

// Infinite scroll with caching
const { items, loadMore, reset } = useCachedInfiniteScroll(
  ({ page, pageSize }) => api.getItems({ page, pageSize }),
  {
    cacheKey: 'infinite_items',
    pageSize: 20
  }
)
```

### Pinia Store Caching

```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    preferences: {},
    temp: {}  // Won't be cached
  }),
  
  // Cache configuration
  cache: {
    enabled: true,
    ttl: 600000,  // 10 minutes
    paths: ['profile', 'preferences'],  // Only cache these
    exclude: ['temp'],  // Never cache these
    reloadOnError: true
  },
  
  actions: {
    clearCache() {
      this.$cache.clear()
    }
  }
})
```

### API Response Caching

```javascript
import axios from 'axios'
import { APICache } from '@/services/cache'

// Setup API cache interceptor
const apiCache = new APICache(axios, {
  defaultTTL: 300000,
  debug: true
})

// Make cached request
const response = await axios.get('/api/products', {
  cache: true,  // Enable caching
  cacheTTL: 600000  // Custom TTL for this request
})

// Bypass cache
const freshData = await axios.get('/api/products', {
  cache: false  // Bypass cache
})

// Invalidate cached responses
apiCache.invalidate('/api/products')
```

### Service Worker Caching

The service worker implements multiple caching strategies:

1. **Cache First** - For static assets (images, fonts)
2. **Network First** - For API requests
3. **Stale While Revalidate** - For JS/CSS files

```javascript
// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(reg => console.log('SW registered'))
    .catch(err => console.error('SW registration failed'))
}

// Control service worker from app
navigator.serviceWorker.controller.postMessage({
  type: 'CLEAR_CACHE'
})

// Cache specific URLs
navigator.serviceWorker.controller.postMessage({
  type: 'CACHE_URLS',
  payload: {
    urls: ['/api/config', '/api/products']
  }
})
```

## Cache Invalidation Strategies

### Time-based Invalidation

- Default TTL of 5 minutes for most data
- Longer TTL for static content (1 hour to 30 days)
- Configurable per cache operation

### Event-based Invalidation

```python
# Backend - Signal-based invalidation
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.cache.services import invalidate_cache

@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    invalidate_cache(
        patterns=[f'product:{instance.id}', 'products:*'],
        tags=['products']
    )
```

```javascript
// Frontend - Mutation-based invalidation
const updateProduct = async (data) => {
  const result = await api.updateProduct(data)
  
  // Invalidate related caches
  cache.remove('products')
  cache.remove(`product:${data.id}`)
  
  return result
}
```

### Manual Invalidation

- Admin interface for cache management
- Management commands for bulk operations
- API endpoints for cache control

## Performance Monitoring

### Backend Metrics

```python
from apps.cache.services import CacheService

cache = CacheService()

# Log cache operations
import logging
logging.getLogger('django.cache').setLevel(logging.DEBUG)

# Monitor cache hit rates
from django.core.cache import cache
from django.core.cache.utils import make_key

hits = cache.get('cache_hits', 0)
misses = cache.get('cache_misses', 0)
hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
```

### Frontend Metrics

```javascript
// Monitor cache performance
const stats = cache.getStats()
console.log('Cache Statistics:', {
  items: stats.count,
  size: `${stats.sizeInMB}MB`,
  expired: stats.expired,
  hitRate: (hits / (hits + misses) * 100).toFixed(2) + '%'
})

// Track cache operations
window.addEventListener('storage', (e) => {
  if (e.key?.startsWith('app_cache_')) {
    console.log('Cache updated:', e.key)
  }
})
```

## Best Practices

### DO's

1. **Use appropriate TTLs** - Balance freshness vs performance
2. **Cache at multiple layers** - Browser, CDN, application, database
3. **Implement cache warming** - Pre-populate cache for common queries
4. **Monitor cache metrics** - Track hit rates and performance
5. **Use cache tags** - Group related cache entries for bulk invalidation
6. **Handle cache failures gracefully** - Always have fallback logic

### DON'Ts

1. **Don't cache sensitive data** - User-specific or security-sensitive information
2. **Don't cache everything** - Some data needs to be real-time
3. **Don't ignore cache size** - Monitor and clean up regularly
4. **Don't forget invalidation** - Stale data is worse than no cache
5. **Don't rely solely on cache** - Always have a data source fallback

## Troubleshooting

### Common Issues

1. **Cache not working**
   ```bash
   # Check Redis connection
   redis-cli ping
   
   # Test cache in Django shell
   python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.set('test', 'value')
   >>> cache.get('test')
   ```

2. **Stale data**
   ```python
   # Force cache clear
   from apps.cache.services import CacheService
   cache = CacheService()
   cache.invalidate_pattern('*')  # Clear all
   ```

3. **Cache size issues**
   ```javascript
   // Check and clear frontend cache
   const stats = cache.getStats()
   if (stats.sizeInMB > 40) {
     cache.cleanup()  // Remove old entries
   }
   ```

4. **Service worker issues**
   ```javascript
   // Unregister and re-register
   navigator.serviceWorker.getRegistrations()
     .then(regs => regs.forEach(reg => reg.unregister()))
   ```

## Advanced Topics

### Cache Warming

```python
# Warm cache on deployment
from apps.cache.services import CacheWarmer
from myapp.models import Product

warmer = CacheWarmer()

# Warm common querysets
warmer.warm_queryset_cache(Product, [
    Product.objects.filter(featured=True),
    Product.objects.filter(on_sale=True),
])

# Warm API endpoints
warmer.warm_api_endpoints([
    '/api/config/',
    '/api/products/featured/',
])
```

### Distributed Caching

For multi-server deployments:

```python
# Use Redis Sentinel for high availability
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            'redis://sentinel1:26379/1',
            'redis://sentinel2:26379/1',
        ],
        'OPTIONS': {
            'CONNECTION_POOL_CLASS': 'redis.sentinel.SentinelConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'master_name': 'mymaster',
            },
        },
    },
}
```

### Cache Compression

```python
# Enable compression for large objects
CACHES = {
    'default': {
        'OPTIONS': {
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'COMPRESSION_LEVEL': 6,  # 1-9, higher = more compression
        },
    },
}
```

## Monitoring and Alerting

### Metrics to Track

1. **Cache hit rate** - Should be > 80% for effective caching
2. **Cache response time** - Should be < 10ms for Redis
3. **Cache size** - Monitor memory usage
4. **Eviction rate** - High evictions indicate memory pressure
5. **Error rate** - Connection failures or timeouts

### Setting up Monitoring

```python
# Django prometheus metrics
from django_prometheus.cache import PrometheusCache

CACHES = {
    'default': {
        'BACKEND': 'django_prometheus.cache.backends.redis.RedisCache',
        # ... rest of config
    },
}
```

```javascript
// Frontend performance monitoring
const monitorCache = () => {
  const stats = cache.getStats()
  
  // Send to analytics
  analytics.track('cache_stats', {
    items: stats.count,
    size_mb: stats.sizeInMB,
    expired: stats.expired
  })
}

// Monitor every 5 minutes
setInterval(monitorCache, 5 * 60 * 1000)
```