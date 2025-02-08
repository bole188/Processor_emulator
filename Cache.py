from abc import ABC, abstractmethod
from collections import deque

class CacheLine:
    def __init__(self):
        self.data = 0  # 64 bits
        self.valid = False
        self.tag = None

class Cache(ABC):
    def __init__(self, cache_size, line_size, memory_access_function):
        self.cache_size = cache_size
        self.line_size = line_size
        self.num_lines = cache_size // line_size
        self.cache_lines = [CacheLine() for _ in range(self.num_lines)]
        self.memory_access_function = memory_access_function
        self.hits = 0
        self.misses = 0
        self.accesses = 0

    @abstractmethod
    def access_cache(self, address):
        pass
    
    @abstractmethod
    def update_cache(self, address, data):
        pass
    
    @abstractmethod
    def breakdown_address(self, address):
        pass

    def increment_access(self):
        self.accesses += 1
    
    def increment_hit(self):
        self.hits += 1

    def increment_miss(self):
        self.misses += 1

    def cache_stats(self):
        return {
            "accesses": self.accesses,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / self.accesses if self.accesses > 0 else 0
        }

class DirectMappedCache(Cache):
    def __init__(self, cache_size, line_size, memory_access_function):
        super().__init__(cache_size, line_size, memory_access_function)

    def breakdown_address(self, address):
        offset_bits = int.bit_length(self.line_size - 1)
        index_bits = int.bit_length(self.num_lines - 1)
        tag = address >> (offset_bits + index_bits)
        index = (address >> offset_bits) & (self.num_lines - 1)
        offset = address & (self.line_size - 1)
        return tag, index, offset

    def access_cache(self, address):
        self.increment_access()
        tag, index, _ = self.breakdown_address(address)
        line = self.cache_lines[index]

        if line.valid and line.tag == tag:
            self.increment_hit()
            return line.data
        else:
            self.increment_miss()
            data = self.memory_access_function(address)
            self.update_cache(address, data)
            return data

    def update_cache(self, address, data):
        tag, index, _ = self.breakdown_address(address)
        line = self.cache_lines[index]
        line.data = data
        line.tag = tag
        line.valid = True

class SetAssociativeCache(Cache):
    def __init__(self, cache_size, line_size, num_ways, replacement_policy, memory_access_function, future_accesses=None):
        super().__init__(cache_size, line_size, memory_access_function)
        self.num_ways = num_ways
        self.num_sets = self.num_lines // num_ways
        self.cache_sets = [[CacheLine() for _ in range(num_ways)] for _ in range(self.num_sets)]
        self.replacement_policy = replacement_policy
        self.future_accesses = future_accesses or {}
        if replacement_policy == 'LRU':
            self.lru_tracker = [deque() for _ in range(self.num_sets)]
    
    def breakdown_address(self, address):
        offset_bits = int.bit_length(self.line_size - 1)
        index_bits = int.bit_length(self.num_sets - 1)
        tag = address >> (offset_bits + index_bits)
        index = (address >> offset_bits) & (self.num_sets - 1)
        offset = address & (self.line_size - 1)
        return tag, index, offset
    
    def access_cache(self, address):
        self.increment_access()
        tag, index, _ = self.breakdown_address(address)
        cache_set = self.cache_sets[index]
        
        for i, line in enumerate(cache_set):
            if line.valid and line.tag == tag:
                self.increment_hit()
                if self.replacement_policy == 'LRU':
                    self.lru_tracker[index].remove(i)
                    self.lru_tracker[index].append(i)
                return line.data
        
        self.increment_miss()
        data = self.memory_access_function(address)
        self.update_cache(address, data)
        return data

    def update_cache(self, address, data):
        tag, index, _ = self.breakdown_address(address)
        cache_set = self.cache_sets[index]
        
        for i, line in enumerate(cache_set):
            if not line.valid:
                cache_set[i].data = data
                cache_set[i].tag = tag
                cache_set[i].valid = True
                if self.replacement_policy == 'LRU':
                    self.lru_tracker[index].append(i)
                return
        
        if self.replacement_policy == 'LRU':
            lru_index = self.lru_tracker[index].popleft()
            cache_set[lru_index].data = data
            cache_set[lru_index].tag = tag
            cache_set[lru_index].valid = True
            self.lru_tracker[index].append(lru_index)
        elif self.replacement_policy == 'Belady':
            future_access = self.future_accesses.get(index, [])
            furthest_use = -1
            block_to_replace = None
            for i, line in enumerate(cache_set):
                if line.tag in future_access:
                    use_distance = future_access.index(line.tag)
                    if use_distance > furthest_use:
                        furthest_use = use_distance
                        block_to_replace = i
                else:
                    block_to_replace = i
                    break
            cache_set[block_to_replace].data = data
            cache_set[block_to_replace].tag = tag
            cache_set[block_to_replace].valid = True

class FullyAssociativeCache(Cache):
    def __init__(self, cache_size, line_size, replacement_policy, memory_access_function, future_accesses=None):
        super().__init__(cache_size, line_size, memory_access_function)
        self.replacement_policy = replacement_policy
        self.future_accesses = future_accesses or []
        if replacement_policy == 'LRU':
            self.lru_tracker = deque()
    
    def breakdown_address(self, address):
        offset_bits = int.bit_length(self.line_size - 1)
        tag = address >> offset_bits
        offset = address & (self.line_size - 1)
        return tag, None, offset
    
    def access_cache(self, address):
        self.increment_access()
        tag, _, _ = self.breakdown_address(address)

        for i, line in enumerate(self.cache_lines):
            if line.valid and line.tag == tag:
                self.increment_hit()
                if self.replacement_policy == 'LRU':
                    self.lru_tracker.remove(i)
                    self.lru_tracker.append(i)
                return line.data
        
        self.increment_miss()
        data = self.memory_access_function(address)
        self.update_cache(address, data)
        return data

    def update_cache(self, address, data):
        tag, _, _ = self.breakdown_address(address)

        for i, line in enumerate(self.cache_lines):
            if not line.valid:
                line.data = data
                line.tag = tag
                line.valid = True
                if self.replacement_policy == 'LRU':
                    self.lru_tracker.append(i)
                return
        
        if self.replacement_policy == 'LRU':
            lru_index = self.lru_tracker.popleft()
            self.cache_lines[lru_index].data = data
            self.cache_lines[lru_index].tag = tag
            self.cache_lines[lru_index].valid = True
            self.lru_tracker.append(lru_index)
        

