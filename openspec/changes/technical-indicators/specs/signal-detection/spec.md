## ADDED Requirements

### Requirement: Detect MACD golden cross signal
The system SHALL identify when MACD DIF line crosses above DEA line as a bullish signal.

#### Scenario: Detect MACD golden cross
- **WHEN** DIF crosses from below to above DEA
- **THEN** system generates "MACD Golden Cross" signal with timestamp and price

#### Scenario: Ignore false signals
- **WHEN** DIF and DEA lines are very close (< 0.01 difference)
- **THEN** system does not generate signal to avoid noise

### Requirement: Detect MACD death cross signal
The system SHALL identify when MACD DIF line crosses below DEA line as a bearish signal.

#### Scenario: Detect MACD death cross
- **WHEN** DIF crosses from above to below DEA
- **THEN** system generates "MACD Death Cross" signal with timestamp and price

### Requirement: Detect MA golden cross signal
The system SHALL identify when fast MA crosses above slow MA as a bullish signal.

#### Scenario: Detect MA5 crosses above MA20
- **WHEN** MA5 crosses from below to above MA20
- **THEN** system generates "MA Golden Cross (5/20)" signal

#### Scenario: Detect MA10 crosses above MA60
- **WHEN** MA10 crosses from below to above MA60
- **THEN** system generates "MA Golden Cross (10/60)" signal

### Requirement: Detect MA death cross signal
The system SHALL identify when fast MA crosses below slow MA as a bearish signal.

#### Scenario: Detect MA5 crosses below MA20
- **WHEN** MA5 crosses from above to below MA20
- **THEN** system generates "MA Death Cross (5/20)" signal

### Requirement: Detect RSI overbought signal
The system SHALL identify when RSI enters overbought zone as a potential sell signal.

#### Scenario: RSI crosses above 70
- **WHEN** RSI value crosses from below 70 to above 70
- **THEN** system generates "RSI Overbought" signal

#### Scenario: RSI exits overbought zone
- **WHEN** RSI crosses back below 70
- **THEN** system generates "RSI Overbought Exit" signal

### Requirement: Detect RSI oversold signal
The system SHALL identify when RSI enters oversold zone as a potential buy signal.

#### Scenario: RSI crosses below 30
- **WHEN** RSI value crosses from above 30 to below 30
- **THEN** system generates "RSI Oversold" signal

#### Scenario: RSI exits oversold zone
- **WHEN** RSI crosses back above 30
- **THEN** system generates "RSI Oversold Exit" signal

### Requirement: Detect KDJ golden cross signal
The system SHALL identify when K line crosses above D line as a bullish signal.

#### Scenario: K crosses above D
- **WHEN** K line crosses from below to above D line
- **THEN** system generates "KDJ Golden Cross" signal

#### Scenario: KDJ golden cross in oversold zone
- **WHEN** K crosses above D and both are below 20
- **THEN** system generates "KDJ Strong Buy" signal with higher confidence

### Requirement: Detect KDJ death cross signal
The system SHALL identify when K line crosses below D line as a bearish signal.

#### Scenario: K crosses below D
- **WHEN** K line crosses from above to below D line
- **THEN** system generates "KDJ Death Cross" signal

#### Scenario: KDJ death cross in overbought zone
- **WHEN** K crosses below D and both are above 80
- **THEN** system generates "KDJ Strong Sell" signal with higher confidence

### Requirement: Detect Bollinger Band breakout signal
The system SHALL identify when price breaks out of Bollinger Bands.

#### Scenario: Price breaks above upper band
- **WHEN** close price exceeds upper Bollinger Band
- **THEN** system generates "BOLL Upper Breakout" signal

#### Scenario: Price breaks below lower band
- **WHEN** close price falls below lower Bollinger Band
- **THEN** system generates "BOLL Lower Breakout" signal

#### Scenario: Price returns inside bands
- **WHEN** price moves back between bands after breakout
- **THEN** system generates "BOLL Band Return" signal

### Requirement: Assign signal confidence levels
The system SHALL assign confidence scores to signals based on multiple indicator confirmation.

#### Scenario: Multiple indicators confirm bullish signal
- **WHEN** MACD golden cross AND RSI oversold exit occur within 3 days
- **THEN** system assigns "High Confidence" to buy signal

#### Scenario: Single indicator signal
- **WHEN** only one indicator generates signal
- **THEN** system assigns "Low Confidence" to signal

#### Scenario: Conflicting signals
- **WHEN** bullish and bearish signals occur simultaneously
- **THEN** system assigns "Conflicting" status and shows both

### Requirement: Provide signal history
The system SHALL maintain a history of all detected signals for a stock.

#### Scenario: Query recent signals
- **WHEN** user requests signals for a stock
- **THEN** system returns all signals from last 90 days

#### Scenario: Filter signals by type
- **WHEN** user filters for "Golden Cross" signals only
- **THEN** system returns only MACD and MA golden cross signals

#### Scenario: Export signal history
- **WHEN** user requests signal export
- **THEN** system provides CSV/JSON with signal type, date, price, and confidence

### Requirement: Real-time signal notification
The system SHALL detect and notify new signals as data updates.

#### Scenario: Detect signal on latest data
- **WHEN** new price data creates a signal condition
- **THEN** system immediately generates signal and notifies user

#### Scenario: Avoid duplicate notifications
- **WHEN** same signal persists across multiple data points
- **THEN** system sends notification only once when signal first appears

### Requirement: Validate signal accuracy
The system SHALL calculate signal accuracy metrics over time.

#### Scenario: Track signal performance
- **WHEN** system generates a signal
- **THEN** system tracks subsequent price movement to measure signal effectiveness

#### Scenario: Calculate signal success rate
- **WHEN** user views signal history
- **THEN** system displays percentage of signals that resulted in expected price movement
