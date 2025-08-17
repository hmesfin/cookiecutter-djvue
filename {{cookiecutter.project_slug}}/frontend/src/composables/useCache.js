/**
 * Composable for cache management in Vue components
 */
import { ref, computed, watch, onUnmounted } from 'vue'
import { cache, memoryCache } from '@/services/cache'

/**
 * Cache composable for Vue components
 * 
 * @param {String} key - Cache key prefix
 * @param {Object} options - Cache options
 * @returns {Object} Cache utilities
 */
export function useCache(key, options = {}) {
  const {
    storage = 'local', // 'local', 'session', or 'memory'
    ttl = 300000, // 5 minutes default
    watchValue = null,
    autoSave = false,
    debug = false
  } = options

  // Select cache instance based on storage type
  const cacheInstance = storage === 'memory' ? memoryCache : cache

  // Reactive state
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const lastFetch = ref(null)

  // Computed properties
  const hasCache = computed(() => {
    return cacheInstance.get(key) !== null
  })

  const isStale = computed(() => {
    if (!lastFetch.value) return true
    return Date.now() - lastFetch.value > ttl
  })

  /**
   * Load data from cache
   */
  const load = () => {
    try {
      const cached = cacheInstance.get(key)
      if (cached !== null) {
        data.value = cached
        lastFetch.value = Date.now()
        if (debug) console.log(`[useCache] Loaded from cache:`, key)
        return true
      }
      return false
    } catch (err) {
      error.value = err
      console.error('[useCache] Load error:', err)
      return false
    }
  }

  /**
   * Save data to cache
   */
  const save = (value = null) => {
    try {
      const dataToSave = value !== null ? value : data.value
      cacheInstance.set(key, dataToSave, ttl)
      lastFetch.value = Date.now()
      if (debug) console.log(`[useCache] Saved to cache:`, key)
      return true
    } catch (err) {
      error.value = err
      console.error('[useCache] Save error:', err)
      return false
    }
  }

  /**
   * Fetch data with caching
   */
  const fetch = async (fetchFn, forceRefresh = false) => {
    // Check cache first unless force refresh
    if (!forceRefresh && !isStale.value) {
      const cached = cacheInstance.get(key)
      if (cached !== null) {
        data.value = cached
        return cached
      }
    }

    loading.value = true
    error.value = null

    try {
      const result = await fetchFn()
      data.value = result
      save(result)
      return result
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Clear cache
   */
  const clear = () => {
    cacheInstance.remove(key)
    data.value = null
    lastFetch.value = null
    if (debug) console.log(`[useCache] Cleared cache:`, key)
  }

  /**
   * Invalidate cache (mark as stale)
   */
  const invalidate = () => {
    lastFetch.value = null
  }

  // Auto-save watcher
  let stopWatcher = null
  if (autoSave && watchValue) {
    stopWatcher = watch(watchValue, (newValue) => {
      save(newValue)
    }, { deep: true })
  }

  // Load initial data from cache
  load()

  // Cleanup
  onUnmounted(() => {
    if (stopWatcher) {
      stopWatcher()
    }
  })

  return {
    // State
    data,
    loading,
    error,
    hasCache,
    isStale,
    
    // Methods
    load,
    save,
    fetch,
    clear,
    invalidate
  }
}

/**
 * Cached API call composable
 * 
 * @param {Function} apiCall - API call function
 * @param {Object} options - Cache options
 * @returns {Object} API utilities
 */
export function useCachedAPI(apiCall, options = {}) {
  const {
    key = null,
    ttl = 300000,
    immediate = false,
    transform = null,
    onSuccess = null,
    onError = null,
    retryAttempts = 0,
    retryDelay = 1000
  } = options

  // Generate cache key from API call
  const cacheKey = key || `api_${apiCall.toString().slice(0, 50)}`
  
  // Use cache composable
  const {
    data,
    loading,
    error,
    hasCache,
    isStale,
    fetch: fetchWithCache,
    clear,
    invalidate
  } = useCache(cacheKey, { ttl })

  /**
   * Execute API call with retry logic
   */
  const execute = async (params = {}, forceRefresh = false) => {
    const apiCallWithRetry = async () => {
      let lastError = null
      
      for (let attempt = 0; attempt <= retryAttempts; attempt++) {
        try {
          const response = await apiCall(params)
          const result = transform ? transform(response) : response
          
          if (onSuccess) {
            onSuccess(result)
          }
          
          return result
        } catch (err) {
          lastError = err
          
          if (attempt < retryAttempts) {
            await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)))
          }
        }
      }
      
      if (onError) {
        onError(lastError)
      }
      
      throw lastError
    }

    return fetchWithCache(apiCallWithRetry, forceRefresh)
  }

  /**
   * Refresh data (force fetch)
   */
  const refresh = () => execute({}, true)

  // Execute immediately if requested
  if (immediate) {
    execute()
  }

  return {
    // State
    data,
    loading,
    error,
    hasCache,
    isStale,
    
    // Methods
    execute,
    refresh,
    clear,
    invalidate
  }
}

/**
 * Optimistic update composable
 * 
 * @param {Function} updateFn - Update function
 * @param {Object} options - Options
 * @returns {Object} Update utilities
 */
export function useOptimisticUpdate(updateFn, options = {}) {
  const {
    cacheKey,
    optimisticUpdate = null,
    rollbackOnError = true
  } = options

  const updating = ref(false)
  const error = ref(null)
  const previousValue = ref(null)

  /**
   * Perform optimistic update
   */
  const update = async (data) => {
    updating.value = true
    error.value = null

    // Store previous value for rollback
    if (cacheKey && rollbackOnError) {
      previousValue.value = cache.get(cacheKey)
    }

    // Apply optimistic update
    if (optimisticUpdate && cacheKey) {
      const optimisticValue = optimisticUpdate(previousValue.value, data)
      cache.set(cacheKey, optimisticValue)
    }

    try {
      const result = await updateFn(data)
      
      // Update cache with real result
      if (cacheKey) {
        cache.set(cacheKey, result)
      }
      
      return result
    } catch (err) {
      error.value = err
      
      // Rollback on error
      if (rollbackOnError && cacheKey && previousValue.value !== null) {
        cache.set(cacheKey, previousValue.value)
      }
      
      throw err
    } finally {
      updating.value = false
    }
  }

  return {
    updating,
    error,
    update
  }
}

/**
 * Infinite scroll with caching
 * 
 * @param {Function} fetchFn - Fetch function for pages
 * @param {Object} options - Options
 * @returns {Object} Infinite scroll utilities
 */
export function useCachedInfiniteScroll(fetchFn, options = {}) {
  const {
    cacheKey = 'infinite_scroll',
    pageSize = 20,
    ttl = 300000
  } = options

  const items = ref([])
  const page = ref(1)
  const hasMore = ref(true)
  const loading = ref(false)
  const error = ref(null)

  // Load cached pages
  const loadCached = () => {
    const cached = cache.get(cacheKey)
    if (cached) {
      items.value = cached.items || []
      page.value = cached.page || 1
      hasMore.value = cached.hasMore !== false
    }
  }

  // Save to cache
  const saveToCache = () => {
    cache.set(cacheKey, {
      items: items.value,
      page: page.value,
      hasMore: hasMore.value
    }, ttl)
  }

  /**
   * Load next page
   */
  const loadMore = async () => {
    if (loading.value || !hasMore.value) return

    loading.value = true
    error.value = null

    try {
      const result = await fetchFn({
        page: page.value,
        pageSize
      })

      const newItems = result.data || result.results || result
      
      if (newItems.length < pageSize) {
        hasMore.value = false
      }

      items.value = [...items.value, ...newItems]
      page.value++
      
      saveToCache()
      
      return newItems
    } catch (err) {
      error.value = err
      throw err
    } finally {
      loading.value = false
    }
  }

  /**
   * Reset and reload
   */
  const reset = () => {
    items.value = []
    page.value = 1
    hasMore.value = true
    error.value = null
    cache.remove(cacheKey)
  }

  // Load cached data on init
  loadCached()

  return {
    items,
    page,
    hasMore,
    loading,
    error,
    loadMore,
    reset
  }
}