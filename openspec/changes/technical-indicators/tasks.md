## 1. Environment Setup

- [ ] 1.1 Add pandas-ta to backend/requirements.txt
- [ ] 1.2 Install pandas-ta in backend container
- [ ] 1.3 Verify pandas-ta installation with test import

## 2. Backend - Indicator Service

- [ ] 2.1 Create app/services/indicator_service.py file
- [ ] 2.2 Implement IndicatorCalculator base class
- [ ] 2.3 Implement calculate_ma() method (Simple Moving Average)
- [ ] 2.4 Implement calculate_macd() method (MACD indicator)
- [ ] 2.5 Implement calculate_rsi() method (RSI indicator)
- [ ] 2.6 Implement calculate_kdj() method (KDJ indicator)
- [ ] 2.7 Implement calculate_boll() method (Bollinger Bands)
- [ ] 2.8 Implement batch_calculate() method for multiple indicators
- [ ] 2.9 Add parameter validation for all indicators
- [ ] 2.10 Add error handling for edge cases (missing data, insufficient data points)

## 3. Backend - Signal Detection

- [ ] 3.1 Create SignalDetector class in indicator_service.py
- [ ] 3.2 Implement detect_macd_cross() method (golden/death cross)
- [ ] 3.3 Implement detect_ma_cross() method (MA golden/death cross)
- [ ] 3.4 Implement detect_rsi_threshold() method (overbought/oversold)
- [ ] 3.5 Implement detect_kdj_cross() method (KDJ signals)
- [ ] 3.6 Implement detect_boll_breakout() method (band breakouts)
- [ ] 3.7 Implement calculate_signal_confidence() method
- [ ] 3.8 Add signal deduplication logic

## 4. Backend - API Integration

- [ ] 4.1 Update app/api/stocks.py to accept indicators parameter
- [ ] 4.2 Add IndicatorRequest Pydantic model for validation
- [ ] 4.3 Add IndicatorResponse Pydantic model
- [ ] 4.4 Implement parse_indicator_params() helper function
- [ ] 4.5 Integrate IndicatorService into get_stock_prices endpoint
- [ ] 4.6 Add indicators to response format
- [ ] 4.7 Create GET /api/stocks/{code}/signals endpoint for signal history
- [ ] 4.8 Add API documentation for new indicator parameters

## 5. Backend - Caching

- [ ] 5.1 Design cache key format for indicators
- [ ] 5.2 Implement indicator cache in CacheManager (cache.py)
- [ ] 5.3 Add cache_indicator_data() method
- [ ] 5.4 Add get_cached_indicator_data() method
- [ ] 5.5 Implement dynamic TTL based on trading hours
- [ ] 5.6 Add cache invalidation logic

## 6. Backend - Unit Tests

- [ ] 6.1 Create tests/test_indicator_service.py
- [ ] 6.2 Write tests for MA calculation (MA5, MA20, MA60)
- [ ] 6.3 Write tests for MACD calculation
- [ ] 6.4 Write tests for RSI calculation
- [ ] 6.5 Write tests for KDJ calculation
- [ ] 6.6 Write tests for BOLL calculation
- [ ] 6.7 Write tests for signal detection (golden/death cross)
- [ ] 6.8 Write tests for edge cases (insufficient data, invalid params)
- [ ] 6.9 Write tests for cache functionality
- [ ] 6.10 Ensure test coverage >85%

## 7. Backend - API Tests

- [ ] 7.1 Add tests for /api/stocks/{code}/prices with indicators param
- [ ] 7.2 Test indicator parameter parsing
- [ ] 7.3 Test indicator response format
- [ ] 7.4 Test /api/stocks/{code}/signals endpoint
- [ ] 7.5 Test error handling for invalid indicator requests
- [ ] 7.6 Test cache behavior

## 8. Frontend - Component Refactoring

- [ ] 8.1 Refactor StockChart.tsx to support multi-grid layout
- [ ] 8.2 Extract chart configuration into separate utility
- [ ] 8.3 Add props for indicator configuration
- [ ] 8.4 Implement dynamic grid creation based on enabled indicators

## 9. Frontend - Main Chart Indicators

- [ ] 9.1 Implement MA overlay rendering (MA5, MA10, MA20, MA60)
- [ ] 9.2 Add color coding for different MA lines
- [ ] 9.3 Implement BOLL overlay rendering (upper, middle, lower bands)
- [ ] 9.4 Add semi-transparent fill between BOLL bands
- [ ] 9.5 Implement indicator legend for main chart

## 10. Frontend - MACD Subplot

- [ ] 10.1 Create MACD grid configuration
- [ ] 10.2 Implement MACD histogram rendering (red/green bars)
- [ ] 10.3 Implement DIF and DEA line rendering
- [ ] 10.4 Add golden/death cross markers
- [ ] 10.5 Add MACD subplot legend

## 11. Frontend - RSI Subplot

- [ ] 11.1 Create RSI grid configuration
- [ ] 11.2 Implement RSI line rendering (0-100 range)
- [ ] 11.3 Add overbought zone (70+) with shading
- [ ] 11.4 Add oversold zone (30-) with shading
- [ ] 11.5 Add threshold crossing markers
- [ ] 11.6 Add RSI subplot legend

## 12. Frontend - KDJ Subplot

- [ ] 12.1 Create KDJ grid configuration
- [ ] 12.2 Implement K, D, J line rendering with distinct colors
- [ ] 12.3 Add reference lines at 20 and 80
- [ ] 12.4 Add golden/death cross markers
- [ ] 12.5 Add KDJ subplot legend

## 13. Frontend - Indicator Selector Component

- [ ] 13.1 Create src/components/IndicatorSelector.tsx
- [ ] 13.2 Implement checkbox UI for main chart indicators (MA, BOLL)
- [ ] 13.3 Implement toggle switches for subplots (MACD, RSI, KDJ)
- [ ] 13.4 Add MA period selector (5, 10, 20, 60, 120, 250)
- [ ] 13.5 Add MACD parameter inputs (fast, slow, signal)
- [ ] 13.6 Add RSI period input
- [ ] 13.7 Add KDJ parameter inputs (N, M1, M2)
- [ ] 13.8 Add BOLL parameter inputs (period, std)
- [ ] 13.9 Add preset configurations (default, conservative, aggressive)
- [ ] 13.10 Implement "Apply" and "Reset" buttons

## 14. Frontend - State Management

- [ ] 14.1 Create indicator state in StockAnalysisPage
- [ ] 14.2 Implement localStorage save for indicator preferences
- [ ] 14.3 Implement localStorage load on component mount
- [ ] 14.4 Add state update handlers for indicator changes
- [ ] 14.5 Implement optimistic UI updates

## 15. Frontend - API Integration

- [ ] 15.1 Update api.ts to support indicators query parameter
- [ ] 15.2 Add getStockPricesWithIndicators() function
- [ ] 15.3 Add getStockSignals() function
- [ ] 15.4 Implement indicator data transformation for ECharts
- [ ] 15.5 Add error handling for indicator API calls
- [ ] 15.6 Add loading states for indicator data

## 16. Frontend - Signal Visualization

- [ ] 16.1 Implement signal marker rendering on chart
- [ ] 16.2 Add different icons for different signal types (buy/sell)
- [ ] 16.3 Add signal tooltip with details (type, confidence, date)
- [ ] 16.4 Implement signal filtering UI
- [ ] 16.5 Add signal legend

## 17. Frontend - Performance Optimization

- [ ] 17.1 Implement data downsampling for long periods (1y+)
- [ ] 17.2 Add React.memo to IndicatorSelector component
- [ ] 17.3 Implement lazy loading for indicator data
- [ ] 17.4 Add debounce to indicator parameter changes
- [ ] 17.5 Optimize ECharts rendering with progressive loading

## 18. Frontend - UI/UX Polish

- [ ] 18.1 Add loading spinner for indicator calculations
- [ ] 18.2 Add error messages for failed indicator loads
- [ ] 18.3 Implement responsive layout for indicator selector
- [ ] 18.4 Add tooltips explaining each indicator
- [ ] 18.5 Implement keyboard shortcuts for common actions
- [ ] 18.6 Add smooth transitions for subplot show/hide

## 19. Integration Testing

- [ ] 19.1 Test end-to-end flow: search stock → select indicators → view chart
- [ ] 19.2 Test MA overlay with different periods
- [ ] 19.3 Test BOLL display and band calculations
- [ ] 19.4 Test MACD subplot rendering and signals
- [ ] 19.5 Test RSI subplot with threshold zones
- [ ] 19.6 Test KDJ subplot rendering
- [ ] 19.7 Test signal marker display on chart
- [ ] 19.8 Test indicator configuration persistence
- [ ] 19.9 Test performance with 1y data + all indicators
- [ ] 19.10 Test error scenarios (API failure, invalid params)

## 20. Documentation

- [ ] 20.1 Update API documentation with indicator parameters
- [ ] 20.2 Add JSDoc comments to indicator-related functions
- [ ] 20.3 Create ITERATION_2_SUMMARY.md
- [ ] 20.4 Update README.md with new features
- [ ] 20.5 Add user guide for indicator usage
- [ ] 20.6 Document indicator calculation formulas

## 21. Deployment Preparation

- [ ] 21.1 Run all backend tests and verify >85% coverage
- [ ] 21.2 Run all frontend tests
- [ ] 21.3 Test in production-like environment
- [ ] 21.4 Prepare rollback plan
- [ ] 21.5 Clear Redis cache for indicator data
- [ ] 21.6 Update deployment scripts if needed
