"""
Tushare Pro API Integration Service
"""

import tushare as ts
import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class TushareService:
    """
    Tushare Pro API service for fetching stock data
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initialize Tushare service

        Args:
            token: Tushare API token (if not provided, will use settings.TUSHARE_TOKEN)
        """
        self.token = token or settings.TUSHARE_TOKEN
        if not self.token or self.token == "your_tushare_token_here":
            logger.warning("Tushare token not configured. Some features may not work.")
            self.pro = None
        else:
            try:
                ts.set_token(self.token)
                self.pro = ts.pro_api()
                logger.info("Tushare API initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Tushare API: {e}")
                self.pro = None

    def is_available(self) -> bool:
        """Check if Tushare API is available"""
        return self.pro is not None

    def get_stock_list(
        self,
        exchange: Optional[str] = None,
        status: str = "L"
    ) -> List[Dict]:
        """
        Get stock list

        Args:
            exchange: Exchange code (SSE/SZSE/BSE)
            status: Stock status (L=Listed, D=Delisted, P=Paused)

        Returns:
            List of stock dictionaries
        """
        if not self.is_available():
            logger.error("Tushare API not available")
            return []

        try:
            df = self.pro.stock_basic(
                exchange=exchange,
                list_status=status,
                fields='ts_code,symbol,name,area,industry,market,list_date'
            )

            if df is None or df.empty:
                return []

            stocks = []
            for _, row in df.iterrows():
                stocks.append({
                    'stock_code': row['ts_code'],
                    'symbol': row['symbol'],
                    'name': row['name'],
                    'area': row['area'],
                    'industry': row['industry'],
                    'market': row['market'],
                    'listing_date': row['list_date']
                })

            logger.info(f"Retrieved {len(stocks)} stocks from Tushare")
            return stocks

        except Exception as e:
            logger.error(f"Error fetching stock list: {e}")
            return []

    def get_stock_info(self, stock_code: str) -> Optional[Dict]:
        """
        Get detailed stock information

        Args:
            stock_code: Stock code (e.g., 000001.SZ)

        Returns:
            Stock information dictionary or None
        """
        if not self.is_available():
            logger.error("Tushare API not available")
            return None

        try:
            df = self.pro.stock_basic(
                ts_code=stock_code,
                fields='ts_code,symbol,name,area,industry,fullname,market,exchange,list_date,delist_date'
            )

            if df is None or df.empty:
                logger.warning(f"Stock {stock_code} not found")
                return None

            row = df.iloc[0]
            return {
                'stock_code': row['ts_code'],
                'symbol': row['symbol'],
                'name': row['name'],
                'fullname': row['fullname'],
                'area': row['area'],
                'industry': row['industry'],
                'market': row['market'],
                'exchange': row['exchange'],
                'listing_date': row['list_date'],
                'delist_date': row['delist_date'] if pd.notna(row['delist_date']) else None
            }

        except Exception as e:
            logger.error(f"Error fetching stock info for {stock_code}: {e}")
            return None

    def get_daily_prices(
        self,
        stock_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Get daily price data

        Args:
            stock_code: Stock code (e.g., 000001.SZ)
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            limit: Maximum number of records

        Returns:
            List of price dictionaries
        """
        if not self.is_available():
            logger.error("Tushare API not available")
            return []

        # Default date range: last 3 months
        if not end_date:
            end_date = datetime.now().strftime('%Y%m%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')

        try:
            df = self.pro.daily(
                ts_code=stock_code,
                start_date=start_date,
                end_date=end_date
            )

            if df is None or df.empty:
                logger.warning(f"No price data found for {stock_code}")
                return []

            # Sort by date ascending
            df = df.sort_values('trade_date')

            # Limit results
            if len(df) > limit:
                df = df.tail(limit)

            prices = []
            for _, row in df.iterrows():
                prices.append({
                    'stock_code': row['ts_code'],
                    'trade_date': row['trade_date'],
                    'open': float(row['open']) if pd.notna(row['open']) else None,
                    'high': float(row['high']) if pd.notna(row['high']) else None,
                    'low': float(row['low']) if pd.notna(row['low']) else None,
                    'close': float(row['close']),
                    'pre_close': float(row['pre_close']) if pd.notna(row['pre_close']) else None,
                    'change': float(row['change']) if pd.notna(row['change']) else None,
                    'pct_change': float(row['pct_chg']) if pd.notna(row['pct_chg']) else None,
                    'volume': float(row['vol']) if pd.notna(row['vol']) else None,
                    'amount': float(row['amount']) if pd.notna(row['amount']) else None,
                })

            logger.info(f"Retrieved {len(prices)} price records for {stock_code}")
            return prices

        except Exception as e:
            logger.error(f"Error fetching daily prices for {stock_code}: {e}")
            return []

    def get_realtime_quote(self, stock_codes: List[str]) -> List[Dict]:
        """
        Get real-time quotes (Note: This requires VIP account)

        Args:
            stock_codes: List of stock codes

        Returns:
            List of quote dictionaries
        """
        if not self.is_available():
            logger.error("Tushare API not available")
            return []

        try:
            # For demo purposes, use daily data as fallback
            quotes = []
            for code in stock_codes:
                df = self.pro.daily(
                    ts_code=code,
                    start_date=datetime.now().strftime('%Y%m%d'),
                    end_date=datetime.now().strftime('%Y%m%d')
                )

                if df is not None and not df.empty:
                    row = df.iloc[0]
                    quotes.append({
                        'stock_code': code,
                        'close': float(row['close']),
                        'change': float(row['change']) if pd.notna(row['change']) else None,
                        'pct_change': float(row['pct_chg']) if pd.notna(row['pct_chg']) else None,
                        'volume': float(row['vol']) if pd.notna(row['vol']) else None,
                    })

            return quotes

        except Exception as e:
            logger.error(f"Error fetching realtime quotes: {e}")
            return []

    def search_stocks(self, keyword: str) -> List[Dict]:
        """
        Search stocks by name or code

        Args:
            keyword: Search keyword (stock code or name)

        Returns:
            List of matching stocks
        """
        if not self.is_available():
            logger.error("Tushare API not available")
            return []

        try:
            # Get all stocks
            df = self.pro.stock_basic(
                list_status='L',
                fields='ts_code,symbol,name,area,industry,market,list_date'
            )

            if df is None or df.empty:
                return []

            # Filter by keyword (case-insensitive)
            keyword_lower = keyword.lower()
            filtered = df[
                df['ts_code'].str.lower().str.contains(keyword_lower) |
                df['symbol'].str.lower().str.contains(keyword_lower) |
                df['name'].str.lower().str.contains(keyword_lower)
            ]

            results = []
            for _, row in filtered.head(20).iterrows():  # Limit to 20 results
                results.append({
                    'stock_code': row['ts_code'],
                    'symbol': row['symbol'],
                    'name': row['name'],
                    'area': row['area'],
                    'industry': row['industry'],
                    'market': row['market'],
                    'listing_date': row['list_date']
                })

            logger.info(f"Found {len(results)} stocks matching '{keyword}'")
            return results

        except Exception as e:
            logger.error(f"Error searching stocks: {e}")
            return []


# Singleton instance
tushare_service = TushareService()
