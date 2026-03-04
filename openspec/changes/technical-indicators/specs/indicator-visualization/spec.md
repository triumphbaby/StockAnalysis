## ADDED Requirements

### Requirement: Display moving averages on main chart
The system SHALL overlay MA lines on the candlestick chart with distinct colors.

#### Scenario: Display MA5, MA10, MA20, MA60 simultaneously
- **WHEN** user selects multiple MA indicators
- **THEN** system displays all MA lines with different colors (MA5=white, MA10=yellow, MA20=pink, MA60=green)

#### Scenario: Toggle MA visibility
- **WHEN** user unchecks MA indicator in selector
- **THEN** system removes that MA line from chart

#### Scenario: MA line follows price data
- **WHEN** user zooms or pans the chart
- **THEN** MA lines update accordingly with visible data range

### Requirement: Display MACD in subplot
The system SHALL render MACD indicator in a separate subplot below the main candlestick chart.

#### Scenario: Render MACD histogram
- **WHEN** MACD indicator is enabled
- **THEN** system displays histogram bars (red for negative, green for positive)

#### Scenario: Render DIF and DEA lines
- **WHEN** MACD subplot is shown
- **THEN** system displays DIF line and DEA line with distinct colors

#### Scenario: Highlight golden cross
- **WHEN** DIF crosses above DEA
- **THEN** system highlights the crossover point

#### Scenario: Highlight death cross
- **WHEN** DIF crosses below DEA
- **THEN** system highlights the crossover point

### Requirement: Display RSI in subplot
The system SHALL render RSI indicator in a separate subplot with overbought/oversold zones.

#### Scenario: Render RSI line
- **WHEN** RSI indicator is enabled
- **THEN** system displays RSI line chart with values 0-100

#### Scenario: Mark overbought zone
- **WHEN** rendering RSI subplot
- **THEN** system draws horizontal line at 70 and shades area above as overbought zone

#### Scenario: Mark oversold zone
- **WHEN** rendering RSI subplot
- **THEN** system draws horizontal line at 30 and shades area below as oversold zone

#### Scenario: Highlight RSI crossing thresholds
- **WHEN** RSI crosses 70 or 30 threshold
- **THEN** system marks the crossover point with a marker

### Requirement: Display KDJ in subplot
The system SHALL render KDJ indicator lines (K, D, J) in a separate subplot.

#### Scenario: Render K, D, J lines
- **WHEN** KDJ indicator is enabled
- **THEN** system displays three lines with distinct colors

#### Scenario: Mark overbought/oversold zones for KDJ
- **WHEN** rendering KDJ subplot
- **THEN** system draws reference lines at 20 and 80

### Requirement: Display Bollinger Bands on main chart
The system SHALL overlay Bollinger Bands (upper, middle, lower) on the candlestick chart.

#### Scenario: Render three Bollinger Band lines
- **WHEN** BOLL indicator is enabled
- **THEN** system displays upper band, middle band, and lower band with distinct styles

#### Scenario: Fill area between bands
- **WHEN** BOLL is displayed
- **THEN** system fills area between upper and lower bands with semi-transparent color

#### Scenario: Highlight price touching bands
- **WHEN** price touches or exceeds band boundaries
- **THEN** system highlights those candlesticks

### Requirement: Support indicator configuration panel
The system SHALL provide UI controls for selecting and configuring indicators.

#### Scenario: Show indicator selector
- **WHEN** user opens indicator configuration
- **THEN** system displays checkboxes for available indicators

#### Scenario: Configure MA periods
- **WHEN** user selects MA indicator
- **THEN** system allows selecting which periods to display (5, 10, 20, 60, etc.)

#### Scenario: Configure MACD parameters
- **WHEN** user selects MACD indicator
- **THEN** system allows setting fast, slow, and signal periods

#### Scenario: Save indicator preferences
- **WHEN** user changes indicator settings
- **THEN** system persists preferences in local storage

### Requirement: Optimize chart performance
The system SHALL render indicators efficiently without degrading chart performance.

#### Scenario: Lazy load indicator data
- **WHEN** user enables new indicator
- **THEN** system loads only necessary data for visible time range

#### Scenario: Downsample data for long periods
- **WHEN** displaying 1+ year of data with indicators
- **THEN** system intelligently downsamples to maintain performance

#### Scenario: Update indicators on data refresh
- **WHEN** stock price data updates
- **THEN** system recalculates and re-renders only affected indicators

### Requirement: Display indicator legend
The system SHALL show a legend explaining indicator lines and their colors.

#### Scenario: Show legend on chart
- **WHEN** multiple indicators are displayed
- **THEN** system shows legend identifying each line/indicator

#### Scenario: Toggle legend visibility
- **WHEN** user clicks legend toggle
- **THEN** system shows/hides legend while keeping indicators visible

#### Scenario: Highlight indicator on legend hover
- **WHEN** user hovers over indicator name in legend
- **THEN** system emphasizes that indicator line on chart
