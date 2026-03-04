"""
Test Tushare Service
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.tushare_service import TushareService
import pandas as pd


@pytest.fixture
def tushare_service_mock():
    """
    Create a TushareService with mocked Tushare API
    """
    with patch('tushare.set_token'), patch('tushare.pro_api') as mock_pro:
        service = TushareService(token="test_token")
        service.pro = mock_pro.return_value
        return service


def test_tushare_service_initialization():
    """
    Test TushareService initialization
    """
    with patch('tushare.set_token'), patch('tushare.pro_api'):
        service = TushareService(token="test_token")
        assert service.is_available() is True


def test_tushare_service_no_token():
    """
    Test TushareService initialization without token
    """
    service = TushareService(token=None)
    assert service.is_available() is False


def test_get_stock_list(tushare_service_mock):
    """
    Test get stock list
    """
    # Mock DataFrame
    mock_df = pd.DataFrame({
        'ts_code': ['000001.SZ', '000002.SZ'],
        'symbol': ['000001', '000002'],
        'name': ['平安银行', '万科A'],
        'area': ['深圳', '深圳'],
        'industry': ['银行', '房地产'],
        'market': ['主板', '主板'],
        'list_date': ['19910403', '19910129']
    })

    tushare_service_mock.pro.stock_basic.return_value = mock_df

    results = tushare_service_mock.get_stock_list()

    assert len(results) == 2
    assert results[0]['stock_code'] == '000001.SZ'
    assert results[0]['name'] == '平安银行'
    assert results[1]['stock_code'] == '000002.SZ'


def test_get_stock_info(tushare_service_mock):
    """
    Test get stock information
    """
    mock_df = pd.DataFrame({
        'ts_code': ['000001.SZ'],
        'symbol': ['000001'],
        'name': ['平安银行'],
        'fullname': ['平安银行股份有限公司'],
        'area': ['深圳'],
        'industry': ['银行'],
        'market': ['主板'],
        'exchange': ['SZSE'],
        'list_date': ['19910403'],
        'delist_date': [None]
    })

    tushare_service_mock.pro.stock_basic.return_value = mock_df

    result = tushare_service_mock.get_stock_info('000001.SZ')

    assert result is not None
    assert result['stock_code'] == '000001.SZ'
    assert result['name'] == '平安银行'
    assert result['industry'] == '银行'


def test_get_stock_info_not_found(tushare_service_mock):
    """
    Test get stock information for non-existent stock
    """
    tushare_service_mock.pro.stock_basic.return_value = pd.DataFrame()

    result = tushare_service_mock.get_stock_info('INVALID.SZ')

    assert result is None


def test_get_daily_prices(tushare_service_mock):
    """
    Test get daily price data
    """
    mock_df = pd.DataFrame({
        'ts_code': ['000001.SZ', '000001.SZ'],
        'trade_date': ['20240101', '20240102'],
        'open': [10.0, 10.2],
        'high': [10.5, 10.6],
        'low': [9.8, 10.0],
        'close': [10.2, 10.4],
        'pre_close': [9.9, 10.2],
        'change': [0.3, 0.2],
        'pct_chg': [3.03, 1.96],
        'vol': [1000000, 1200000],
        'amount': [102000000, 124800000]
    })

    tushare_service_mock.pro.daily.return_value = mock_df

    results = tushare_service_mock.get_daily_prices('000001.SZ')

    assert len(results) == 2
    assert results[0]['stock_code'] == '000001.SZ'
    assert results[0]['close'] == 10.2
    assert results[1]['close'] == 10.4


def test_search_stocks(tushare_service_mock):
    """
    Test search stocks by keyword
    """
    mock_df = pd.DataFrame({
        'ts_code': ['000001.SZ', '600000.SH'],
        'symbol': ['000001', '600000'],
        'name': ['平安银行', '浦发银行'],
        'area': ['深圳', '上海'],
        'industry': ['银行', '银行'],
        'market': ['主板', '主板'],
        'list_date': ['19910403', '19991110']
    })

    tushare_service_mock.pro.stock_basic.return_value = mock_df

    results = tushare_service_mock.search_stocks('银行')

    assert len(results) == 2
    assert all('银行' in stock['name'] for stock in results)
