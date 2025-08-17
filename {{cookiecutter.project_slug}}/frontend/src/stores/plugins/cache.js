/**
 * Pinia plugin for automatic store caching
 */
import { watch } from 'vue'
import { cache } from '@/services/cache'

/**
 * Cache plugin for Pinia stores
 * 
 * Usage in store:
 * export const useMyStore = defineStore('myStore', {
 *   state: () => ({ ... }),
 *   cache: {
 *     enabled: true,
 *     ttl: 300000, // 5 minutes
 *     paths: ['user', 'settings'], // Specific paths to cache
 *     exclude: ['temp'], // Paths to exclude from caching
 *   }
 * })
 */
export function PiniaCachePlugin(context) {
  const { store, options } = context
  
  // Check if caching is enabled for this store
  const cacheConfig = options.cache || store.$options?.cache
  if (!cacheConfig || cacheConfig.enabled === false) {
    return
  }

  const storeId = store.$id
  const cacheKey = `pinia_${storeId}`
  const ttl = cacheConfig.ttl || 300000 // Default 5 minutes
  const paths = cacheConfig.paths || null
  const exclude = cacheConfig.exclude || []

  // Load cached state on store creation
  const loadCachedState = () => {
    const cached = cache.get(cacheKey)
    if (cached) {
      // If specific paths are defined, only restore those
      if (paths && Array.isArray(paths)) {
        paths.forEach(path => {
          if (cached[path] !== undefined) {
            setNestedProperty(store.$state, path, cached[path])
          }
        })
      } else {
        // Restore entire state except excluded paths
        Object.keys(cached).forEach(key => {
          if (!exclude.includes(key)) {
            store.$state[key] = cached[key]
          }
        })
      }
    }
  }

  // Save state to cache
  const saveToCache = () => {
    let stateToCache = {}

    if (paths && Array.isArray(paths)) {
      // Only cache specific paths
      paths.forEach(path => {
        const value = getNestedProperty(store.$state, path)
        if (value !== undefined) {
          setNestedProperty(stateToCache, path, value)
        }
      })
    } else {
      // Cache entire state except excluded paths
      stateToCache = { ...store.$state }
      exclude.forEach(path => {
        deleteNestedProperty(stateToCache, path)
      })
    }

    cache.set(cacheKey, stateToCache, ttl)
  }

  // Load cached state immediately
  loadCachedState()

  // Watch for state changes and update cache
  const stopWatcher = watch(
    () => store.$state,
    () => {
      saveToCache()
    },
    { deep: true }
  )

  // Provide methods to manually control caching
  store.$cache = {
    save: saveToCache,
    load: loadCachedState,
    clear: () => cache.remove(cacheKey),
    stop: stopWatcher
  }

  // Clean up on store disposal
  store.$onAction(({ after, onError }) => {
    after(() => {
      // Save after successful actions
      saveToCache()
    })
    
    onError(() => {
      // Optionally reload from cache on error
      if (cacheConfig.reloadOnError) {
        loadCachedState()
      }
    })
  })

  return {
    // Return cleanup function
    dispose: () => {
      stopWatcher()
    }
  }
}

/**
 * Helper function to get nested property
 */
function getNestedProperty(obj, path) {
  return path.split('.').reduce((current, key) => current?.[key], obj)
}

/**
 * Helper function to set nested property
 */
function setNestedProperty(obj, path, value) {
  const keys = path.split('.')
  const lastKey = keys.pop()
  const target = keys.reduce((current, key) => {
    if (!current[key]) {
      current[key] = {}
    }
    return current[key]
  }, obj)
  target[lastKey] = value
}

/**
 * Helper function to delete nested property
 */
function deleteNestedProperty(obj, path) {
  const keys = path.split('.')
  const lastKey = keys.pop()
  const target = keys.reduce((current, key) => current?.[key], obj)
  if (target) {
    delete target[lastKey]
  }
}

/**
 * Create a cached getter for expensive computations
 */
export function cachedGetter(fn, ttl = 60000) {
  let cachedValue = null
  let cacheTime = 0

  return function(...args) {
    const now = Date.now()
    if (!cachedValue || now - cacheTime > ttl) {
      cachedValue = fn.apply(this, args)
      cacheTime = now
    }
    return cachedValue
  }
}

/**
 * Debounced cache setter to avoid excessive writes
 */
export function debouncedCache(fn, delay = 1000) {
  let timeoutId = null

  return function(...args) {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}