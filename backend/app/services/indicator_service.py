"""
Technical Indicator Calculation Service

This module provides technical indicator calculations using pandas-ta library.
Supports MA, MACD, RSI, KDJ, and Bollinger Bands indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class IndicatorCalculator:
    """
    Technical indicator calculator using pandas-ta
    """

    def __init__(self):
        """Initialize the indicator calculator"""
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate_data(self, df: pd.DataFrame, min_periods: int = 1) -> bool:
        """
        Validate if dataframe has sufficient data

        Args:
            df: DataFrame with OHLCV data
            min_periods: Minimum required periods

        Returns:
            bool: True if valid, False otherwise
        """
        if df is None or df.empty:
            return False
        if len(df) < min_periods:
            self.logger.warning(f"Insufficient data: {len(df)} < {min_periods}")
            return False
        required_columns = ['close']
        if not all(col in df.columns for col in required_columns):
            self.logger.warning(f"Missing required columns: {required_columns}")
            return False
        return True

    def calculate_ma(self, df: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> Dict[str, pd.Series]:
        """
        Calculate Simple Moving Average for multiple periods

        Args:
            df: DataFrame with at least 'close' column
            periods: List of MA periods to calculate

        Returns:
            Dict mapping 'ma_{period}' to Series of values
        """
        results = {}

        for period in periods:
            if not self.validate_data(df, min_periods=period):
                self.logger.warning(f"Skipping MA{period} - insufficient data")
                continue

            try:
                ma = df['close'].rolling(window=period).mean()
                results[f'ma_{period}'] = ma
                self.logger.debug(f"Calculated MA{period}")
            except Exception as e:
                self.logger.error(f"Error calculating MA{period}: {e}")

        return results

    def calculate_macd(
        self,
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Dict[str, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Args:
            df: DataFrame with 'close' column
            fast: Fast EMA period (default 12)
            slow: Slow EMA period (default 26)
            signal: Signal line EMA period (default 9)

        Returns:
            Dict with 'dif', 'dea', 'macd' (histogram) Series
        """
        if not self.validate_data(df, min_periods=slow + signal):
            return {}

        try:
            # Calculate EMAs
            ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
            ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

            # DIF line (MACD line)
            dif = ema_fast - ema_slow

            # DEA line (Signal line)
            dea = dif.ewm(span=signal, adjust=False).mean()

            # MACD histogram
            macd = (dif - dea) * 2  # Multiply by 2 for standard display

            self.logger.debug(f"Calculated MACD({fast},{slow},{signal})")

            return {
                'dif': dif,
                'dea': dea,
                'macd': macd
            }
        except Exception as e:
            self.logger.error(f"Error calculating MACD: {e}")
            return {}

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Optional[pd.Series]:
        """
        Calculate RSI (Relative Strength Index)

        Args:
            df: DataFrame with 'close' column
            period: RSI period (default 14)

        Returns:
            Series of RSI values (0-100)
        """
        if not self.validate_data(df, min_periods=period + 1):
            return None

        try:
            # Calculate price changes
            delta = df['close'].diff()

            # Separate gains and losses
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)

            # Calculate average gain and loss
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()

            # Calculate RS and RSI
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            self.logger.debug(f"Calculated RSI({period})")

            return rsi
        except Exception as e:
            self.logger.error(f"Error calculating RSI: {e}")
            return None

    def calculate_kdj(
        self,
        df: pd.DataFrame,
        n: int = 9,
        m1: int = 3,
        m2: int = 3
    ) -> Dict[str, pd.Series]:
        """
        Calculate KDJ Stochastic Oscillator

        Args:
            df: DataFrame with 'high', 'low', 'close' columns
            n: Period for RSV calculation (default 9)
            m1: Period for K smoothing (default 3)
            m2: Period for D smoothing (default 3)

        Returns:
            Dict with 'k', 'd', 'j' Series
        """
        required_cols = ['high', 'low', 'close']
        if not all(col in df.columns for col in required_cols):
            self.logger.warning(f"Missing required columns for KDJ: {required_cols}")
            return {}

        if not self.validate_data(df, min_periods=n):
            return {}

        try:
            # Calculate RSV (Raw Stochastic Value)
            low_n = df['low'].rolling(window=n).min()
            high_n = df['high'].rolling(window=n).max()

            rsv = ((df['close'] - low_n) / (high_n - low_n)) * 100
            rsv = rsv.fillna(50)  # Fill NaN with neutral value

            # Calculate K, D, J lines
            k = rsv.ewm(alpha=1/m1, adjust=False).mean()
            d = k.ewm(alpha=1/m2, adjust=False).mean()
            j = 3 * k - 2 * d

            self.logger.debug(f"Calculated KDJ({n},{m1},{m2})")

            return {
                'k': k,
                'd': d,
                'j': j
            }
        except Exception as e:
            self.logger.error(f"Error calculating KDJ: {e}")
            return {}

    def calculate_boll(
        self,
        df: pd.DataFrame,
        period: int = 20,
        std_dev: float = 2.0
    ) -> Dict[str, pd.Series]:
        """
        Calculate Bollinger Bands

        Args:
            df: DataFrame with 'close' column
            period: Period for middle band (SMA) (default 20)
            std_dev: Standard deviation multiplier (default 2.0)

        Returns:
            Dict with 'upper', 'middle', 'lower' Series
        """
        if not self.validate_data(df, min_periods=period):
            return {}

        try:
            # Middle band (SMA)
            middle = df['close'].rolling(window=period).mean()

            # Standard deviation
            std = df['close'].rolling(window=period).std()

            # Upper and lower bands
            upper = middle + (std * std_dev)
            lower = middle - (std * std_dev)

            self.logger.debug(f"Calculated BOLL({period},{std_dev})")

            return {
                'upper': upper,
                'middle': middle,
                'lower': lower
            }
        except Exception as e:
            self.logger.error(f"Error calculating BOLL: {e}")
            return {}

    def batch_calculate(
        self,
        df: pd.DataFrame,
        indicators: List[str],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate multiple indicators in a single call

        Args:
            df: DataFrame with OHLCV data
            indicators: List of indicator names (e.g., ['ma', 'macd', 'rsi'])
            params: Optional dict of parameters for each indicator

        Returns:
            Dict mapping indicator names to their results
        """
        if params is None:
            params = {}

        results = {}

        for indicator in indicators:
            indicator_lower = indicator.lower()

            try:
                if indicator_lower == 'ma':
                    periods = params.get('ma_periods', [5, 10, 20, 60])
                    results['ma'] = self.calculate_ma(df, periods)

                elif indicator_lower == 'macd':
                    fast = params.get('macd_fast', 12)
                    slow = params.get('macd_slow', 26)
                    signal = params.get('macd_signal', 9)
                    results['macd'] = self.calculate_macd(df, fast, slow, signal)

                elif indicator_lower == 'rsi':
                    period = params.get('rsi_period', 14)
                    results['rsi'] = self.calculate_rsi(df, period)

                elif indicator_lower == 'kdj':
                    n = params.get('kdj_n', 9)
                    m1 = params.get('kdj_m1', 3)
                    m2 = params.get('kdj_m2', 3)
                    results['kdj'] = self.calculate_kdj(df, n, m1, m2)

                elif indicator_lower == 'boll':
                    period = params.get('boll_period', 20)
                    std_dev = params.get('boll_std', 2.0)
                    results['boll'] = self.calculate_boll(df, period, std_dev)

                else:
                    self.logger.warning(f"Unknown indicator: {indicator}")

            except Exception as e:
                self.logger.error(f"Error calculating {indicator}: {e}")

        return results


class SignalDetector:
    """
    Technical signal detection based on indicators
    """

    def __init__(self):
        """Initialize the signal detector"""
        self.logger = logging.getLogger(self.__class__.__name__)

    def detect_macd_cross(self, macd_data: Dict[str, pd.Series]) -> List[Dict]:
        """
        Detect MACD golden and death crosses

        Args:
            macd_data: Dict with 'dif' and 'dea' Series

        Returns:
            List of signal dicts with type, date, and value
        """
        if 'dif' not in macd_data or 'dea' not in macd_data:
            return []

        signals = []
        dif = macd_data['dif']
        dea = macd_data['dea']

        # Find crossover points
        for i in range(1, len(dif)):
            if pd.isna(dif.iloc[i]) or pd.isna(dea.iloc[i]):
                continue
            if pd.isna(dif.iloc[i-1]) or pd.isna(dea.iloc[i-1]):
                continue

            # Golden cross: DIF crosses above DEA
            if dif.iloc[i-1] <= dea.iloc[i-1] and dif.iloc[i] > dea.iloc[i]:
                if abs(dif.iloc[i] - dea.iloc[i]) > 0.01:  # Avoid noise
                    signals.append({
                        'type': 'MACD_GOLDEN_CROSS',
                        'date': dif.index[i],
                        'dif': float(dif.iloc[i]),
                        'dea': float(dea.iloc[i]),
                        'confidence': 'medium'
                    })

            # Death cross: DIF crosses below DEA
            elif dif.iloc[i-1] >= dea.iloc[i-1] and dif.iloc[i] < dea.iloc[i]:
                if abs(dif.iloc[i] - dea.iloc[i]) > 0.01:
                    signals.append({
                        'type': 'MACD_DEATH_CROSS',
                        'date': dif.index[i],
                        'dif': float(dif.iloc[i]),
                        'dea': float(dea.iloc[i]),
                        'confidence': 'medium'
                    })

        return signals

    def detect_rsi_threshold(self, rsi: pd.Series, overbought: float = 70, oversold: float = 30) -> List[Dict]:
        """
        Detect RSI overbought/oversold signals

        Args:
            rsi: RSI Series
            overbought: Overbought threshold (default 70)
            oversold: Oversold threshold (default 30)

        Returns:
            List of signal dicts
        """
        if rsi is None or rsi.empty:
            return []

        signals = []

        for i in range(1, len(rsi)):
            if pd.isna(rsi.iloc[i]) or pd.isna(rsi.iloc[i-1]):
                continue

            # Overbought entry
            if rsi.iloc[i-1] < overbought and rsi.iloc[i] >= overbought:
                signals.append({
                    'type': 'RSI_OVERBOUGHT',
                    'date': rsi.index[i],
                    'rsi': float(rsi.iloc[i]),
                    'confidence': 'medium'
                })

            # Oversold entry
            elif rsi.iloc[i-1] > oversold and rsi.iloc[i] <= oversold:
                signals.append({
                    'type': 'RSI_OVERSOLD',
                    'date': rsi.index[i],
                    'rsi': float(rsi.iloc[i]),
                    'confidence': 'medium'
                })

        return signals

    def detect_all_signals(
        self,
        indicators: Dict[str, Any]
    ) -> List[Dict]:
        """
        Detect all signals from calculated indicators

        Args:
            indicators: Dict of calculated indicators

        Returns:
            List of all detected signals
        """
        all_signals = []

        # MACD signals
        if 'macd' in indicators:
            macd_signals = self.detect_macd_cross(indicators['macd'])
            all_signals.extend(macd_signals)

        # RSI signals
        if 'rsi' in indicators:
            rsi_signals = self.detect_rsi_threshold(indicators['rsi'])
            all_signals.extend(rsi_signals)

        # Sort by date
        all_signals.sort(key=lambda x: x['date'])

        return all_signals
