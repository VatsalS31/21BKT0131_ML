import redis
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_from_cache(key):
    result = cache.get(key)
    if result:
        return json.loads(result)
    return None

def save_to_cache(key, value, expire_time=3600):
    cache.set(key, json.dumps(value), ex=expire_time)
