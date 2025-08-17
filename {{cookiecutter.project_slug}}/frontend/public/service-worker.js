/**
 * Service Worker for advanced caching strategies
 */

const CACHE_VERSION = 'v1'
const CACHE_NAME = `app-cache-${CACHE_VERSION}`
const API_CACHE_NAME = `api-cache-${CACHE_VERSION}`
const IMAGE_CACHE_NAME = `image-cache-${CACHE_VERSION}`

// Files to cache immediately
const STATIC_CACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico'
]

// Cache strategies
const CACHE_STRATEGIES = {
  // Cache first, fallback to network
  CACHE_FIRST: 'cache-first',
  // Network first, fallback to cache
  NETWORK_FIRST: 'network-first',
  // Cache only
  CACHE_ONLY: 'cache-only',
  // Network only
  NETWORK_ONLY: 'network-only',
  // Stale while revalidate
  STALE_WHILE_REVALIDATE: 'stale-while-revalidate'
}

// Route to strategy mapping
const ROUTE_STRATEGIES = [
  {
    pattern: /\/api\//,
    strategy: CACHE_STRATEGIES.NETWORK_FIRST,
    cache: API_CACHE_NAME,
    ttl: 5 * 60 * 1000 // 5 minutes
  },
  {
    pattern: /\.(png|jpg|jpeg|gif|webp|svg)$/,
    strategy: CACHE_STRATEGIES.CACHE_FIRST,
    cache: IMAGE_CACHE_NAME,
    ttl: 7 * 24 * 60 * 60 * 1000 // 7 days
  },
  {
    pattern: /\.(js|css)$/,
    strategy: CACHE_STRATEGIES.STALE_WHILE_REVALIDATE,
    cache: CACHE_NAME,
    ttl: 24 * 60 * 60 * 1000 // 1 day
  },
  {
    pattern: /\.(woff2?|ttf|eot)$/,
    strategy: CACHE_STRATEGIES.CACHE_FIRST,
    cache: CACHE_NAME,
    ttl: 30 * 24 * 60 * 60 * 1000 // 30 days
  }
]

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Installing...')
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Caching static assets')
        return cache.addAll(STATIC_CACHE_URLS)
      })
      .then(() => self.skipWaiting())
      .catch(err => console.error('[ServiceWorker] Install failed:', err))
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activating...')
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => {
              // Delete old cache versions
              return name.startsWith('app-cache-') && name !== CACHE_NAME ||
                     name.startsWith('api-cache-') && name !== API_CACHE_NAME ||
                     name.startsWith('image-cache-') && name !== IMAGE_CACHE_NAME
            })
            .map(name => {
              console.log('[ServiceWorker] Deleting cache:', name)
              return caches.delete(name)
            })
        )
      })
      .then(() => self.clients.claim())
  )
})

// Fetch event - apply caching strategies
self.addEventListener('fetch', event => {
  const { request } = event
  const url = new URL(request.url)

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return
  }

  // Skip Chrome extensions and dev tools
  if (url.protocol === 'chrome-extension:' || url.hostname === 'localhost' && url.port === '3000') {
    return
  }

  // Find matching strategy
  const route = ROUTE_STRATEGIES.find(r => r.pattern.test(url.pathname))
  const strategy = route ? route.strategy : CACHE_STRATEGIES.NETWORK_FIRST
  const cacheName = route ? route.cache : CACHE_NAME

  event.respondWith(
    handleRequest(request, strategy, cacheName)
  )
})

/**
 * Handle request based on caching strategy
 */
async function handleRequest(request, strategy, cacheName) {
  switch (strategy) {
    case CACHE_STRATEGIES.CACHE_FIRST:
      return cacheFirst(request, cacheName)
    
    case CACHE_STRATEGIES.NETWORK_FIRST:
      return networkFirst(request, cacheName)
    
    case CACHE_STRATEGIES.CACHE_ONLY:
      return cacheOnly(request, cacheName)
    
    case CACHE_STRATEGIES.NETWORK_ONLY:
      return fetch(request)
    
    case CACHE_STRATEGIES.STALE_WHILE_REVALIDATE:
      return staleWhileRevalidate(request, cacheName)
    
    default:
      return fetch(request)
  }
}

/**
 * Cache first strategy
 */
async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cached = await cache.match(request)
  
  if (cached) {
    return cached
  }
  
  try {
    const response = await fetch(request)
    
    if (response.ok) {
      cache.put(request, response.clone())
    }
    
    return response
  } catch (error) {
    console.error('[ServiceWorker] Fetch failed:', error)
    throw error
  }
}

/**
 * Network first strategy
 */
async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request)
    
    if (response.ok) {
      const cache = await caches.open(cacheName)
      cache.put(request, response.clone())
    }
    
    return response
  } catch (error) {
    const cache = await caches.open(cacheName)
    const cached = await cache.match(request)
    
    if (cached) {
      return cached
    }
    
    throw error
  }
}

/**
 * Cache only strategy
 */
async function cacheOnly(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cached = await cache.match(request)
  
  if (cached) {
    return cached
  }
  
  return new Response('Cache miss', {
    status: 404,
    statusText: 'Not Found'
  })
}

/**
 * Stale while revalidate strategy
 */
async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName)
  const cached = await cache.match(request)
  
  const fetchPromise = fetch(request).then(response => {
    if (response.ok) {
      cache.put(request, response.clone())
    }
    return response
  })
  
  return cached || fetchPromise
}

// Message event - handle cache operations from main thread
self.addEventListener('message', event => {
  const { type, payload } = event.data
  
  switch (type) {
    case 'SKIP_WAITING':
      self.skipWaiting()
      break
    
    case 'CLEAR_CACHE':
      event.waitUntil(
        caches.keys().then(names => {
          return Promise.all(names.map(name => caches.delete(name)))
        })
      )
      break
    
    case 'CACHE_URLS':
      event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
          return cache.addAll(payload.urls)
        })
      )
      break
  }
})

// Background sync for offline support
self.addEventListener('sync', event => {
  if (event.tag === 'sync-api-requests') {
    event.waitUntil(syncAPIRequests())
  }
})

/**
 * Sync queued API requests when back online
 */
async function syncAPIRequests() {
  // Implementation for syncing offline requests
  console.log('[ServiceWorker] Syncing API requests...')
}