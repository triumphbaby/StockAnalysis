"""Initial stock tables

Revision ID: 001
Revises:
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create stocks table
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stock_code', sa.String(length=20), nullable=False, comment='股票代码 (e.g., 000001.SZ)'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='股票名称'),
        sa.Column('name_en', sa.String(length=100), nullable=True, comment='英文名称'),
        sa.Column('market', sa.String(length=20), nullable=False, comment='市场 (A股/港股/美股)'),
        sa.Column('exchange', sa.String(length=20), nullable=True, comment='交易所 (SSE/SZSE/HKEX/NYSE/NASDAQ)'),
        sa.Column('industry', sa.String(length=50), nullable=True, comment='所属行业'),
        sa.Column('sector', sa.String(length=50), nullable=True, comment='所属板块'),
        sa.Column('listing_date', sa.Date(), nullable=True, comment='上市日期'),
        sa.Column('delist_date', sa.Date(), nullable=True, comment='退市日期'),
        sa.Column('status', sa.String(length=20), nullable=True, comment='状态 (active/suspended/delisted)'),
        sa.Column('fullname', sa.String(length=200), nullable=True, comment='公司全称'),
        sa.Column('area', sa.String(length=50), nullable=True, comment='地域'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='更新时间'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('stock_code'),
        comment='股票基本信息表'
    )

    # Create indexes for stocks table
    op.create_index('idx_stock_name', 'stocks', ['name'], unique=False)
    op.create_index('idx_stock_market_industry', 'stocks', ['market', 'industry'], unique=False)
    op.create_index(op.f('ix_stocks_id'), 'stocks', ['id'], unique=False)
    op.create_index(op.f('ix_stocks_stock_code'), 'stocks', ['stock_code'], unique=True)
    op.create_index(op.f('ix_stocks_market'), 'stocks', ['market'], unique=False)
    op.create_index(op.f('ix_stocks_industry'), 'stocks', ['industry'], unique=False)

    # Create stock_prices table
    op.create_table(
        'stock_prices',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('stock_code', sa.String(length=20), nullable=False, comment='股票代码'),
        sa.Column('trade_date', sa.Date(), nullable=False, comment='交易日期'),
        sa.Column('open', sa.Float(), nullable=True, comment='开盘价'),
        sa.Column('high', sa.Float(), nullable=True, comment='最高价'),
        sa.Column('low', sa.Float(), nullable=True, comment='最低价'),
        sa.Column('close', sa.Float(), nullable=False, comment='收盘价'),
        sa.Column('pre_close', sa.Float(), nullable=True, comment='前收盘价'),
        sa.Column('change', sa.Float(), nullable=True, comment='涨跌额'),
        sa.Column('pct_change', sa.Float(), nullable=True, comment='涨跌幅 (%)'),
        sa.Column('volume', sa.Float(), nullable=True, comment='成交量 (手)'),
        sa.Column('amount', sa.Float(), nullable=True, comment='成交额 (元)'),
        sa.Column('turnover_rate', sa.Float(), nullable=True, comment='换手率 (%)'),
        sa.Column('volume_ratio', sa.Float(), nullable=True, comment='量比'),
        sa.Column('pe_ratio', sa.Float(), nullable=True, comment='市盈率'),
        sa.Column('pb_ratio', sa.Float(), nullable=True, comment='市净率'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.PrimaryKeyConstraint('id'),
        comment='股票行情时序数据表'
    )

    # Create indexes for stock_prices table
    op.create_index('idx_stock_code_date', 'stock_prices', ['stock_code', 'trade_date'], unique=False)
    op.create_index('idx_trade_date', 'stock_prices', ['trade_date'], unique=False)
    op.create_index(op.f('ix_stock_prices_id'), 'stock_prices', ['id'], unique=False)
    op.create_index(op.f('ix_stock_prices_stock_code'), 'stock_prices', ['stock_code'], unique=False)
    op.create_index(op.f('ix_stock_prices_trade_date'), 'stock_prices', ['trade_date'], unique=False)

    # Create TimescaleDB hypertable for stock_prices (if TimescaleDB is available)
    # Note: This requires TimescaleDB extension to be enabled
    op.execute("""
        SELECT create_hypertable('stock_prices', 'trade_date', if_not_exists => TRUE);
    """)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_stock_prices_trade_date'), table_name='stock_prices')
    op.drop_index(op.f('ix_stock_prices_stock_code'), table_name='stock_prices')
    op.drop_index(op.f('ix_stock_prices_id'), table_name='stock_prices')
    op.drop_index('idx_trade_date', table_name='stock_prices')
    op.drop_index('idx_stock_code_date', table_name='stock_prices')
    op.drop_table('stock_prices')

    op.drop_index(op.f('ix_stocks_industry'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_market'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_stock_code'), table_name='stocks')
    op.drop_index(op.f('ix_stocks_id'), table_name='stocks')
    op.drop_index('idx_stock_market_industry', table_name='stocks')
    op.drop_index('idx_stock_name', table_name='stocks')
    op.drop_table('stocks')
