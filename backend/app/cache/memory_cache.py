"""In-memory cache for Sheets data with TTL support."""
import logging
import time
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class MemoryCache:
    """Simple in-memory cache with TTL (Time To Live) for MVP."""

    def __init__(self, ttl_minutes: int = 5):
        self.ttl_seconds = ttl_minutes * 60
        self.cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self.cache:
            logger.debug(f"Cache miss: {key}")
            return None

        entry = self.cache[key]
        if time.time() > entry["expires_at"]:
            del self.cache[key]
            logger.debug(f"Cache expired: {key}")
            return None

        logger.debug(f"Cache hit: {key}")
        return entry["value"]

    def set(self, key: str, value: Any) -> None:
        """Store value in cache with TTL."""
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + self.ttl_seconds
        }
        logger.debug(f"Cache set: {key} (TTL: {self.ttl_seconds}s)")

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "entries": len(self.cache),
            "ttl_seconds": self.ttl_seconds
        }
