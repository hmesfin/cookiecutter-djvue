/**
 * Advanced caching utilities for frontend
 */

class CacheService {
  constructor(options = {}) {
    this.storage = options.storage || localStorage
    this.prefix = options.prefix || 'app_cache_'
    this.defaultTTL = options.defaultTTL || 300000 // 5 minutes in milliseconds
    this.maxSize = options.maxSize || 50 * 1024 * 1024 // 50MB default
    this.debug = options.debug || false
  }

  /**
   * Generate cache key with prefix
   */
  makeKey(key) {
    return `${this.prefix}${key}`
  }

  /**
   * Get item from cache
   */
  get(key) {
    try {
      const fullKey = this.makeKey(key)
      const item = this.storage.getItem(fullKey)
      
      if (!item) {
        this.log('Cache miss:', key)
        return null
      }

      const data = JSON.parse(item)
      
      // Check if expired
      if (data.expiry && Date.now() > data.expiry) {
        this.log('Cache expired:', key)
        this.remove(key)
        return null
      }

      this.log('Cache hit:', key)
      return data.value
    } catch (error) {
      console.error('Cache get error:', error)
      return null
    }
  }

  /**
   * Set item in cache with optional TTL
   */
  set(key, value, ttl = null) {
    try {
      const fullKey = this.makeKey(key)
      const expiry = ttl ? Date.now() + ttl : (this.defaultTTL ? Date.now() + this.defaultTTL : null)
      
      const data = {
        value,
        expiry,
        timestamp: Date.now()
      }

      // Check storage size before adding
      if (!this.hasSpace(JSON.stringify(data).length)) {
        this.cleanup()
      }

      this.storage.setItem(fullKey, JSON.stringify(data))
      this.log('Cache set:', key)
      return true
    } catch (error) {
      console.error('Cache set error:', error)
      
      // If quota exceeded, try cleanup and retry
      if (error.name === 'QuotaExceededError') {
        this.cleanup()
        try {
          this.storage.setItem(fullKey, JSON.stringify(data))
          return true
        } catch (retryError) {
          console.error('Cache set retry failed:', retryError)
        }
      }
      
      return false
    }
  }

  /**
   * Remove item from cache
   */
  remove(key) {
    try {
      const fullKey = this.makeKey(key)
      this.storage.removeItem(fullKey)
      this.log('Cache remove:', key)
      return true
    } catch (error) {
      console.error('Cache remove error:', error)
      return false
    }
  }

  /**
   * Clear all cache items with prefix
   */
  clear() {
    try {
      const keys = []
      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i)
        if (key && key.startsWith(this.prefix)) {
          keys.push(key)
        }
      }

      keys.forEach(key => this.storage.removeItem(key))
      this.log('Cache cleared:', keys.length, 'items')
      return true
    } catch (error) {
      console.error('Cache clear error:', error)
      return false
    }
  }

  /**
   * Get or set cache value
   */
  async getOrSet(key, fetchFn, ttl = null) {
    // Try to get from cache first
    const cached = this.get(key)
    if (cached !== null) {
      return cached
    }

    // Fetch new value
    try {
      const value = await fetchFn()
      this.set(key, value, ttl)
      return value
    } catch (error) {
      console.error('Cache getOrSet error:', error)
      throw error
    }
  }

  /**
   * Check if storage has enough space
   */
  hasSpace(bytesNeeded) {
    try {
      const used = new Blob([JSON.stringify(this.storage)]).size
      return used + bytesNeeded < this.maxSize
    } catch {
      return true // Assume we have space if we can't check
    }
  }

  /**
   * Clean up expired items
   */
  cleanup() {
    try {
      const now = Date.now()
      const items = []
      
      // Collect all cache items with metadata
      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i)
        if (key && key.startsWith(this.prefix)) {
          try {
            const data = JSON.parse(this.storage.getItem(key))
            items.push({
              key,
              data,
              expired: data.expiry && now > data.expiry
            })
          } catch {
            // Remove corrupted items
            this.storage.removeItem(key)
          }
        }
      }

      // Remove expired items first
      let removed = 0
      items.forEach(item => {
        if (item.expired) {
          this.storage.removeItem(item.key)
          removed++
        }
      })

      // If still need space, remove oldest items
      if (removed === 0) {
        items.sort((a, b) => a.data.timestamp - b.data.timestamp)
        const toRemove = Math.ceil(items.length * 0.2) // Remove 20% of oldest
        
        for (let i = 0; i < toRemove && i < items.length; i++) {
          this.storage.removeItem(items[i].key)
          removed++
        }
      }

      this.log('Cache cleanup:', removed, 'items removed')
      return removed
    } catch (error) {
      console.error('Cache cleanup error:', error)
      return 0
    }
  }

  /**
   * Get cache statistics
   */
  getStats() {
    try {
      let count = 0
      let size = 0
      let expired = 0
      const now = Date.now()

      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i)
        if (key && key.startsWith(this.prefix)) {
          count++
          const item = this.storage.getItem(key)
          size += item.length
          
          try {
            const data = JSON.parse(item)
            if (data.expiry && now > data.expiry) {
              expired++
            }
          } catch {
            // Ignore parse errors
          }
        }
      }

      return {
        count,
        size,
        expired,
        sizeInMB: (size / (1024 * 1024)).toFixed(2)
      }
    } catch (error) {
      console.error('Cache stats error:', error)
      return { count: 0, size: 0, expired: 0, sizeInMB: '0' }
    }
  }

  /**
   * Debug logging
   */
  log(...args) {
    if (this.debug) {
      console.log('[Cache]', ...args)
    }
  }
}

/**
 * Memory cache for temporary data
 */
class MemoryCache {
  constructor(options = {}) {
    this.cache = new Map()
    this.defaultTTL = options.defaultTTL || 60000 // 1 minute default
    this.maxSize = options.maxSize || 100 // Maximum number of items
    this.debug = options.debug || false
  }

  get(key) {
    const item = this.cache.get(key)
    
    if (!item) {
      this.log('Memory cache miss:', key)
      return null
    }

    if (item.expiry && Date.now() > item.expiry) {
      this.log('Memory cache expired:', key)
      this.cache.delete(key)
      return null
    }

    this.log('Memory cache hit:', key)
    return item.value
  }

  set(key, value, ttl = null) {
    const expiry = ttl ? Date.now() + ttl : (this.defaultTTL ? Date.now() + this.defaultTTL : null)
    
    // Enforce max size
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value
      this.cache.delete(firstKey)
    }

    this.cache.set(key, {
      value,
      expiry,
      timestamp: Date.now()
    })

    this.log('Memory cache set:', key)
  }

  remove(key) {
    return this.cache.delete(key)
  }

  clear() {
    this.cache.clear()
  }

  getStats() {
    return {
      count: this.cache.size,
      maxSize: this.maxSize
    }
  }

  log(...args) {
    if (this.debug) {
      console.log('[MemoryCache]', ...args)
    }
  }
}

/**
 * API response cache with axios interceptor
 */
class APICache {
  constructor(axios, options = {}) {
    this.axios = axios
    this.cache = new CacheService({
      prefix: 'api_cache_',
      ...options
    })
    this.setupInterceptors()
  }

  setupInterceptors() {
    // Request interceptor
    this.axios.interceptors.request.use(
      config => {
        // Only cache GET requests
        if (config.method === 'get' && config.cache !== false) {
          const cacheKey = this.getCacheKey(config)
          const cached = this.cache.get(cacheKey)
          
          if (cached) {
            // Return cached response
            config.adapter = () => {
              return Promise.resolve({
                data: cached.data,
                status: cached.status,
                statusText: cached.statusText,
                headers: cached.headers,
                config: config,
                cached: true
              })
            }
          }
        }
        
        return config
      },
      error => Promise.reject(error)
    )

    // Response interceptor
    this.axios.interceptors.response.use(
      response => {
        // Cache successful GET responses
        if (
          response.config.method === 'get' &&
          response.config.cache !== false &&
          response.status === 200 &&
          !response.cached
        ) {
          const cacheKey = this.getCacheKey(response.config)
          const ttl = this.getCacheTTL(response.config)
          
          this.cache.set(cacheKey, {
            data: response.data,
            status: response.status,
            statusText: response.statusText,
            headers: response.headers
          }, ttl)
        }
        
        return response
      },
      error => Promise.reject(error)
    )
  }

  getCacheKey(config) {
    const url = config.url
    const params = config.params ? JSON.stringify(config.params) : ''
    return `${url}:${params}`
  }

  getCacheTTL(config) {
    // Allow per-request cache TTL
    if (config.cacheTTL) {
      return config.cacheTTL
    }

    // Default TTLs based on endpoint
    const url = config.url
    
    if (url.includes('/config')) {
      return 3600000 // 1 hour for config
    }
    if (url.includes('/user')) {
      return 60000 // 1 minute for user data
    }
    
    return 300000 // 5 minutes default
  }

  invalidate(pattern) {
    // Clear cache entries matching pattern
    const stats = this.cache.getStats()
    let cleared = 0
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && key.includes(pattern)) {
        localStorage.removeItem(key)
        cleared++
      }
    }
    
    return cleared
  }
}

/**
 * Service Worker cache helper
 */
class ServiceWorkerCache {
  constructor(cacheName = 'app-cache-v1') {
    this.cacheName = cacheName
    this.initialized = false
    this.init()
  }

  async init() {
    if ('serviceWorker' in navigator && 'caches' in window) {
      this.initialized = true
    }
  }

  async precache(urls) {
    if (!this.initialized) return false

    try {
      const cache = await caches.open(this.cacheName)
      await cache.addAll(urls)
      return true
    } catch (error) {
      console.error('Precache error:', error)
      return false
    }
  }

  async get(url) {
    if (!this.initialized) return null

    try {
      const cache = await caches.open(this.cacheName)
      const response = await cache.match(url)
      return response
    } catch (error) {
      console.error('Cache get error:', error)
      return null
    }
  }

  async set(url, response) {
    if (!this.initialized) return false

    try {
      const cache = await caches.open(this.cacheName)
      await cache.put(url, response)
      return true
    } catch (error) {
      console.error('Cache set error:', error)
      return false
    }
  }

  async clear() {
    if (!this.initialized) return false

    try {
      await caches.delete(this.cacheName)
      return true
    } catch (error) {
      console.error('Cache clear error:', error)
      return false
    }
  }
}

// Create default instances
const cache = new CacheService()
const memoryCache = new MemoryCache()

export {
  CacheService,
  MemoryCache,
  APICache,
  ServiceWorkerCache,
  cache,
  memoryCache
}