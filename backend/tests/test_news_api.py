"""
Tests for News API Endpoints
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.news_api import NewsAPIService


class TestNewsAPIService:
    """Test NewsAPI service."""

    def test_not_available_without_key(self):
        service = NewsAPIService(api_key="")
        assert service.is_available() is False

    def test_not_available_with_placeholder(self):
        service = NewsAPIService(api_key="your_newsapi_org_key_here")
        assert service.is_available() is False

    def test_normalize_articles(self):
        service = NewsAPIService(api_key="test")
        raw = [
            {
                "title": "Test Article",
                "description": "Test Description",
                "content": "Test Content",
                "source": {"name": "TestSource"},
                "author": "Author",
                "url": "https://example.com/1",
                "urlToImage": "https://example.com/img.jpg",
                "publishedAt": "2026-01-01T00:00:00Z",
            },
            {
                "title": "[Removed]",
                "description": None,
                "content": None,
                "source": {"name": "Removed"},
                "author": None,
                "url": None,
                "urlToImage": None,
                "publishedAt": None,
            },
        ]
        result = service._normalize_articles(raw)
        # [Removed] articles should be filtered out
        assert len(result) == 1
        assert result[0]["title"] == "Test Article"
        assert result[0]["source"] == "TestSource"

    def test_rate_limit_check(self):
        service = NewsAPIService(api_key="test")
        service._request_count = 100
        assert service._check_rate_limit() is False

    def test_rate_limit_reset_on_new_day(self):
        from datetime import date, timedelta
        service = NewsAPIService(api_key="test")
        service._request_count = 100
        service._last_reset = date.today() - timedelta(days=1)
        assert service._check_rate_limit() is True
        assert service._request_count == 0
