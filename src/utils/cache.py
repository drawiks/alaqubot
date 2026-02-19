
from cachetools import TTLCache

class CacheManager:
    def __init__(self, maxsize=100, ttl=3600):
        self._storage = TTLCache(maxsize=maxsize, ttl=ttl)

    def set_cache(self, key, value):
        self._storage[key] = value

    def get_cache(self, key):
        return self._storage.get(key)

cache = CacheManager()