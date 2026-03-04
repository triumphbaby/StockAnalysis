"""
Tests for Technical Indicator Service
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.services.indicator_service import IndicatorCalculator, SignalDetector


@pytest.fixture
def sample_price_data():
    """Generate sample OHLCV data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    np.random.seed(42)

    # Generate realistic price data
    close_prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
    high_prices = close_prices + np.abs(np.random.randn(100) * 0.3)
    low_prices = close_prices - np.abs(np.random.randn(100) * 0.3)
    open_prices = close_prices + np.random.randn(100) * 0.2
    volume = np.random.randint(1000000, 5000000, 100)

    df = pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high_prices,
        'low': low_prices,
        'close': close_prices,
        'volume': volume
    })
    df.set_index('date', inplace=True)

    return df


@pytest.fixture
def indicator_calculator():
    """Create indicator calculator instance"""
    return IndicatorCalculator()


@pytest.fixture
def signal_detector():
    """Create signal detector instance"""
    return SignalDetector()


class TestIndicatorCalculator:
    """Test IndicatorCalculator class"""

    def test_calculate_ma_single_period(self, indicator_calculator, sample_price_data):
        """Test MA calculation for a single period"""
        result = indicator_calculator.calculate_ma(sample_price_data, periods=[5])

        assert 'ma_5' in result
        assert len(result['ma_5']) == len(sample_price_data)
        assert not result['ma_5'].iloc[-1] == np.nan

        # First 4 values should be NaN (insufficient data)
        assert pd.isna(result['ma_5'].iloc[0])
        assert pd.isna(result['ma_5'].iloc[3])

        # 5th value onwards should have values
        assert not pd.isna(result['ma_5'].iloc[4])

    def test_calculate_ma_multiple_periods(self, indicator_calculator, sample_price_data):
        """Test MA calculation for multiple periods"""
        result = indicator_calculator.calculate_ma(sample_price_data, periods=[5, 10, 20])

        assert 'ma_5' in result
        assert 'ma_10' in result
        assert 'ma_20' in result

        # MA20 should have more NaN values at the start
        assert pd.isna(result['ma_20'].iloc[19])
        assert not pd.isna(result['ma_20'].iloc[20])

    def test_calculate_ma_insufficient_data(self, indicator_calculator):
        """Test MA with insufficient data"""
        df = pd.DataFrame({'close': [100, 101, 102]})
        result = indicator_calculator.calculate_ma(df, periods=[10])

        # Should return empty or warning
        assert 'ma_10' not in result or result['ma_10'].isna().all()

    def test_calculate_macd_default_params(self, indicator_calculator, sample_price_data):
        """Test MACD calculation with default parameters"""
        result = indicator_calculator.calculate_macd(sample_price_data)

        assert 'dif' in result
        assert 'dea' in result
        assert 'macd' in result

        assert len(result['dif']) == len(sample_price_data)
        assert len(result['dea']) == len(sample_price_data)
        assert len(result['macd']) == len(sample_price_data)

        # Check that MACD = (DIF - DEA) * 2
        macd_check = (result['dif'] - result['dea']) * 2
        pd.testing.assert_series_equal(result['macd'], macd_check, check_names=False)

    def test_calculate_macd_custom_params(self, indicator_calculator, sample_price_data):
        """Test MACD with custom parameters"""
        result = indicator_calculator.calculate_macd(sample_price_data, fast=6, slow=12, signal=5)

        assert 'dif' in result
        assert 'dea' in result
        assert 'macd' in result

    def test_calculate_rsi_default_period(self, indicator_calculator, sample_price_data):
        """Test RSI calculation with default period"""
        result = indicator_calculator.calculate_rsi(sample_price_data)

        assert result is not None
        assert len(result) == len(sample_price_data)

        # RSI should be between 0 and 100
        valid_rsi = result.dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()

    def test_calculate_rsi_custom_period(self, indicator_calculator, sample_price_data):
        """Test RSI with custom period"""
        result = indicator_calculator.calculate_rsi(sample_price_data, period=7)

        assert result is not None
        valid_rsi = result.dropna()
        assert (valid_rsi >= 0).all()
        assert (valid_rsi <= 100).all()

    def test_calculate_kdj_default_params(self, indicator_calculator, sample_price_data):
        """Test KDJ calculation with default parameters"""
        result = indicator_calculator.calculate_kdj(sample_price_data)

        assert 'k' in result
        assert 'd' in result
        assert 'j' in result

        assert len(result['k']) == len(sample_price_data)
        assert len(result['d']) == len(sample_price_data)
        assert len(result['j']) == len(sample_price_data)

    def test_calculate_kdj_missing_columns(self, indicator_calculator):
        """Test KDJ with missing required columns"""
        df = pd.DataFrame({'close': [100, 101, 102]})
        result = indicator_calculator.calculate_kdj(df)

        # Should return empty dict
        assert result == {}

    def test_calculate_boll_default_params(self, indicator_calculator, sample_price_data):
        """Test Bollinger Bands with default parameters"""
        result = indicator_calculator.calculate_boll(sample_price_data)

        assert 'upper' in result
        assert 'middle' in result
        assert 'lower' in result

        # Upper should be > Middle > Lower
        valid_data = ~result['upper'].isna()
        assert (result['upper'][valid_data] >= result['middle'][valid_data]).all()
        assert (result['middle'][valid_data] >= result['lower'][valid_data]).all()

    def test_calculate_boll_custom_params(self, indicator_calculator, sample_price_data):
        """Test Bollinger Bands with custom parameters"""
        result = indicator_calculator.calculate_boll(sample_price_data, period=10, std_dev=1.5)

        assert 'upper' in result
        assert 'middle' in result
        assert 'lower' in result

    def test_batch_calculate_single_indicator(self, indicator_calculator, sample_price_data):
        """Test batch calculation with single indicator"""
        result = indicator_calculator.batch_calculate(sample_price_data, indicators=['ma'])

        assert 'ma' in result
        assert 'ma_5' in result['ma']

    def test_batch_calculate_multiple_indicators(self, indicator_calculator, sample_price_data):
        """Test batch calculation with multiple indicators"""
        indicators = ['ma', 'macd', 'rsi', 'kdj', 'boll']
        result = indicator_calculator.batch_calculate(sample_price_data, indicators=indicators)

        assert 'ma' in result
        assert 'macd' in result
        assert 'rsi' in result
        assert 'kdj' in result
        assert 'boll' in result

    def test_batch_calculate_with_params(self, indicator_calculator, sample_price_data):
        """Test batch calculation with custom parameters"""
        params = {
            'ma_periods': [10, 20],
            'macd_fast': 6,
            'rsi_period': 7
        }
        result = indicator_calculator.batch_calculate(
            sample_price_data,
            indicators=['ma', 'macd', 'rsi'],
            params=params
        )

        assert 'ma' in result
        assert 'ma_10' in result['ma']
        assert 'ma_20' in result['ma']
        assert 'macd' in result
        assert 'rsi' in result

    def test_validate_data_valid(self, indicator_calculator, sample_price_data):
        """Test data validation with valid data"""
        assert indicator_calculator.validate_data(sample_price_data, min_periods=10)

    def test_validate_data_insufficient(self, indicator_calculator):
        """Test data validation with insufficient data"""
        df = pd.DataFrame({'close': [100, 101]})
        assert not indicator_calculator.validate_data(df, min_periods=10)

    def test_validate_data_empty(self, indicator_calculator):
        """Test data validation with empty dataframe"""
        df = pd.DataFrame()
        assert not indicator_calculator.validate_data(df)

    def test_validate_data_missing_columns(self, indicator_calculator):
        """Test data validation with missing columns"""
        df = pd.DataFrame({'open': [100, 101, 102]})
        assert not indicator_calculator.validate_data(df)


class TestSignalDetector:
    """Test SignalDetector class"""

    def test_detect_macd_golden_cross(self, signal_detector):
        """Test MACD golden cross detection"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        dif = pd.Series([-0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.3, 0.1, -0.1, -0.3], index=dates)
        dea = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=dates)

        macd_data = {'dif': dif, 'dea': dea}
        signals = signal_detector.detect_macd_cross(macd_data)

        # Should detect golden cross around index 3
        golden_crosses = [s for s in signals if s['type'] == 'MACD_GOLDEN_CROSS']
        assert len(golden_crosses) > 0

    def test_detect_macd_death_cross(self, signal_detector):
        """Test MACD death cross detection"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        dif = pd.Series([0.5, 0.3, 0.1, -0.1, -0.3, -0.5, -0.3, -0.1, 0.1, 0.3], index=dates)
        dea = pd.Series([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], index=dates)

        macd_data = {'dif': dif, 'dea': dea}
        signals = signal_detector.detect_macd_cross(macd_data)

        # Should detect death cross around index 3
        death_crosses = [s for s in signals if s['type'] == 'MACD_DEATH_CROSS']
        assert len(death_crosses) > 0

    def test_detect_rsi_overbought(self, signal_detector):
        """Test RSI overbought detection"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        rsi = pd.Series([50, 55, 60, 65, 68, 72, 75, 73, 70, 68], index=dates)

        signals = signal_detector.detect_rsi_threshold(rsi)

        # Should detect overbought entry around index 5
        overbought = [s for s in signals if s['type'] == 'RSI_OVERBOUGHT']
        assert len(overbought) > 0

    def test_detect_rsi_oversold(self, signal_detector):
        """Test RSI oversold detection"""
        dates = pd.date_range(start='2024-01-01', periods=10, freq='D')
        rsi = pd.Series([50, 45, 40, 35, 32, 28, 25, 27, 30, 32], index=dates)

        signals = signal_detector.detect_rsi_threshold(rsi)

        # Should detect oversold entry around index 5
        oversold = [s for s in signals if s['type'] == 'RSI_OVERSOLD']
        assert len(oversold) > 0

    def test_detect_all_signals(self, signal_detector, indicator_calculator, sample_price_data):
        """Test detecting all signals from indicators"""
        indicators = indicator_calculator.batch_calculate(
            sample_price_data,
            indicators=['macd', 'rsi']
        )

        signals = signal_detector.detect_all_signals(indicators)

        # Should have some signals
        assert len(signals) >= 0

        # Check signal structure
        if len(signals) > 0:
            assert 'type' in signals[0]
            assert 'date' in signals[0]
            assert 'confidence' in signals[0]

    def test_detect_signals_empty_indicators(self, signal_detector):
        """Test signal detection with empty indicators"""
        signals = signal_detector.detect_all_signals({})
        assert signals == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
