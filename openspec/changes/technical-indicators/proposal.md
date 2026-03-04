## Why

迭代1完成了股票行情数据的获取和K线图展示，但缺乏技术面分析能力。投资者需要技术指标（MA、MACD、RSI、KDJ、布林带等）来辅助决策。当前K线图仅展示原始OHLCV数据，无法提供技术分析视角，限制了平台的实用价值。

## What Changes

- 新增技术指标计算引擎（支持 MA、MACD、RSI、KDJ、BOLL）
- K线图支持叠加均线指标（MA5、MA10、MA20、MA60）
- 新增副图展示 MACD 和 RSI 指标
- 新增技术信号检测功能（金叉/死叉、超买/超卖）
- 提供指标配置界面（用户可选择显示哪些指标）
- 后端 API 支持指标数据计算和缓存

## Capabilities

### New Capabilities
- `indicator-calculation`: 技术指标计算引擎，支持常用技术指标的计算逻辑
- `indicator-visualization`: K线图指标可视化，包括主图叠加和副图展示
- `signal-detection`: 技术信号检测，识别关键的买卖信号

### Modified Capabilities
<!-- 无现有功能需求变更 -->

## Impact

**后端影响**:
- 新增 `app/services/indicator_service.py` - 指标计算服务
- 新增 `app/api/indicators.py` - 指标API路由
- 修改 `app/api/stocks.py` - 添加指标参数支持
- 新增数据库缓存表（可选，用于缓存计算结果）

**前端影响**:
- 修改 `StockChart.tsx` - 支持指标叠加和副图
- 新增 `IndicatorSelector.tsx` - 指标选择器组件
- 修改 `StockAnalysisPage.tsx` - 集成指标选择功能

**依赖影响**:
- 后端新增依赖: `pandas-ta` 或 `ta-lib` (技术指标库)
- 前端无新增依赖（ECharts 已支持）

**性能影响**:
- 指标计算可能增加响应时间（需缓存优化）
- 前端图表渲染数据量增加（需优化性能）
