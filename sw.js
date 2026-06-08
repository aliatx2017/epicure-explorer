/* Epicure Explorer — Service Worker for offline caching */
const CACHE = 'epicure-680f162bb43e';
const STATIC = [
  './',
  './index.html',
  './icon-192.png',
  './icon-512.png',
  './data/epicure_shared.json',
  './data/epicure_nutrition.json',
  './data/recipe_nutrition.json',
  './data/recipe_detections_slim.json',
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(STATIC).catch(function() {
        // Non-critical; app works without SW
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.filter(function(k) { return k !== CACHE; }).map(function(k) { return caches.delete(k); }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  var url = new URL(e.request.url);

  // Only cache our own origin + data files
  if (url.origin !== location.origin) return;

  // Cache JSON bundles on first fetch (lazy-loaded model data)
  if (url.pathname.indexOf('/data/epicure_') >= 0 && url.pathname.endsWith('.json')) {
    e.respondWith(
      caches.open(CACHE).then(function(cache) {
        return fetch(e.request).then(function(response) {
          cache.put(e.request, response.clone());
          return response;
        }).catch(function() {
          return caches.match(e.request);
        });
      })
    );
    return;
  }

  // Stale-while-revalidate for the app shell
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      var fetchPromise = fetch(e.request).then(function(response) {
        caches.open(CACHE).then(function(cache) { cache.put(e.request, response.clone()); });
        return response;
      }).catch(function() { return cached; });
      return cached || fetchPromise;
    })
  );
});
