"""
Test Stock API Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch


def test_search_stocks_success(client: TestClient):
    """
    Test stock search API returns results
    """
    with patch('app.services.stock_service.StockService.search_stocks') as mock_search:
        mock_search.return_value = [
            {
                'stock_code': '000001.SZ',
                'name': '平安银行',
                'market': 'A股',
                'industry': '银行'
            }
        ]

        response = client.get("/api/stocks/search?keyword=平安")

        assert response.status_code == 200
        data = response.json()
        assert data['total'] == 1
        assert len(data['data']) == 1
        assert data['data'][0]['stock_code'] == '000001.SZ'


def test_search_stocks_empty_keyword(client: TestClient):
    """
    Test stock search with empty keyword returns 422
    """
    response = client.get("/api/stocks/search")

    # Missing required parameter
    assert response.status_code == 422


def test_get_stock_info_success(client: TestClient):
    """
    Test get stock information by code
    """
    with patch('app.services.stock_service.StockService.get_stock_by_code') as mock_get:
        mock_get.return_value = {
            'stock_code': '000001.SZ',
            'name': '平安银行',
            'fullname': '平安银行股份有限公司',
            'market': 'A股',
            'exchange': 'SZSE',
            'industry': '银行',
            'status': 'active'
        }

        response = client.get("/api/stocks/000001.SZ")

        assert response.status_code == 200
        data = response.json()
        assert data['stock_code'] == '000001.SZ'
        assert data['name'] == '平安银行'
        assert data['status'] == 'active'


def test_get_stock_info_not_found(client: TestClient):
    """
    Test get stock information for non-existent stock
    """
    with patch('app.services.stock_service.StockService.get_stock_by_code') as mock_get:
        mock_get.return_value = None

        response = client.get("/api/stocks/INVALID.SZ")

        assert response.status_code == 404
        assert 'not found' in response.json()['detail'].lower()


def test_get_stock_prices_success(client: TestClient):
    """
    Test get stock prices
    """
    with patch('app.services.stock_service.StockService.get_stock_prices') as mock_prices:
        mock_prices.return_value = [
            {
                'stock_code': '000001.SZ',
                'trade_date': '20240101',
                'open': 10.0,
                'high': 10.5,
                'low': 9.8,
                'close': 10.2,
                'volume': 1000000
            }
        ]

        response = client.get("/api/stocks/000001.SZ/prices?period=1m")

        assert response.status_code == 200
        data = response.json()
        assert data['stock_code'] == '000001.SZ'
        assert data['period'] == '1m'
        assert data['total'] == 1
        assert len(data['data']) == 1


def test_get_stock_prices_invalid_period(client: TestClient):
    """
    Test get stock prices with invalid period
    """
    response = client.get("/api/stocks/000001.SZ/prices?period=invalid")

    assert response.status_code == 400
    assert 'invalid period' in response.json()['detail'].lower()


def test_sync_stock_list_success(client: TestClient):
    """
    Test sync stock list from Tushare
    """
    with patch('app.services.stock_service.StockService.sync_stock_list') as mock_sync:
        mock_sync.return_value = 100

        response = client.post("/api/stocks/sync")

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert data['count'] == 100
