
import datetime, os
from os.path import exists

class LdesCache:

    def __init__(self, max_entries, cache_dir):
        self.mem_cache = dict()
        self.cache_dir = cache_dir if cache_dir else "__cache__"
        self.max_entries = max_entries if max_entries else 100
    
    def get(self, key):
        if key in self.mem_cache.keys():
            self.mem_cache[key]["last_used"] = datetime.datetime.now()
            return self.mem_cache[key]["value"]
        else:
            return self.get_from_disk(key)
            return None
    
    def mem_keys(self):
        return self.mem_cache.keys()

    def get_from_disk(self, key):
        filename = os.path.join(self.cache_dir, f"{key}.ttl")
        if not exists(filename):
            return None
        else: 
            with open(filename, 'r') as f:
                value = f.read()
            cahce_entry = {
            "key": key,
            "value": value,
            "last_used": datetime.datetime.now()
        }
        self.mem_cache[key] = cahce_entry
        self.remove_least_recently_used()
    
    def put(self, key, value):
        cahce_entry = {
            "key": key,
            "value": value,
            "last_used": datetime.datetime.now()
        }
        self.mem_cache[key] = cahce_entry
        self.store_to_disk(key, value)
        self.remove_least_recently_used()

    def store_to_disk(self, key, value):
        filename = os.path.join(self.cache_dir, f"{key}.ttl")
        with open(filename, 'w') as f:
            f.write(value)

    def remove_least_recently_used(self):
        if len(self.mem_cache) > self.max_entries:
            min_date = datetime.datetime.now()
            min_key = None
            for key in self.mem_cache.keys():
                if  self.mem_cache[key]["last_used"] < min_date:
                    min_date = self.mem_cache[key]["last_used"]
                    min_key = key
            self.mem_cache.pop(min_key)

    def clear(self):
        for key in self.mem_cache.keys():
            filename = os.path.join(self.cache_dir, f"{key}.ttl")
            if exists(filename):
                os.remove(filename)
        self.mem_cache = dict()


    def _dump_cache(self):
        for key in self.mem_cache.keys():
            last_used = self.mem_cache[key]["last_used"]
            print(f"{key} | {last_used}")


