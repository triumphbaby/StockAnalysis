"""
Seed Data Script - Initialize database with stock data via Tushare API.

Usage:
    python -m app.scripts.seed_data

If Tushare token is not configured, generates mock data for development.
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal, engine, Base
from app.models.stock import Stock, StockPrice
from app.services.tushare_service import tushare_service
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Popular A-share stocks for seeding
SEED_STOCKS = [
    {"stock_code": "000001.SZ", "name": "平安银行", "market": "A股", "exchange": "SZSE", "industry": "银行", "sector": "金融", "area": "深圳", "fullname": "平安银行股份有限公司"},
    {"stock_code": "600000.SH", "name": "浦发银行", "market": "A股", "exchange": "SSE", "industry": "银行", "sector": "金融", "area": "上海", "fullname": "上海浦东发展银行股份有限公司"},
    {"stock_code": "600519.SH", "name": "贵州茅台", "market": "A股", "exchange": "SSE", "industry": "白酒", "sector": "消费", "area": "贵州", "fullname": "贵州茅台酒股份有限公司"},
    {"stock_code": "000858.SZ", "name": "五粮液", "market": "A股", "exchange": "SZSE", "industry": "白酒", "sector": "消费", "area": "四川", "fullname": "宜宾五粮液股份有限公司"},
    {"stock_code": "601318.SH", "name": "中国平安", "market": "A股", "exchange": "SSE", "industry": "保险", "sector": "金融", "area": "深圳", "fullname": "中国平安保险(集团)股份有限公司"},
    {"stock_code": "600036.SH", "name": "招商银行", "market": "A股", "exchange": "SSE", "industry": "银行", "sector": "金融", "area": "深圳", "fullname": "招商银行股份有限公司"},
    {"stock_code": "000333.SZ", "name": "美的集团", "market": "A股", "exchange": "SZSE", "industry": "家电", "sector": "制造", "area": "广东", "fullname": "美的集团股份有限公司"},
    {"stock_code": "002594.SZ", "name": "比亚迪", "market": "A股", "exchange": "SZSE", "industry": "汽车", "sector": "制造", "area": "广东", "fullname": "比亚迪股份有限公司"},
    {"stock_code": "601012.SH", "name": "隆基绿能", "market": "A股", "exchange": "SSE", "industry": "光伏", "sector": "新能源", "area": "陕西", "fullname": "隆基绿能科技股份有限公司"},
    {"stock_code": "300750.SZ", "name": "宁德时代", "market": "A股", "exchange": "SZSE", "industry": "电池", "sector": "新能源", "area": "福建", "fullname": "宁德时代新能源科技股份有限公司"},
]

# Base prices for mock generation
BASE_PRICES = {
    "000001.SZ": 12.0, "600000.SH": 8.0, "600519.SH": 1700.0, "000858.SZ": 150.0,
    "601318.SH": 45.0, "600036.SH": 35.0, "000333.SZ": 55.0, "002594.SZ": 250.0,
    "601012.SH": 25.0, "300750.SZ": 180.0,
}


def generate_mock_prices(stock_code: str, days: int = 180) -> list:
    """Generate realistic mock price data for a stock."""
    base_price = BASE_PRICES.get(stock_code, 20.0)
    prices = []
    current_price = base_price
    today = datetime.now().date()

    for i in range(days - 1, -1, -1):
        trade_date = today - timedelta(days=i)
        # Skip weekends
        if trade_date.weekday() >= 5:
            continue

        # Random walk with slight upward bias
        pct_change = random.gauss(0.001, 0.02)  # mean 0.1%, std 2%
        open_price = current_price * (1 + random.gauss(0, 0.005))
        close_price = current_price * (1 + pct_change)
        high_price = max(open_price, close_price) * (1 + abs(random.gauss(0, 0.008)))
        low_price = min(open_price, close_price) * (1 - abs(random.gauss(0, 0.008)))
        volume = random.randint(300000, 2000000)

        prices.append({
            "stock_code": stock_code,
            "trade_date": trade_date,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "pre_close": round(current_price, 2),
            "change": round(close_price - current_price, 2),
            "pct_change": round(pct_change * 100, 2),
            "volume": volume,
            "amount": round(volume * close_price, 2),
        })
        current_price = close_price

    return prices


def seed_stocks(db):
    """Seed stock basic information."""
    count = 0
    for stock_data in SEED_STOCKS:
        existing = db.query(Stock).filter(Stock.stock_code == stock_data["stock_code"]).first()
        if existing:
            logger.info(f"Stock {stock_data['stock_code']} already exists, skipping")
            continue

        stock = Stock(
            stock_code=stock_data["stock_code"],
            name=stock_data["name"],
            market=stock_data["market"],
            exchange=stock_data["exchange"],
            industry=stock_data["industry"],
            sector=stock_data["sector"],
            area=stock_data["area"],
            fullname=stock_data["fullname"],
            status="active",
        )
        db.add(stock)
        count += 1

    db.commit()
    logger.info(f"Seeded {count} stocks")
    return count


def seed_prices(db, days: int = 180):
    """Seed price data - use Tushare if available, else mock data."""
    total = 0

    for stock_data in SEED_STOCKS:
        code = stock_data["stock_code"]

        # Check if prices already exist
        existing_count = db.query(StockPrice).filter(StockPrice.stock_code == code).count()
        if existing_count > 50:
            logger.info(f"Stock {code} already has {existing_count} price records, skipping")
            continue

        # Try Tushare first
        if tushare_service.is_available():
            logger.info(f"Fetching prices from Tushare for {code}...")
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            price_list = tushare_service.get_daily_prices(code, start_date, end_date)

            if price_list:
                for p in price_list:
                    price = StockPrice(
                        stock_code=p["stock_code"],
                        trade_date=datetime.strptime(p["trade_date"], '%Y%m%d').date(),
                        open=p.get("open"),
                        high=p.get("high"),
                        low=p.get("low"),
                        close=p["close"],
                        pre_close=p.get("pre_close"),
                        change=p.get("change"),
                        pct_change=p.get("pct_change"),
                        volume=p.get("volume"),
                        amount=p.get("amount"),
                    )
                    db.add(price)
                total += len(price_list)
                db.commit()
                logger.info(f"Saved {len(price_list)} Tushare prices for {code}")
                continue

        # Fallback: generate mock data
        logger.info(f"Generating mock prices for {code}...")
        mock_prices = generate_mock_prices(code, days)
        for p in mock_prices:
            price = StockPrice(
                stock_code=p["stock_code"],
                trade_date=p["trade_date"],
                open=p["open"],
                high=p["high"],
                low=p["low"],
                close=p["close"],
                pre_close=p["pre_close"],
                change=p["change"],
                pct_change=p["pct_change"],
                volume=p["volume"],
                amount=p["amount"],
            )
            db.add(price)
        total += len(mock_prices)
        db.commit()
        logger.info(f"Saved {len(mock_prices)} mock prices for {code}")

    logger.info(f"Seeded {total} total price records")
    return total


def main():
    """Run seed data script."""
    logger.info("=" * 60)
    logger.info("Starting seed data script...")
    logger.info("=" * 60)

    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ensured")

    db = SessionLocal()
    try:
        # Seed stocks
        stock_count = seed_stocks(db)
        logger.info(f"Stocks seeded: {stock_count}")

        # Seed prices
        price_count = seed_prices(db)
        logger.info(f"Prices seeded: {price_count}")

        logger.info("=" * 60)
        logger.info("Seed data completed successfully!")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
