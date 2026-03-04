const http = require('http');
const url = require('url');

const PORT = 8000;

// Mock data
const mockData = {
  apiInfo: {
    api_name: 'Stock Analysis Platform',
    version: '0.1.0',
    environment: 'development',
    features: [
      '股票行情数据获取',
      '技术面分析',
      '基本面分析',
      '资讯采集与分析',
      '综合分析报告生成'
    ],
    documentation: '/docs',
    timestamp: new Date().toISOString()
  },
  healthCheck: {
    status: 'healthy',
    database: 'connected',
    redis: 'connected',
    timestamp: new Date().toISOString()
  },
  stockSearchResults: [
    {
      stock_code: '000001.SZ',
      name: '平安银行',
      symbol: '000001',
      market: 'A股',
      industry: '银行',
      area: '深圳'
    },
    {
      stock_code: '600000.SH',
      name: '浦发银行',
      symbol: '600000',
      market: 'A股',
      industry: '银行',
      area: '上海'
    }
  ],
  stockInfo: {
    stock_code: '000001.SZ',
    name: '平安银行',
    fullname: '平安银行股份有限公司',
    market: 'A股',
    exchange: 'SZSE',
    industry: '银行',
    sector: '金融',
    area: '深圳',
    listing_date: '1991-04-03',
    status: 'active'
  },
  stockPrices: []
};

// Generate mock price data
const generatePrices = (days = 30) => {
  const prices = [];
  const basePrice = 10.0;
  const today = new Date();

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');

    const open = basePrice + Math.random() * 2 - 1;
    const close = open + Math.random() * 1 - 0.5;
    const high = Math.max(open, close) + Math.random() * 0.5;
    const low = Math.min(open, close) - Math.random() * 0.5;
    const volume = Math.floor(Math.random() * 1000000) + 500000;

    prices.push({
      stock_code: '000001.SZ',
      trade_date: dateStr,
      open: parseFloat(open.toFixed(2)),
      high: parseFloat(high.toFixed(2)),
      low: parseFloat(low.toFixed(2)),
      close: parseFloat(close.toFixed(2)),
      volume: volume,
      amount: volume * close
    });
  }

  return prices;
};

mockData.stockPrices = generatePrices(90);

// Calculate MA indicators
const calculateMA = (prices, period) => {
  const result = [];
  for (let i = 0; i < prices.length; i++) {
    if (i < period - 1) {
      result.push(null);
    } else {
      let sum = 0;
      for (let j = 0; j < period; j++) {
        sum += prices[i - j].close;
      }
      result.push(parseFloat((sum / period).toFixed(2)));
    }
  }
  return result;
};

// Calculate MACD
const calculateMACD = (prices) => {
  const closes = prices.map(p => p.close);
  const ema12 = calculateEMA(closes, 12);
  const ema26 = calculateEMA(closes, 26);

  const dif = ema12.map((v, i) => v && ema26[i] ? v - ema26[i] : null);
  const dea = calculateEMA(dif.filter(v => v !== null), 9);

  // Pad dea to match length
  const paddedDea = Array(dif.length - dea.length).fill(null).concat(dea);
  const macd = dif.map((v, i) => v && paddedDea[i] ? (v - paddedDea[i]) * 2 : null);

  return { dif, dea: paddedDea, macd };
};

const calculateEMA = (data, period) => {
  const k = 2 / (period + 1);
  const result = [];
  let ema = data[0];

  for (let i = 0; i < data.length; i++) {
    if (data[i] === null) {
      result.push(null);
    } else {
      if (i === 0) {
        ema = data[i];
      } else {
        ema = data[i] * k + ema * (1 - k);
      }
      result.push(parseFloat(ema.toFixed(4)));
    }
  }
  return result;
};

// Calculate RSI
const calculateRSI = (prices, period = 14) => {
  const closes = prices.map(p => p.close);
  const result = [];

  for (let i = 0; i < closes.length; i++) {
    if (i < period) {
      result.push(null);
    } else {
      let gains = 0;
      let losses = 0;

      for (let j = i - period + 1; j <= i; j++) {
        const change = closes[j] - closes[j - 1];
        if (change > 0) gains += change;
        else losses += Math.abs(change);
      }

      const avgGain = gains / period;
      const avgLoss = losses / period;
      const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
      const rsi = 100 - (100 / (1 + rs));

      result.push(parseFloat(rsi.toFixed(2)));
    }
  }

  return result;
};

// Calculate KDJ
const calculateKDJ = (prices, n = 9, m1 = 3, m2 = 3) => {
  const k = [];
  const d = [];
  const j = [];

  for (let i = 0; i < prices.length; i++) {
    if (i < n - 1) {
      k.push(null);
      d.push(null);
      j.push(null);
    } else {
      let highest = -Infinity;
      let lowest = Infinity;

      for (let idx = i - n + 1; idx <= i; idx++) {
        highest = Math.max(highest, prices[idx].high);
        lowest = Math.min(lowest, prices[idx].low);
      }

      const rsv = lowest === highest ? 50 : ((prices[i].close - lowest) / (highest - lowest)) * 100;

      const prevK = i === n - 1 ? 50 : k[i - 1];
      const prevD = i === n - 1 ? 50 : d[i - 1];

      const currentK = (prevK * (m1 - 1) + rsv) / m1;
      const currentD = (prevD * (m2 - 1) + currentK) / m2;
      const currentJ = 3 * currentK - 2 * currentD;

      k.push(parseFloat(currentK.toFixed(2)));
      d.push(parseFloat(currentD.toFixed(2)));
      j.push(parseFloat(currentJ.toFixed(2)));
    }
  }

  return { k, d, j };
};

// Calculate Bollinger Bands
const calculateBOLL = (prices, period = 20, stdDev = 2) => {
  const closes = prices.map(p => p.close);
  const upper = [];
  const middle = [];
  const lower = [];

  for (let i = 0; i < closes.length; i++) {
    if (i < period - 1) {
      upper.push(null);
      middle.push(null);
      lower.push(null);
    } else {
      let sum = 0;
      for (let j = i - period + 1; j <= i; j++) {
        sum += closes[j];
      }
      const ma = sum / period;

      let variance = 0;
      for (let j = i - period + 1; j <= i; j++) {
        variance += Math.pow(closes[j] - ma, 2);
      }
      const std = Math.sqrt(variance / period);

      middle.push(parseFloat(ma.toFixed(2)));
      upper.push(parseFloat((ma + stdDev * std).toFixed(2)));
      lower.push(parseFloat((ma - stdDev * std).toFixed(2)));
    }
  }

  return { upper, middle, lower };
};

const server = http.createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  const parsedUrl = url.parse(req.url, true);
  const pathname = parsedUrl.pathname;

  res.setHeader('Content-Type', 'application/json');

  // Route handling
  if (pathname === '/') {
    res.writeHead(200);
    res.end(JSON.stringify({
      name: 'Stock Analysis Platform API',
      version: '0.1.0',
      status: 'running',
      timestamp: new Date().toISOString()
    }));
  } else if (pathname === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify(mockData.healthCheck));
  } else if (pathname === '/api/info') {
    res.writeHead(200);
    res.end(JSON.stringify(mockData.apiInfo));
  } else if (pathname === '/api/stocks/search') {
    res.writeHead(200);
    res.end(JSON.stringify({
      total: mockData.stockSearchResults.length,
      data: mockData.stockSearchResults
    }));
  } else if (pathname.match(/^\/api\/stocks\/[^\/]+$/)) {
    res.writeHead(200);
    res.end(JSON.stringify(mockData.stockInfo));
  } else if (pathname.match(/^\/api\/stocks\/[^\/]+\/prices$/)) {
    const period = parsedUrl.query.period || '1m';
    const indicators = parsedUrl.query.indicators || '';
    let days = 30;
    if (period === '3m') days = 90;
    else if (period === '6m') days = 180;
    else if (period === '1y') days = 365;

    const prices = mockData.stockPrices.slice(-days);

    const response = {
      stock_code: '000001.SZ',
      period: period,
      total: prices.length,
      data: prices
    };

    // Add indicators if requested
    if (indicators) {
      const indicatorList = indicators.split(',');
      response.indicators = {};

      if (indicatorList.includes('ma')) {
        response.indicators.ma = {
          ma5: calculateMA(prices, 5),
          ma10: calculateMA(prices, 10),
          ma20: calculateMA(prices, 20),
          ma60: calculateMA(prices, 60)
        };
      }

      if (indicatorList.includes('macd')) {
        response.indicators.macd = calculateMACD(prices);
      }

      if (indicatorList.includes('rsi')) {
        response.indicators.rsi = {
          rsi: calculateRSI(prices, 14)
        };
      }

      if (indicatorList.includes('kdj')) {
        response.indicators.kdj = calculateKDJ(prices, 9, 3, 3);
      }

      if (indicatorList.includes('boll')) {
        response.indicators.boll = calculateBOLL(prices, 20, 2);
      }
    }

    res.writeHead(200);
    res.end(JSON.stringify(response));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, () => {
  console.log(`Mock backend server running at http://localhost:${PORT}/`);
  console.log('API endpoints:');
  console.log('  GET  /health');
  console.log('  GET  /api/info');
  console.log('  GET  /api/stocks/search?keyword=xxx');
  console.log('  GET  /api/stocks/{code}');
  console.log('  GET  /api/stocks/{code}/prices?period=1m');
});
