"""
News Business Logic Service

Handles: collection -> dedup -> classify -> keyword extraction -> storage
"""

import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import logging

from app.models.news import NewsArticle
from app.services.news_api import news_api_service
from app.services.classifier import (
    ClassifierFactory, analyze_sentiment, extract_keywords
)
from app.cache import CacheManager

logger = logging.getLogger(__name__)


class NewsService:
    """News business logic service."""

    def __init__(self, db: Session):
        self.db = db
        self.classifier = ClassifierFactory.create("rule")

    # ---- Collection ----

    def collect_and_store(self) -> int:
        """
        Full pipeline: fetch from NewsAPI -> dedup -> classify -> store.
        Returns number of new articles stored.
        """
        articles = news_api_service.fetch_financial_news(page_size=30)
        if not articles:
            logger.info("No articles fetched from NewsAPI")
            return 0

        stored = 0
        for article in articles:
            # Dedup by URL
            if self._article_exists(article.get("url")):
                continue

            # Classify
            title = article.get("title", "")
            desc = article.get("description", "")
            content = article.get("content", "")
            text = desc + " " + content

            category = self.classifier.classify(title, text)
            sentiment = analyze_sentiment(title, text)
            keywords = extract_keywords(title, text)
            importance = self._calculate_importance(article, category, keywords)

            # Parse published_at
            published_at = None
            if article.get("published_at"):
                try:
                    published_at = datetime.fromisoformat(
                        article["published_at"].replace("Z", "+00:00")
                    )
                except (ValueError, TypeError):
                    published_at = datetime.utcnow()

            # Store
            news = NewsArticle(
                title=title,
                description=desc,
                content=content,
                source=article.get("source", "Unknown"),
                author=article.get("author", ""),
                url=article.get("url", ""),
                image_url=article.get("image_url", ""),
                category=category,
                sentiment=sentiment,
                keywords=json.dumps(keywords, ensure_ascii=False),
                importance_score=importance,
                published_at=published_at,
            )
            self.db.add(news)
            stored += 1

        if stored > 0:
            self.db.commit()
            # Invalidate cache
            CacheManager.clear_pattern("news:list:*")
            CacheManager.delete("news:categories")

        logger.info(f"Stored {stored} new articles (fetched {len(articles)} total)")
        return stored

    def _article_exists(self, url: Optional[str]) -> bool:
        """Check if article URL already exists in database."""
        if not url:
            return False
        return self.db.query(NewsArticle).filter(NewsArticle.url == url).first() is not None

    def _calculate_importance(
        self, article: dict, category: str, keywords: List[str]
    ) -> float:
        """
        Calculate importance score (0-100) based on:
        - Source reputation weight
        - Keyword relevance
        - Recency
        """
        score = 50.0  # Base score

        # Source weight
        high_weight_sources = [
            "财联社", "证券时报", "上海证券报", "中国证券报",
            "Reuters", "Bloomberg", "CNBC", "Wall Street Journal",
        ]
        source = article.get("source", "")
        if any(s.lower() in source.lower() for s in high_weight_sources):
            score += 20

        # Keyword relevance
        score += min(len(keywords) * 5, 20)

        # Category boost
        if category in ("政策法规", "公司公告"):
            score += 10

        return min(score, 100.0)

    # ---- Query ----

    def get_news_list(
        self,
        category: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "published_at",
    ) -> Tuple[List[Dict], int]:
        """
        Get paginated news list with optional filters.

        Returns:
            Tuple of (article_list, total_count)
        """
        query = self.db.query(NewsArticle)

        if category and category != "全部":
            query = query.filter(NewsArticle.category == category)

        if keyword:
            like_pattern = f"%{keyword}%"
            query = query.filter(
                (NewsArticle.title.ilike(like_pattern)) |
                (NewsArticle.description.ilike(like_pattern))
            )

        total = query.count()

        # Sort
        if sort_by == "importance":
            query = query.order_by(desc(NewsArticle.importance_score))
        else:
            query = query.order_by(desc(NewsArticle.published_at))

        # Paginate
        offset = (page - 1) * page_size
        articles = query.offset(offset).limit(page_size).all()

        return [a.to_list_dict() for a in articles], total

    def get_news_detail(self, news_id: int) -> Optional[Dict]:
        """Get single news article by ID."""
        article = self.db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
        if not article:
            return None
        return article.to_dict()

    def get_categories(self) -> List[Dict]:
        """Get categories with article counts."""
        results = (
            self.db.query(
                NewsArticle.category,
                func.count(NewsArticle.id).label("count")
            )
            .group_by(NewsArticle.category)
            .order_by(desc("count"))
            .all()
        )

        total = sum(r.count for r in results)
        categories = [{"name": "全部", "count": total}]
        for r in results:
            categories.append({"name": r.category, "count": r.count})

        return categories
