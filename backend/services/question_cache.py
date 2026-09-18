"""
Zavran AI — Question Bank Caching Layer
High-performance Redis caching with In-Memory LRU fallback for prepared 100-question packs.
"""

import json
import hashlib
import logging
import time
from typing import Dict, Any, Optional

logger = logging.getLogger("ZavranAI.QuestionCache")

# Default TTL: 24 hours
DEFAULT_CACHE_TTL = 86400


class QuestionCache:
    """
    Manages Redis caching and local in-memory fallback for prepared question packs.
    """

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_client = None
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._ttl_tracker: Dict[str, float] = {}

        # Attempt Redis connection if redis module is present
        try:
            import redis
            url = redis_url or "redis://localhost:6379/0"
            client = redis.from_url(url, socket_timeout=1.0, socket_connect_timeout=1.0, decode_responses=True)
            client.ping()
            self.redis_client = client
            logger.info("Connected to Redis cache.")
        except Exception as e:
            logger.info(f"Redis not available ({e}). Using robust In-Memory Cache fallback.")
            self.redis_client = None

    @staticmethod
    def build_cache_key(
        normalized_role: str,
        seniority: str,
        skills: list,
        version: str = "v1",
    ) -> str:
        """
        Builds standardized cache key:
        interview_questions:{normalized_role}:{seniority}:{skill_hash}:{version}
        """
        norm_role = normalized_role.strip().lower().replace(" ", "_")
        norm_seniority = (seniority or "all").strip().lower().replace(" ", "_")
        sorted_skills = "-".join(sorted([s.strip().lower() for s in skills if s.strip()]))
        skill_hash = hashlib.md5(sorted_skills.encode("utf-8")).hexdigest()[:12] if sorted_skills else "general"
        return f"interview_questions:{norm_role}:{norm_seniority}:{skill_hash}:{version}"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached item from Redis or in-memory fallback."""
        if self.redis_client:
            try:
                data = self.redis_client.get(key)
                if data:
                    logger.debug(f"Redis cache hit: {key}")
                    return json.loads(data)
            except Exception as e:
                logger.warning(f"Redis get error: {e}")

        # In-memory fallback
        if key in self._memory_cache:
            expiry = self._ttl_tracker.get(key, 0)
            if expiry > time.time():
                logger.debug(f"Memory cache hit: {key}")
                return self._memory_cache[key]
            else:
                del self._memory_cache[key]
                if key in self._ttl_tracker:
                    del self._ttl_tracker[key]

        return None

    def set(self, key: str, value: Dict[str, Any], ttl_seconds: int = DEFAULT_CACHE_TTL) -> bool:
        """Stores item in Redis and in-memory cache."""
        success = False
        payload = json.dumps(value)

        if self.redis_client:
            try:
                self.redis_client.setex(key, ttl_seconds, payload)
                success = True
            except Exception as e:
                logger.warning(f"Redis set error: {e}")

        # Always store in in-memory fallback as well
        self._memory_cache[key] = value
        self._ttl_tracker[key] = time.time() + ttl_seconds
        return True

    def invalidate(self, pattern: Optional[str] = None):
        """Invalidates cache entries."""
        if self.redis_client and pattern:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            except Exception as e:
                logger.warning(f"Redis invalidate error: {e}")

        if pattern:
            prefix = pattern.replace("*", "")
            to_del = [k for k in self._memory_cache if k.startswith(prefix)]
            for k in to_del:
                self._memory_cache.pop(k, None)
                self._ttl_tracker.pop(k, None)
        else:
            self._memory_cache.clear()
            self._ttl_tracker.clear()


question_cache = QuestionCache()
