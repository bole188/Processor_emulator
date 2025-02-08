from Cache import *
from emulator import *

class MultiLevelCache:
    def __init__(self, levels_config, memory_access_function):
        self.caches = []
        for level in levels_config:
            cache_type = level.get("type")
            cache_size = level.get("size")
            line_size = level.get("line_size")

            if cache_type == "DirectMapped":
                self.caches.append(DirectMappedCache(cache_size, line_size, memory_access_function))
            elif cache_type == "SetAssociative":
                num_ways = level.get("ways")
                replacement_policy = level.get("replacement_policy", "LRU")
                self.caches.append(SetAssociativeCache(cache_size, line_size, num_ways, replacement_policy, memory_access_function))
            elif cache_type == "FullyAssociative":
                replacement_policy = level.get("replacement_policy", "LRU")
                self.caches.append(FullyAssociativeCache(cache_size, line_size, replacement_policy, memory_access_function))

    def access_cache(self, address):
        for cache in self.caches:
            data = cache.access_cache(address)
            if cache.hits > 0:
                return data
        return self.caches[-1].access_cache(address)

    def cache_stats(self):
        stats = []
        for i, cache in enumerate(self.caches):
            stats.append(f"Cache Level {i+1} Stats: {cache.cache_stats()}")
        return "\n".join(stats)
