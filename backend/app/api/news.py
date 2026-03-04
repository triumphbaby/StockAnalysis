"""
News API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.database import get_db
from app.services.news_service import NewsService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def get_news_list(
    category: Optional[str] = Query(None, description="Filter by category"),
    keyword: Optional[str] = Query(None, description="Search keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sort_by: str = Query("published_at", description="Sort by field (published_at, importance)"),
    db: Session = Depends(get_db),
):
    """
    Get paginated news list with optional category/keyword filters.
    """
    try:
        service = NewsService(db)
        articles, total = service.get_news_list(
            category=category,
            keyword=keyword,
            page=page,
            page_size=page_size,
            sort_by=sort_by,
        )

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "data": articles,
        }

    except Exception as e:
        logger.error(f"Error fetching news list: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/categories")
async def get_news_categories(
    db: Session = Depends(get_db),
):
    """
    Get news categories with article counts.
    """
    try:
        service = NewsService(db)
        categories = service.get_categories()
        return {"data": categories}

    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching categories: {str(e)}")


@router.get("/{news_id}")
async def get_news_detail(
    news_id: int,
    db: Session = Depends(get_db),
):
    """
    Get news article detail by ID.
    """
    try:
        service = NewsService(db)
        article = service.get_news_detail(news_id)

        if not article:
            raise HTTPException(status_code=404, detail="News article not found")

        return article

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching news {news_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.post("/collect")
async def trigger_collection(
    db: Session = Depends(get_db),
):
    """
    Manually trigger news collection (for testing).
    """
    try:
        service = NewsService(db)
        count = service.collect_and_store()
        return {
            "status": "success",
            "collected": count,
            "message": f"Collected {count} new articles",
        }

    except Exception as e:
        logger.error(f"Error collecting news: {e}")
        raise HTTPException(status_code=500, detail=f"Error collecting news: {str(e)}")
