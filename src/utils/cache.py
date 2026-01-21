from cachetools import TTLCache

class CacheManager:
    def __init__(self):
        self._storage = TTLCache(maxsize=100, ttl=3600)

    def set_cache(self, key, value, ttl=None):
        self._storage[key] = value

    def get_cache(self, key):
        return self._storage.get(key)

cache = CacheManager()