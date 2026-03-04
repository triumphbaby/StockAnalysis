"""
Stock API Routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.services.stock_service import StockService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Pydantic models for request/response
class StockInfo(BaseModel):
    """Stock information response model"""
    id: Optional[int] = None
    stock_code: str
    name: str
    name_en: Optional[str] = None
    market: str
    exchange: Optional[str] = None
    industry: Optional[str] = None
    sector: Optional[str] = None
    listing_date: Optional[str] = None
    delist_date: Optional[str] = None
    status: Optional[str] = None
    fullname: Optional[str] = None
    area: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class StockPrice(BaseModel):
    """Stock price response model"""
    id: Optional[int] = None
    stock_code: str
    trade_date: str
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: float
    pre_close: Optional[float] = None
    change: Optional[float] = None
    pct_change: Optional[float] = None
    volume: Optional[float] = None
    amount: Optional[float] = None
    turnover_rate: Optional[float] = None
    volume_ratio: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    """Search response model"""
    total: int
    data: List[dict]


class PricesResponse(BaseModel):
    """Prices response model"""
    stock_code: str
    period: str
    total: int
    data: List[dict]


@router.get("/search", response_model=SearchResponse)
async def search_stocks(
    keyword: str = Query(..., min_length=1, description="Search keyword (stock code or name)"),
    db: Session = Depends(get_db)
):
    """
    Search stocks by keyword

    Args:
        keyword: Search keyword (stock code or name)

    Returns:
        List of matching stocks
    """
    try:
        service = StockService(db)
        results = service.search_stocks(keyword)

        return {
            "total": len(results),
            "data": results
        }

    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching stocks: {str(e)}")


@router.get("/{stock_code}", response_model=dict)
async def get_stock(
    stock_code: str,
    db: Session = Depends(get_db)
):
    """
    Get stock information by code

    Args:
        stock_code: Stock code (e.g., 000001.SZ)

    Returns:
        Stock information
    """
    try:
        service = StockService(db)
        stock = service.get_stock_by_code(stock_code)

        if not stock:
            raise HTTPException(status_code=404, detail=f"Stock {stock_code} not found")

        return stock

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching stock {stock_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stock: {str(e)}")


@router.get("/{stock_code}/prices", response_model=PricesResponse)
async def get_stock_prices(
    stock_code: str,
    period: str = Query("1m", description="Time period (1m/3m/6m/1y/all)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYYMMDD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYYMMDD)"),
    db: Session = Depends(get_db)
):
    """
    Get stock price data

    Args:
        stock_code: Stock code (e.g., 000001.SZ)
        period: Time period (1m/3m/6m/1y/all)
        start_date: Start date (YYYYMMDD), optional
        end_date: End date (YYYYMMDD), optional

    Returns:
        Price data for the specified period
    """
    try:
        service = StockService(db)

        # Validate period
        valid_periods = ["1m", "3m", "6m", "1y", "all"]
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
            )

        prices = service.get_stock_prices(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date,
            period=period
        )

        return {
            "stock_code": stock_code,
            "period": period,
            "total": len(prices),
            "data": prices
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching prices for {stock_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")


@router.post("/sync")
async def sync_stock_list(db: Session = Depends(get_db)):
    """
    Sync stock list from Tushare to database

    Returns:
        Number of stocks synced
    """
    try:
        service = StockService(db)
        count = service.sync_stock_list()

        return {
            "status": "success",
            "count": count,
            "message": f"Successfully synced {count} stocks"
        }

    except Exception as e:
        logger.error(f"Error syncing stock list: {e}")
        raise HTTPException(status_code=500, detail=f"Error syncing stocks: {str(e)}")
