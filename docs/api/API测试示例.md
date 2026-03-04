# API 测试示例

## 基础API测试

### 1. 健康检查
```bash
curl http://localhost:8000/health
```

**响应**:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2026-02-28T07:06:04.556Z"
}
```

---

### 2. 搜索股票
```bash
curl "http://localhost:8000/api/stocks/search?keyword=平安"
```

**响应**:
```json
{
  "total": 2,
  "data": [
    {
      "stock_code": "000001.SZ",
      "name": "平安银行",
      "symbol": "000001",
      "market": "A股",
      "industry": "银行",
      "area": "深圳"
    }
  ]
}
```

---

### 3. 获取股票详情
```bash
curl http://localhost:8000/api/stocks/000001.SZ
```

**响应**:
```json
{
  "stock_code": "000001.SZ",
  "name": "平安银行",
  "fullname": "平安银行股份有限公司",
  "market": "A股",
  "exchange": "SZSE",
  "industry": "银行",
  "sector": "金融",
  "area": "深圳",
  "listing_date": "1991-04-03",
  "status": "active"
}
```

---

### 4. 获取行情数据（1个月）
```bash
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=1m"
```

**响应**:
```json
{
  "stock_code": "000001.SZ",
  "period": "1m",
  "total": 30,
  "data": [
    {
      "stock_code": "000001.SZ",
      "trade_date": "20240201",
      "open": 10.05,
      "high": 10.52,
      "low": 9.89,
      "close": 10.21,
      "volume": 854231,
      "amount": 8723456.78
    }
    // ... 更多数据
  ]
}
```

---

### 5. 获取行情数据（不同周期）

#### 3个月
```bash
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=3m"
```

#### 6个月
```bash
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=6m"
```

#### 1年
```bash
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=1y"
```

---

## 浦发银行示例

### 搜索
```bash
curl "http://localhost:8000/api/stocks/search?keyword=浦发"
```

### 详情
```bash
curl http://localhost:8000/api/stocks/600000.SH
```

### 行情
```bash
curl "http://localhost:8000/api/stocks/600000.SH/prices?period=3m"
```

---

## 在浏览器中测试

直接在浏览器地址栏输入以下URL：

```
http://localhost:8000/health
http://localhost:8000/api/stocks/search?keyword=平安
http://localhost:8000/api/stocks/000001.SZ
http://localhost:8000/api/stocks/000001.SZ/prices?period=1m
```

浏览器会直接显示JSON响应。

---

## 使用Postman/Insomnia测试

### GET请求示例

**URL**: `http://localhost:8000/api/stocks/000001.SZ/prices`

**Query参数**:
- `period`: `1m` (可选: 3m, 6m, 1y)

**Headers**:
```
Accept: application/json
```

---

## Python测试脚本

```python
import requests

# 健康检查
response = requests.get('http://localhost:8000/health')
print(response.json())

# 搜索股票
response = requests.get('http://localhost:8000/api/stocks/search', params={'keyword': '平安'})
print(response.json())

# 获取股票详情
response = requests.get('http://localhost:8000/api/stocks/000001.SZ')
print(response.json())

# 获取行情数据
response = requests.get('http://localhost:8000/api/stocks/000001.SZ/prices', params={'period': '1m'})
data = response.json()
print(f"获取到 {data['total']} 条行情数据")
```

---

## JavaScript测试脚本

```javascript
// 使用Fetch API
async function testAPI() {
  // 健康检查
  const health = await fetch('http://localhost:8000/health');
  console.log(await health.json());

  // 搜索股票
  const search = await fetch('http://localhost:8000/api/stocks/search?keyword=平安');
  console.log(await search.json());

  // 获取股票详情
  const stock = await fetch('http://localhost:8000/api/stocks/000001.SZ');
  console.log(await stock.json());

  // 获取行情数据
  const prices = await fetch('http://localhost:8000/api/stocks/000001.SZ/prices?period=1m');
  console.log(await prices.json());
}

testAPI();
```

---

## 数据字段说明

### 股票信息字段
- `stock_code`: 股票代码 (如: 000001.SZ)
- `name`: 股票简称 (如: 平安银行)
- `fullname`: 公司全称
- `market`: 所属市场 (A股/港股/美股)
- `exchange`: 交易所 (SZSE/SSE)
- `industry`: 所属行业
- `sector`: 所属板块
- `area`: 所在地区
- `listing_date`: 上市日期
- `status`: 状态 (active/suspended/delisted)

### 行情数据字段
- `trade_date`: 交易日期 (YYYYMMDD格式)
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量
- `amount`: 成交额

---

## 错误处理

### 404 - 股票不存在
```bash
curl http://localhost:8000/api/stocks/999999.SZ
```

响应:
```json
{
  "error": "Not found"
}
```

### 无效的周期参数
```bash
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=invalid"
```

系统会使用默认值 `1m`
