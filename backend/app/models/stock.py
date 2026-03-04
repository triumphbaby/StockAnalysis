"""
Stock Data Models
"""

from sqlalchemy import Column, Integer, String, Date, Float, DateTime, Index, Text
from sqlalchemy.sql import func
from app.database import Base


class Stock(Base):
    """
    Stock basic information table
    股票基本信息表
    """
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(20), unique=True, nullable=False, index=True, comment="股票代码 (e.g., 000001.SZ)")
    name = Column(String(100), nullable=False, comment="股票名称")
    name_en = Column(String(100), comment="英文名称")

    # Classification
    market = Column(String(20), nullable=False, index=True, comment="市场 (A股/港股/美股)")
    exchange = Column(String(20), comment="交易所 (SSE/SZSE/HKEX/NYSE/NASDAQ)")
    industry = Column(String(50), index=True, comment="所属行业")
    sector = Column(String(50), comment="所属板块")

    # Listing info
    listing_date = Column(Date, comment="上市日期")
    delist_date = Column(Date, comment="退市日期")
    status = Column(String(20), default="active", comment="状态 (active/suspended/delisted)")

    # Additional info
    fullname = Column(String(200), comment="公司全称")
    area = Column(String(50), comment="地域")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Indexes
    __table_args__ = (
        Index('idx_stock_name', 'name'),
        Index('idx_stock_market_industry', 'market', 'industry'),
        {'comment': '股票基本信息表'}
    )

    def __repr__(self):
        return f"<Stock(code={self.stock_code}, name={self.name})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "name": self.name,
            "name_en": self.name_en,
            "market": self.market,
            "exchange": self.exchange,
            "industry": self.industry,
            "sector": self.sector,
            "listing_date": self.listing_date.isoformat() if self.listing_date else None,
            "delist_date": self.delist_date.isoformat() if self.delist_date else None,
            "status": self.status,
            "fullname": self.fullname,
            "area": self.area,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class StockPrice(Base):
    """
    Stock price time-series data table
    股票行情时序数据表 (使用 TimescaleDB)
    """
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_code = Column(String(20), nullable=False, index=True, comment="股票代码")
    trade_date = Column(Date, nullable=False, index=True, comment="交易日期")

    # OHLCV data
    open = Column(Float, comment="开盘价")
    high = Column(Float, comment="最高价")
    low = Column(Float, comment="最低价")
    close = Column(Float, nullable=False, comment="收盘价")
    pre_close = Column(Float, comment="前收盘价")
    change = Column(Float, comment="涨跌额")
    pct_change = Column(Float, comment="涨跌幅 (%)")

    # Volume data
    volume = Column(Float, comment="成交量 (手)")
    amount = Column(Float, comment="成交额 (元)")

    # Additional metrics
    turnover_rate = Column(Float, comment="换手率 (%)")
    volume_ratio = Column(Float, comment="量比")
    pe_ratio = Column(Float, comment="市盈率")
    pb_ratio = Column(Float, comment="市净率")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # Indexes
    __table_args__ = (
        Index('idx_stock_code_date', 'stock_code', 'trade_date'),
        Index('idx_trade_date', 'trade_date'),
        {'comment': '股票行情时序数据表'}
    )

    def __repr__(self):
        return f"<StockPrice(code={self.stock_code}, date={self.trade_date}, close={self.close})>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "trade_date": self.trade_date.strftime('%Y%m%d') if self.trade_date else None,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "pre_close": self.pre_close,
            "change": self.change,
            "pct_change": self.pct_change,
            "volume": self.volume,
            "amount": self.amount,
            "turnover_rate": self.turnover_rate,
            "volume_ratio": self.volume_ratio,
            "pe_ratio": self.pe_ratio,
            "pb_ratio": self.pb_ratio,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
