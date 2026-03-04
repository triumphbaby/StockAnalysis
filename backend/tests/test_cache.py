"""
Test Redis Cache Operations
"""

import pytest
from unittest.mock import MagicMock, patch
from app.cache import CacheManager


@pytest.fixture
def mock_redis_client():
    """
    Mock Redis client for testing
    """
    with patch('app.cache.redis_client') as mock:
        yield mock


def test_cache_set(mock_redis_client):
    """
    Test setting a value in cache
    """
    mock_redis_client.setex.return_value = True

    result = CacheManager.set("test_key", {"data": "test"}, ttl=300)

    assert result is True
    mock_redis_client.setex.assert_called_once()


def test_cache_get(mock_redis_client):
    """
    Test getting a value from cache
    """
    import json
    mock_redis_client.get.return_value = json.dumps({"data": "test"})

    result = CacheManager.get("test_key")

    assert result == {"data": "test"}
    mock_redis_client.get.assert_called_once_with("test_key")


def test_cache_get_nonexistent(mock_redis_client):
    """
    Test getting a non-existent key returns None
    """
    mock_redis_client.get.return_value = None

    result = CacheManager.get("nonexistent_key")

    assert result is None


def test_cache_delete(mock_redis_client):
    """
    Test deleting a key from cache
    """
    mock_redis_client.delete.return_value = 1

    result = CacheManager.delete("test_key")

    assert result is True
    mock_redis_client.delete.assert_called_once_with("test_key")


def test_cache_exists(mock_redis_client):
    """
    Test checking if a key exists
    """
    mock_redis_client.exists.return_value = 1

    result = CacheManager.exists("test_key")

    assert result is True
    mock_redis_client.exists.assert_called_once_with("test_key")


def test_cache_stock_data(mock_redis_client):
    """
    Test caching stock data
    """
    mock_redis_client.setex.return_value = True

    stock_data = {"code": "000001", "price": 10.5}
    result = CacheManager.cache_stock_data("000001", stock_data)

    assert result is True
    # Verify the key format
    call_args = mock_redis_client.setex.call_args
    assert call_args[0][0] == "stock:000001:data"


def test_get_cached_stock_data(mock_redis_client):
    """
    Test getting cached stock data
    """
    import json
    stock_data = {"code": "000001", "price": 10.5}
    mock_redis_client.get.return_value = json.dumps(stock_data)

    result = CacheManager.get_cached_stock_data("000001")

    assert result == stock_data
    mock_redis_client.get.assert_called_once_with("stock:000001:data")
