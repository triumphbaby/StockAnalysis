"""
Redis Cache Manager
"""

import redis
import json
from typing import Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create Redis client
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)


class CacheManager:
    """
    Redis cache manager for storing and retrieving data
    """

    @staticmethod
    def set(key: str, value: Any, ttl: int = None) -> bool:
        """
        Set a value in cache with optional TTL

        Args:
            key: Cache key
            value: Value to store (will be JSON serialized)
            ttl: Time to live in seconds (None for no expiration)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            serialized_value = json.dumps(value)
            if ttl:
                redis_client.setex(key, ttl, serialized_value)
            else:
                redis_client.set(key, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False

    @staticmethod
    def get(key: str) -> Optional[Any]:
        """
        Get a value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return None

    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete a key from cache

        Args:
            key: Cache key

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False

    @staticmethod
    def exists(key: str) -> bool:
        """
        Check if a key exists in cache

        Args:
            key: Cache key

        Returns:
            bool: True if exists, False otherwise
        """
        try:
            return redis_client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False

    @staticmethod
    def clear_pattern(pattern: str) -> int:
        """
        Clear all keys matching a pattern

        Args:
            pattern: Key pattern (e.g., "stock:*")

        Returns:
            int: Number of keys deleted
        """
        try:
            keys = redis_client.keys(pattern)
            if keys:
                return redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {e}")
            return 0

    @staticmethod
    def cache_stock_data(stock_code: str, data: dict, ttl: int = settings.CACHE_TTL_SHORT) -> bool:
        """
        Cache stock data

        Args:
            stock_code: Stock code
            data: Stock data to cache
            ttl: Time to live in seconds

        Returns:
            bool: True if successful
        """
        key = f"stock:{stock_code}:data"
        return CacheManager.set(key, data, ttl)

    @staticmethod
    def get_cached_stock_data(stock_code: str) -> Optional[dict]:
        """
        Get cached stock data

        Args:
            stock_code: Stock code

        Returns:
            Cached stock data or None
        """
        key = f"stock:{stock_code}:data"
        return CacheManager.get(key)

    @staticmethod
    def cache_analysis_result(stock_code: str, result: dict, ttl: int = settings.CACHE_TTL_MEDIUM) -> bool:
        """
        Cache analysis result

        Args:
            stock_code: Stock code
            result: Analysis result
            ttl: Time to live in seconds

        Returns:
            bool: True if successful
        """
        key = f"analysis:{stock_code}"
        return CacheManager.set(key, result, ttl)

    @staticmethod
    def get_cached_analysis_result(stock_code: str) -> Optional[dict]:
        """
        Get cached analysis result

        Args:
            stock_code: Stock code

        Returns:
            Cached analysis result or None
        """
        key = f"analysis:{stock_code}"
        return CacheManager.get(key)


# Export singleton instance
cache = CacheManager()
