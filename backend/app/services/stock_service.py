"""
Stock Business Logic Service
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging

from app.models.stock import Stock, StockPrice
from app.services.tushare_service import tushare_service
from app.cache import CacheManager

logger = logging.getLogger(__name__)


class StockService:
    """
    Stock business logic service
    """

    def __init__(self, db: Session):
        self.db = db

    def search_stocks(self, keyword: str, use_cache: bool = True) -> List[Dict]:
        """
        Search stocks by keyword

        Args:
            keyword: Search keyword (code or name)
            use_cache: Whether to use cache

        Returns:
            List of matching stocks
        """
        # Check cache first
        if use_cache:
            cache_key = f"stock:search:{keyword}"
            cached = CacheManager.get(cache_key)
            if cached:
                logger.info(f"Cache hit for search: {keyword}")
                return cached

        # Search in database first
        stocks = self.db.query(Stock).filter(
            (Stock.stock_code.ilike(f"%{keyword}%")) |
            (Stock.name.ilike(f"%{keyword}%"))
        ).limit(20).all()

        if stocks:
            results = [stock.to_dict() for stock in stocks]
        else:
            # Fallback to Tushare API if not in database
            logger.info(f"No local results, searching via Tushare API: {keyword}")
            results = tushare_service.search_stocks(keyword)

        # Cache results
        if use_cache and results:
            cache_key = f"stock:search:{keyword}"
            CacheManager.set(cache_key, results, ttl=3600)  # 1 hour

        return results

    def get_stock_by_code(self, stock_code: str, use_cache: bool = True) -> Optional[Dict]:
        """
        Get stock information by code

        Args:
            stock_code: Stock code
            use_cache: Whether to use cache

        Returns:
            Stock information or None
        """
        # Check cache
        if use_cache:
            cached = CacheManager.get_cached_stock_data(stock_code)
            if cached:
                logger.info(f"Cache hit for stock: {stock_code}")
                return cached

        # Query database
        stock = self.db.query(Stock).filter(Stock.stock_code == stock_code).first()

        if stock:
            result = stock.to_dict()
        else:
            # Fetch from Tushare API
            logger.info(f"Stock not in database, fetching from Tushare: {stock_code}")
            stock_info = tushare_service.get_stock_info(stock_code)
            if not stock_info:
                return None

            # Save to database
            result = self.create_or_update_stock(stock_info)

        # Cache result
        if use_cache and result:
            CacheManager.cache_stock_data(stock_code, result, ttl=86400)  # 1 day

        return result

    def get_stock_prices(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1m",
        use_cache: bool = True
    ) -> List[Dict]:
        """
        Get stock price data

        Args:
            stock_code: Stock code
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            period: Time period (1m/3m/6m/1y/all)
            use_cache: Whether to use cache

        Returns:
            List of price records
        """
        # Parse period
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')

        if not start_date:
            if period == "1m":
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            elif period == "3m":
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
            elif period == "6m":
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
            elif period == "1y":
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            else:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')

        # Check cache
        if use_cache:
            cache_key = f"prices:{stock_code}:{start_date}:{end_date}"
            cached = CacheManager.get(cache_key)
            if cached:
                logger.info(f"Cache hit for prices: {stock_code} {period}")
                return cached

        # Convert string dates to date objects
        start_dt = datetime.strptime(start_date, '%Y%m%d').date()
        end_dt = datetime.strptime(end_date, '%Y%m%d').date()

        # Query database
        prices = self.db.query(StockPrice).filter(
            StockPrice.stock_code == stock_code,
            StockPrice.trade_date >= start_dt,
            StockPrice.trade_date <= end_dt
        ).order_by(StockPrice.trade_date.asc()).all()

        if prices:
            results = [price.to_dict() for price in prices]
        else:
            # Fetch from Tushare API
            logger.info(f"Prices not in database, fetching from Tushare: {stock_code}")
            price_data = tushare_service.get_daily_prices(stock_code, start_date, end_date)

            if price_data:
                # Save to database
                self.save_prices(price_data)
                results = price_data
            else:
                results = []

        # Cache results
        if use_cache and results:
            cache_key = f"prices:{stock_code}:{start_date}:{end_date}"
            CacheManager.set(cache_key, results, ttl=3600)  # 1 hour

        return results

    def create_or_update_stock(self, stock_data: Dict) -> Dict:
        """
        Create or update stock in database

        Args:
            stock_data: Stock data dictionary

        Returns:
            Updated stock dictionary
        """
        stock = self.db.query(Stock).filter(
            Stock.stock_code == stock_data['stock_code']
        ).first()

        if stock:
            # Update existing
            for key, value in stock_data.items():
                if hasattr(stock, key):
                    # Convert date strings to date objects
                    if key in ['listing_date', 'delist_date'] and isinstance(value, str):
                        try:
                            value = datetime.strptime(value, '%Y%m%d').date()
                        except:
                            value = None
                    setattr(stock, key, value)
        else:
            # Create new
            # Convert date strings
            if 'listing_date' in stock_data and isinstance(stock_data['listing_date'], str):
                try:
                    stock_data['listing_date'] = datetime.strptime(stock_data['listing_date'], '%Y%m%d').date()
                except:
                    stock_data['listing_date'] = None

            stock = Stock(
                stock_code=stock_data.get('stock_code'),
                name=stock_data.get('name'),
                name_en=stock_data.get('name_en'),
                market=stock_data.get('market', 'A股'),
                exchange=stock_data.get('exchange'),
                industry=stock_data.get('industry'),
                sector=stock_data.get('sector'),
                listing_date=stock_data.get('listing_date'),
                delist_date=stock_data.get('delist_date'),
                status='active',
                fullname=stock_data.get('fullname'),
                area=stock_data.get('area')
            )
            self.db.add(stock)

        self.db.commit()
        self.db.refresh(stock)

        return stock.to_dict()

    def save_prices(self, price_data: List[Dict]) -> int:
        """
        Save price data to database

        Args:
            price_data: List of price dictionaries

        Returns:
            Number of records saved
        """
        count = 0
        for data in price_data:
            # Check if already exists
            existing = self.db.query(StockPrice).filter(
                StockPrice.stock_code == data['stock_code'],
                StockPrice.trade_date == datetime.strptime(data['trade_date'], '%Y%m%d').date()
            ).first()

            if existing:
                # Update existing
                for key, value in data.items():
                    if hasattr(existing, key) and key != 'trade_date':
                        setattr(existing, key, value)
            else:
                # Create new
                price = StockPrice(
                    stock_code=data['stock_code'],
                    trade_date=datetime.strptime(data['trade_date'], '%Y%m%d').date(),
                    open=data.get('open'),
                    high=data.get('high'),
                    low=data.get('low'),
                    close=data['close'],
                    pre_close=data.get('pre_close'),
                    change=data.get('change'),
                    pct_change=data.get('pct_change'),
                    volume=data.get('volume'),
                    amount=data.get('amount'),
                    turnover_rate=data.get('turnover_rate'),
                    volume_ratio=data.get('volume_ratio'),
                    pe_ratio=data.get('pe_ratio'),
                    pb_ratio=data.get('pb_ratio')
                )
                self.db.add(price)
                count += 1

        self.db.commit()
        logger.info(f"Saved {count} new price records")
        return count

    def sync_stock_list(self) -> int:
        """
        Sync stock list from Tushare to database

        Returns:
            Number of stocks synced
        """
        stocks = tushare_service.get_stock_list()

        count = 0
        for stock_data in stocks:
            self.create_or_update_stock(stock_data)
            count += 1

        logger.info(f"Synced {count} stocks to database")
        return count
