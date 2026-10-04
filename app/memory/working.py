"""
Tier 1: Working Memory (Redis Backed)
Stores active session telemetry, temporary agent assertions, and current ticket context.
"""

import json
from typing import Dict, Any, Optional


class WorkingMemory:
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self._local_cache: Dict[str, Any] = {}

    def set_session_state(self, customer_id: str, key: str, value: Any, ttl_seconds: int = 3600):
        cache_key = f"working_mem:{customer_id}:{key}"
        if self.redis:
            try:
                self.redis.setex(cache_key, ttl_seconds, json.dumps(value))
                return
            except Exception:
                pass
        self._local_cache[cache_key] = value

    def get_session_state(self, customer_id: str, key: str) -> Optional[Any]:
        cache_key = f"working_mem:{customer_id}:{key}"
        if self.redis:
            try:
                val = self.redis.get(cache_key)
                if val:
                    return json.loads(val)
            except Exception:
                pass
        return self._local_cache.get(cache_key)

    def clear_working_memory(self, customer_id: str):
        if self.redis:
            try:
                keys = self.redis.keys(f"working_mem:{customer_id}:*")
                if keys:
                    self.redis.delete(*keys)
            except Exception:
                pass
        prefix = f"working_mem:{customer_id}:"
        self._local_cache = {k: v for k, v in self._local_cache.items() if not k.startswith(prefix)}
