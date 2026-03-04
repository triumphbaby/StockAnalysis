"""
NewsAPI.org Integration Service

Free tier limits:
- 100 requests/day
- Articles up to 1 month old
- Content truncated to 200 chars
"""

import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
import time

from app.config import settings

logger = logging.getLogger(__name__)

NEWSAPI_BASE_URL = "https://newsapi.org/v2"

# Financial/stock-related search keywords
DEFAULT_KEYWORDS = [
    "stock market", "finance", "economy",
    "股票", "A股", "财经", "金融", "经济",
]


class NewsAPIService:
    """
    Service for fetching news from NewsAPI.org.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.NEWS_API_KEY
        self._request_count = 0
        self._last_reset = datetime.now().date()

    def is_available(self) -> bool:
        return bool(self.api_key) and self.api_key != "your_newsapi_org_key_here"

    def _check_rate_limit(self) -> bool:
        """Check if we're within daily rate limit."""
        today = datetime.now().date()
        if today != self._last_reset:
            self._request_count = 0
            self._last_reset = today

        if self._request_count >= settings.NEWS_API_DAILY_LIMIT:
            logger.warning("NewsAPI daily rate limit reached")
            return False
        return True

    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """Make a request to NewsAPI with error handling."""
        if not self.is_available():
            logger.error("NewsAPI key not configured")
            return None

        if not self._check_rate_limit():
            return None

        params["apiKey"] = self.api_key
        url = f"{NEWSAPI_BASE_URL}/{endpoint}"

        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(url, params=params)
                self._request_count += 1

                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "ok":
                        return data
                    else:
                        logger.error(f"NewsAPI error: {data.get('message', 'Unknown')}")
                        return None
                elif response.status_code == 429:
                    logger.warning("NewsAPI rate limited (429)")
                    return None
                else:
                    logger.error(f"NewsAPI HTTP {response.status_code}: {response.text[:200]}")
                    return None

        except httpx.TimeoutException:
            logger.error("NewsAPI request timed out")
            return None
        except Exception as e:
            logger.error(f"NewsAPI request error: {e}")
            return None

    def fetch_top_headlines(
        self,
        country: str = "cn",
        category: str = "business",
        page_size: int = 20,
        page: int = 1,
    ) -> List[Dict]:
        """
        Fetch top business headlines.

        Args:
            country: Country code (cn, us, etc.)
            category: News category (business, technology, etc.)
            page_size: Number of results per page (max 100)
            page: Page number

        Returns:
            List of article dicts
        """
        params = {
            "country": country,
            "category": category,
            "pageSize": min(page_size, 100),
            "page": page,
        }

        data = self._make_request("top-headlines", params)
        if not data:
            return []

        return self._normalize_articles(data.get("articles", []))

    def fetch_everything(
        self,
        query: str = "股票 OR 财经 OR finance OR stock market",
        language: Optional[str] = None,
        sort_by: str = "publishedAt",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page_size: int = 20,
        page: int = 1,
    ) -> List[Dict]:
        """
        Search all articles matching the query.

        Args:
            query: Search keywords
            language: Language filter (zh, en, etc.)
            sort_by: Sort order (publishedAt, relevancy, popularity)
            from_date: Start date (ISO 8601)
            to_date: End date (ISO 8601)
            page_size: Results per page
            page: Page number

        Returns:
            List of article dicts
        """
        params = {
            "q": query,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "page": page,
        }

        if language:
            params["language"] = language
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        data = self._make_request("everything", params)
        if not data:
            return []

        return self._normalize_articles(data.get("articles", []))

    def fetch_financial_news(self, page_size: int = 30) -> List[Dict]:
        """
        Convenience method to fetch financial news using multiple queries.
        Combines Chinese business headlines + English financial search.

        Returns:
            Combined deduplicated list of articles
        """
        all_articles = []

        # 1. Chinese business headlines
        cn_articles = self.fetch_top_headlines(
            country="cn", category="business", page_size=page_size
        )
        all_articles.extend(cn_articles)

        # 2. English financial news search
        en_articles = self.fetch_everything(
            query="stock market OR finance OR economy",
            language="en",
            sort_by="publishedAt",
            page_size=page_size,
        )
        all_articles.extend(en_articles)

        # Deduplicate by URL
        seen_urls = set()
        unique = []
        for article in all_articles:
            url = article.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(article)

        logger.info(f"Fetched {len(unique)} unique financial news articles")
        return unique

    def _normalize_articles(self, articles: list) -> List[Dict]:
        """Normalize NewsAPI article format to our standard format."""
        normalized = []
        for article in articles:
            if not article.get("title") or article["title"] == "[Removed]":
                continue

            normalized.append({
                "title": article.get("title", "").strip(),
                "description": (article.get("description") or "").strip(),
                "content": (article.get("content") or "").strip(),
                "source": article.get("source", {}).get("name", "Unknown"),
                "author": (article.get("author") or "").strip(),
                "url": article.get("url", ""),
                "image_url": article.get("urlToImage", ""),
                "published_at": article.get("publishedAt"),
            })

        return normalized


# Singleton
news_api_service = NewsAPIService()
