# Testing Cache Implementation

## 1. Backend Cache Testing

### A. Test Redis Connection

```bash
# Check if Redis is running
docker exec -it myproject_backend python manage.py shell

from django.core.cache import cache

# Test basic cache operations
cache.set('test_key', 'test_value', 60)
print(cache.get('test_key'))  # Should print: test_value

# Test cache deletion
cache.delete('test_key')
print(cache.get('test_key'))  # Should print: None
```

### B. Test Cache Service

```python
# In Django shell
from apps.cache.services import CacheService, QuerySetCache
from apps.users.models import User

# Initialize cache service
cache_service = CacheService()

# Test get_or_set
def expensive_operation():
    import time
    time.sleep(2)
    return "expensive result"

# First call should take 2 seconds
import time
start = time.time()
result = cache_service.get_or_set('expensive_key', expensive_operation, timeout=300)
print(f"First call took: {time.time() - start} seconds")

# Second call should be instant (from cache)
start = time.time()
result = cache_service.get_or_set('expensive_key', expensive_operation, timeout=300)
print(f"Second call took: {time.time() - start} seconds")

# Test pattern invalidation
cache_service.set_with_tags('product:1', {'name': 'Product 1'}, ['products'])
cache_service.set_with_tags('product:2', {'name': 'Product 2'}, ['products'])
cache_service.invalidate_tags(['products'])  # Should clear both
```

### C. Test QuerySet Caching

```python
from apps.cache.services import QuerySetCache
from django.contrib.auth import get_user_model

User = get_user_model()

# Create test data
for i in range(5):
    User.objects.create_user(f'user{i}', f'user{i}@example.com', 'pass')

# Test QuerySet caching
qs_cache = QuerySetCache(User)

# First query hits database
import time
start = time.time()
users = qs_cache.get_or_set(User.objects.all(), timeout=60)
print(f"First query: {time.time() - start} seconds")

# Second query hits cache
start = time.time()
users = qs_cache.get_or_set(User.objects.all(), timeout=60)
print(f"Cached query: {time.time() - start} seconds")

# Invalidate model cache
qs_cache.invalidate_model()
```

### D. Test API Response Caching

```bash
# Test API endpoint caching
# First request should be slower
time curl http://localhost:8000/api/users/me/

# Second request should be faster (cached)
time curl http://localhost:8000/api/users/me/

# Check cache headers
curl -I http://localhost:8000/api/users/me/
```

### E. Create Cache Performance Test Script

Create `backend/test_cache_performance.py`:

```python
#!/usr/bin/env python
import os
import django
import sys
import time
import statistics

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.cache import cache
from apps.cache.services import CacheService, QuerySetCache
from django.contrib.auth import get_user_model

User = get_user_model()

def test_cache_performance():
    """Test cache performance metrics."""
    cache_service = CacheService()
    
    print("=" * 50)
    print("CACHE PERFORMANCE TEST")
    print("=" * 50)
    
    # Test 1: Basic cache operations
    print("\n1. Basic Cache Operations")
    times = []
    for i in range(100):
        start = time.perf_counter()
        cache.set(f'test_{i}', f'value_{i}')
        cache.get(f'test_{i}')
        times.append((time.perf_counter() - start) * 1000)
    
    print(f"   Average time: {statistics.mean(times):.2f}ms")
    print(f"   Median time: {statistics.median(times):.2f}ms")
    print(f"   Min/Max: {min(times):.2f}ms / {max(times):.2f}ms")
    
    # Test 2: Cache hit ratio
    print("\n2. Cache Hit Ratio Test")
    hits = 0
    misses = 0
    
    for i in range(100):
        key = f'hit_test_{i % 10}'  # Only 10 unique keys
        if cache.get(key):
            hits += 1
        else:
            misses += 1
            cache.set(key, f'value_{i}', 60)
    
    hit_ratio = (hits / (hits + misses)) * 100
    print(f"   Hits: {hits}, Misses: {misses}")
    print(f"   Hit ratio: {hit_ratio:.1f}%")
    
    # Test 3: Large object caching
    print("\n3. Large Object Caching")
    large_data = {'data': 'x' * 10000}  # ~10KB object
    
    start = time.perf_counter()
    cache.set('large_object', large_data)
    set_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    retrieved = cache.get('large_object')
    get_time = (time.perf_counter() - start) * 1000
    
    print(f"   Set time: {set_time:.2f}ms")
    print(f"   Get time: {get_time:.2f}ms")
    print(f"   Compression working: {len(str(large_data)) > 1000}")
    
    # Test 4: QuerySet caching
    print("\n4. QuerySet Caching")
    qs_cache = QuerySetCache(User)
    
    # Create test users if needed
    if User.objects.count() < 10:
        for i in range(10):
            User.objects.create_user(f'test{i}', f'test{i}@example.com')
    
    # First query (no cache)
    start = time.perf_counter()
    users = list(User.objects.all())
    db_time = (time.perf_counter() - start) * 1000
    
    # Cached query
    start = time.perf_counter()
    users = qs_cache.get_or_set(User.objects.all(), 'all_users', 60)
    first_cache_time = (time.perf_counter() - start) * 1000
    
    # Second cached query
    start = time.perf_counter()
    users = qs_cache.get_or_set(User.objects.all(), 'all_users', 60)
    cached_time = (time.perf_counter() - start) * 1000
    
    print(f"   Database query: {db_time:.2f}ms")
    print(f"   First cache call: {first_cache_time:.2f}ms")
    print(f"   Cached query: {cached_time:.2f}ms")
    print(f"   Speedup: {db_time/cached_time:.1f}x")
    
    # Test 5: Cache invalidation
    print("\n5. Cache Invalidation")
    
    # Set multiple keys with pattern
    for i in range(10):
        cache.set(f'user:{i}', f'data_{i}')
    
    start = time.perf_counter()
    cache_service.invalidate_pattern('user:*')
    invalidate_time = (time.perf_counter() - start) * 1000
    
    # Check if invalidation worked
    remaining = sum(1 for i in range(10) if cache.get(f'user:{i}'))
    
    print(f"   Invalidation time: {invalidate_time:.2f}ms")
    print(f"   Keys remaining: {remaining} (should be 0)")
    
    print("\n" + "=" * 50)
    print("TEST COMPLETE")
    print("=" * 50)

if __name__ == '__main__':
    test_cache_performance()
```

Run it:
```bash
docker exec -it myproject_backend python /app/test_cache_performance.py
```

## 2. Frontend Cache Testing

### A. Test Browser Cache

Open browser DevTools (F12) and check:

1. **Network Tab**:
   - Look for cached responses (304 status)
   - Check Cache-Control headers
   - Monitor response times

2. **Application Tab**:
   - Check Local Storage for cache entries
   - Look for keys starting with `app_cache_`
   - Monitor cache size

### B. Test Cache Service

In browser console:

```javascript
// Import cache service
import { cache, memoryCache } from '@/services/cache'

// Test basic operations
cache.set('test_key', 'test_value', 5000)  // 5 second TTL
console.log(cache.get('test_key'))  // Should log: test_value

// Wait 6 seconds and try again
setTimeout(() => {
  console.log(cache.get('test_key'))  // Should log: null (expired)
}, 6000)

// Test cache statistics
console.log(cache.getStats())

// Test memory cache
memoryCache.set('mem_test', {data: 'test'}, 3000)
console.log(memoryCache.get('mem_test'))

// Test cache cleanup
cache.cleanup()
console.log('Cleanup complete:', cache.getStats())
```

### C. Test Vue Composables

Create `frontend/src/views/CacheTest.vue`:

```vue
<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Cache Testing</h2>
    
    <div class="grid grid-cols-2 gap-4">
      <!-- Cache Status -->
      <div class="card">
        <div class="card-body">
          <h3 class="font-bold mb-2">Cache Status</h3>
          <p>Has Cache: {{ hasCache }}</p>
          <p>Is Stale: {{ isStale }}</p>
          <p>Data: {{ data }}</p>
        </div>
      </div>
      
      <!-- API Cache Test -->
      <div class="card">
        <div class="card-body">
          <h3 class="font-bold mb-2">API Cache Test</h3>
          <button @click="fetchData" class="btn btn-primary mb-2">
            Fetch Data
          </button>
          <button @click="refreshData" class="btn btn-secondary mb-2">
            Force Refresh
          </button>
          <p v-if="loading">Loading...</p>
          <p v-if="apiData">Response time: {{ responseTime }}ms</p>
          <pre v-if="apiData">{{ JSON.stringify(apiData, null, 2) }}</pre>
        </div>
      </div>
      
      <!-- Cache Stats -->
      <div class="card col-span-2">
        <div class="card-body">
          <h3 class="font-bold mb-2">Cache Statistics</h3>
          <pre>{{ JSON.stringify(cacheStats, null, 2) }}</pre>
          <button @click="clearCache" class="btn btn-danger mt-2">
            Clear All Cache
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCache, useCachedAPI } from '@/composables/useCache'
import { cache } from '@/services/cache'
import axios from 'axios'

// Basic cache test
const { data, hasCache, isStale, save, clear } = useCache('test_cache', {
  ttl: 10000  // 10 seconds
})

// API cache test
const responseTime = ref(0)
const apiData = ref(null)
const loading = ref(false)

const fetchData = async () => {
  loading.value = true
  const start = Date.now()
  
  try {
    const response = await axios.get('/api/users/me/', {
      cache: true,
      cacheTTL: 60000  // 1 minute
    })
    apiData.value = response.data
    responseTime.value = Date.now() - start
  } catch (error) {
    console.error('Fetch error:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  const start = Date.now()
  
  try {
    const response = await axios.get('/api/users/me/', {
      cache: false  // Bypass cache
    })
    apiData.value = response.data
    responseTime.value = Date.now() - start
  } catch (error) {
    console.error('Fetch error:', error)
  } finally {
    loading.value = false
  }
}

// Cache statistics
const cacheStats = ref({})

const updateStats = () => {
  cacheStats.value = cache.getStats()
}

const clearCache = () => {
  cache.clear()
  clear()
  updateStats()
}

onMounted(() => {
  // Set some test data
  save({ message: 'Test cache data', timestamp: Date.now() })
  updateStats()
  
  // Update stats every second
  setInterval(updateStats, 1000)
})
</script>
```

### D. Test Service Worker Caching

1. Check Service Worker registration:
```javascript
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(regs => {
    console.log('Service Workers:', regs)
  })
}
```

2. Check cached resources:
```javascript
caches.keys().then(names => {
  console.log('Cache names:', names)
  names.forEach(name => {
    caches.open(name).then(cache => {
      cache.keys().then(keys => {
        console.log(`Cache ${name}:`, keys.map(k => k.url))
      })
    })
  })
})
```

## 3. Cache Performance Monitoring

### Create Monitoring Dashboard

Create `backend/cache_monitor.py`:

```python
#!/usr/bin/env python
"""Cache monitoring script."""
import os
import django
import sys
import time
import json

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.cache import cache
from django_redis import get_redis_connection

def monitor_cache():
    """Monitor cache metrics."""
    redis_conn = get_redis_connection("default")
    
    while True:
        info = redis_conn.info()
        
        metrics = {
            'used_memory': info['used_memory_human'],
            'connected_clients': info['connected_clients'],
            'total_commands': info['total_commands_processed'],
            'keyspace_hits': info.get('keyspace_hits', 0),
            'keyspace_misses': info.get('keyspace_misses', 0),
            'hit_ratio': 0,
            'keys': redis_conn.dbsize(),
        }
        
        if metrics['keyspace_hits'] + metrics['keyspace_misses'] > 0:
            metrics['hit_ratio'] = round(
                metrics['keyspace_hits'] / 
                (metrics['keyspace_hits'] + metrics['keyspace_misses']) * 100, 
                2
            )
        
        print(f"\r{json.dumps(metrics)}", end='')
        time.sleep(1)

if __name__ == '__main__':
    print("Cache Monitor - Press Ctrl+C to exit")
    try:
        monitor_cache()
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
```

Run it:
```bash
docker exec -it myproject_backend python /app/cache_monitor.py
```

## 4. Load Testing Cache

### Using Apache Bench (ab)

```bash
# Test without cache (first run)
ab -n 100 -c 10 http://localhost:8000/api/users/

# Test with cache (subsequent runs should be faster)
ab -n 100 -c 10 http://localhost:8000/api/users/

# Compare response times
```

### Using locust

Create `backend/locustfile.py`:

```python
from locust import HttpUser, task, between

class CacheTestUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def test_cached_endpoint(self):
        self.client.get("/api/users/")
    
    @task(1)
    def test_uncached_endpoint(self):
        self.client.get(f"/api/users/?random={self.random}")
    
    def on_start(self):
        self.random = 0
    
    def on_stop(self):
        self.random += 1
```

Run load test:
```bash
pip install locust
locust -H http://localhost:8000
# Open browser at http://localhost:8089
```

## 5. Testing Checklist

### Backend Cache
- [ ] Redis connection works
- [ ] Cache get/set operations work
- [ ] Cache TTL expiration works
- [ ] Pattern invalidation works
- [ ] Tag-based invalidation works
- [ ] QuerySet caching works
- [ ] API response caching works
- [ ] Cache middleware active
- [ ] Session storage in cache works
- [ ] Cache compression works

### Frontend Cache
- [ ] LocalStorage cache works
- [ ] Memory cache works
- [ ] Cache TTL works
- [ ] Cache cleanup works
- [ ] API response interceptor works
- [ ] Vue composables work
- [ ] Pinia store caching works
- [ ] Service Worker registered
- [ ] Static assets cached
- [ ] Cache statistics accurate

### Performance
- [ ] Cache hit ratio > 80%
- [ ] Response time improved
- [ ] Memory usage acceptable
- [ ] No cache stampede issues
- [ ] Proper cache headers set

## 6. Debugging Commands

```bash
# Check Redis status
docker exec -it myproject_redis redis-cli INFO

# Monitor Redis commands in real-time
docker exec -it myproject_redis redis-cli MONITOR

# Check cache keys
docker exec -it myproject_redis redis-cli KEYS '*'

# Flush all cache
docker exec -it myproject_redis redis-cli FLUSHALL

# Check Django cache
docker exec -it myproject_backend python manage.py shell -c "from django.core.cache import cache; print(cache._cache)"
```