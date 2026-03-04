"""
Standalone test for indicator service
Run without pytest framework
"""

import sys
sys.path.insert(0, 'backend')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.app.services.indicator_service import IndicatorCalculator, SignalDetector


def generate_sample_data():
    """Generate sample OHLCV data"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    np.random.seed(42)

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


def test_ma_calculation():
    """Test MA calculation"""
    print("\n=== Testing MA Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    result = calc.calculate_ma(df, periods=[5, 10, 20])

    print(f"✓ MA5 calculated: {len(result['ma_5'])} points")
    print(f"✓ MA10 calculated: {len(result['ma_10'])} points")
    print(f"✓ MA20 calculated: {len(result['ma_20'])} points")

    # Show last 5 values
    print(f"\nLast 5 MA values:")
    print(f"  Close: {df['close'].tail().values}")
    print(f"  MA5:   {result['ma_5'].tail().values}")
    print(f"  MA20:  {result['ma_20'].tail().values}")

    return True


def test_macd_calculation():
    """Test MACD calculation"""
    print("\n=== Testing MACD Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    result = calc.calculate_macd(df)

    print(f"✓ DIF calculated: {len(result['dif'])} points")
    print(f"✓ DEA calculated: {len(result['dea'])} points")
    print(f"✓ MACD calculated: {len(result['macd'])} points")

    # Show last 5 values
    print(f"\nLast 5 MACD values:")
    print(f"  DIF:  {result['dif'].tail().values}")
    print(f"  DEA:  {result['dea'].tail().values}")
    print(f"  MACD: {result['macd'].tail().values}")

    return True


def test_rsi_calculation():
    """Test RSI calculation"""
    print("\n=== Testing RSI Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    result = calc.calculate_rsi(df, period=14)

    print(f"✓ RSI calculated: {len(result)} points")

    # Show last 10 values
    print(f"\nLast 10 RSI values:")
    print(f"  {result.tail(10).values}")

    # Check range
    valid_rsi = result.dropna()
    print(f"✓ RSI range check: min={valid_rsi.min():.2f}, max={valid_rsi.max():.2f}")

    assert (valid_rsi >= 0).all(), "RSI should be >= 0"
    assert (valid_rsi <= 100).all(), "RSI should be <= 100"

    return True


def test_kdj_calculation():
    """Test KDJ calculation"""
    print("\n=== Testing KDJ Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    result = calc.calculate_kdj(df)

    print(f"✓ K line calculated: {len(result['k'])} points")
    print(f"✓ D line calculated: {len(result['d'])} points")
    print(f"✓ J line calculated: {len(result['j'])} points")

    # Show last 5 values
    print(f"\nLast 5 KDJ values:")
    print(f"  K: {result['k'].tail().values}")
    print(f"  D: {result['d'].tail().values}")
    print(f"  J: {result['j'].tail().values}")

    return True


def test_boll_calculation():
    """Test Bollinger Bands calculation"""
    print("\n=== Testing Bollinger Bands Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    result = calc.calculate_boll(df, period=20, std_dev=2.0)

    print(f"✓ Upper band calculated: {len(result['upper'])} points")
    print(f"✓ Middle band calculated: {len(result['middle'])} points")
    print(f"✓ Lower band calculated: {len(result['lower'])} points")

    # Show last 5 values
    print(f"\nLast 5 BOLL values:")
    print(f"  Upper:  {result['upper'].tail().values}")
    print(f"  Middle: {result['middle'].tail().values}")
    print(f"  Lower:  {result['lower'].tail().values}")

    # Check upper > middle > lower
    valid = ~result['upper'].isna()
    assert (result['upper'][valid] >= result['middle'][valid]).all()
    assert (result['middle'][valid] >= result['lower'][valid]).all()
    print("✓ Band ordering verified (upper >= middle >= lower)")

    return True


def test_batch_calculation():
    """Test batch calculation"""
    print("\n=== Testing Batch Calculation ===")
    calc = IndicatorCalculator()
    df = generate_sample_data()

    indicators = ['ma', 'macd', 'rsi', 'kdj', 'boll']
    result = calc.batch_calculate(df, indicators=indicators)

    print(f"✓ Batch calculated {len(result)} indicators")
    for indicator in indicators:
        assert indicator in result, f"Missing indicator: {indicator}"
        print(f"  • {indicator}: {type(result[indicator])}")

    return True


def test_signal_detection():
    """Test signal detection"""
    print("\n=== Testing Signal Detection ===")
    calc = IndicatorCalculator()
    detector = SignalDetector()
    df = generate_sample_data()

    # Calculate indicators
    indicators = calc.batch_calculate(df, indicators=['macd', 'rsi'])

    # Detect signals
    signals = detector.detect_all_signals(indicators)

    print(f"✓ Detected {len(signals)} signals")

    # Show signals
    if signals:
        print("\nDetected signals:")
        for i, signal in enumerate(signals[:10]):  # Show first 10
            print(f"  {i+1}. {signal['type']} on {signal['date'].date()} (confidence: {signal['confidence']})")

    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("TECHNICAL INDICATOR SERVICE - STANDALONE TESTS")
    print("=" * 60)

    tests = [
        ("MA Calculation", test_ma_calculation),
        ("MACD Calculation", test_macd_calculation),
        ("RSI Calculation", test_rsi_calculation),
        ("KDJ Calculation", test_kdj_calculation),
        ("Bollinger Bands Calculation", test_boll_calculation),
        ("Batch Calculation", test_batch_calculation),
        ("Signal Detection", test_signal_detection),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            print(f"\n✅ {test_name}: PASSED")
            passed += 1
        except Exception as e:
            print(f"\n❌ {test_name}: FAILED")
            print(f"   Error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"TEST SUMMARY: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 60)

    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
