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
from app.services.indicator_service import IndicatorCalculator
import pandas as pd
import numpy as np
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


@router.get("/{stock_code}/prices")
async def get_stock_prices(
    stock_code: str,
    period: str = Query("1m", description="Time period (1m/3m/6m/1y/all)"),
    start_date: Optional[str] = Query(None, description="Start date (YYYYMMDD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYYMMDD)"),
    indicators: Optional[str] = Query(None, description="Comma-separated indicators (ma,macd,rsi,kdj,boll)"),
    db: Session = Depends(get_db)
):
    """
    Get stock price data with optional technical indicators

    Args:
        stock_code: Stock code (e.g., 000001.SZ)
        period: Time period (1m/3m/6m/1y/all)
        start_date: Start date (YYYYMMDD), optional
        end_date: End date (YYYYMMDD), optional
        indicators: Comma-separated indicator names (ma,macd,rsi,kdj,boll)

    Returns:
        Price data with optional indicators for the specified period
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

        response = {
            "stock_code": stock_code,
            "period": period,
            "total": len(prices),
            "data": prices
        }

        # Calculate indicators if requested
        if indicators and prices:
            indicator_list = [i.strip().lower() for i in indicators.split(',') if i.strip()]
            if indicator_list:
                response["indicators"] = _calculate_indicators(prices, indicator_list)

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching prices for {stock_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching prices: {str(e)}")


def _calculate_indicators(prices: List[dict], indicator_list: List[str]) -> dict:
    """
    Calculate technical indicators from price data.
    Returns indicators as arrays aligned with price data indices.
    """
    # Build DataFrame from price dicts
    df = pd.DataFrame(prices)
    # Ensure numeric columns
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    calculator = IndicatorCalculator()
    result = {}

    def series_to_list(s):
        """Convert pandas Series to JSON-safe list"""
        if s is None:
            return []
        return [None if (pd.isna(v) or np.isinf(v)) else round(float(v), 4) for v in s]

    if 'ma' in indicator_list:
        ma_data = calculator.calculate_ma(df, periods=[5, 10, 20, 60])
        result['ma'] = {
            'ma5': series_to_list(ma_data.get('ma_5')),
            'ma10': series_to_list(ma_data.get('ma_10')),
            'ma20': series_to_list(ma_data.get('ma_20')),
            'ma60': series_to_list(ma_data.get('ma_60')),
        }

    if 'macd' in indicator_list:
        macd_data = calculator.calculate_macd(df)
        result['macd'] = {
            'dif': series_to_list(macd_data.get('dif')),
            'dea': series_to_list(macd_data.get('dea')),
            'macd': series_to_list(macd_data.get('macd')),
        }

    if 'rsi' in indicator_list:
        rsi_data = calculator.calculate_rsi(df)
        result['rsi'] = {
            'rsi': series_to_list(rsi_data),
        }

    if 'kdj' in indicator_list:
        kdj_data = calculator.calculate_kdj(df)
        result['kdj'] = {
            'k': series_to_list(kdj_data.get('k')),
            'd': series_to_list(kdj_data.get('d')),
            'j': series_to_list(kdj_data.get('j')),
        }

    if 'boll' in indicator_list:
        boll_data = calculator.calculate_boll(df)
        result['boll'] = {
            'upper': series_to_list(boll_data.get('upper')),
            'middle': series_to_list(boll_data.get('middle')),
            'lower': series_to_list(boll_data.get('lower')),
        }

    return result


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
