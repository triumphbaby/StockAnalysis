# 🎉 迭代1成品 - 快速启动指南

## ✨ 已完成的功能展示

### 核心功能
- ✅ **股票搜索** - 实时搜索股票（支持代码/名称）
- ✅ **股票详情** - 展示股票基本信息
- ✅ **K线图表** - 专业级蜡烛图 + 成交量图
- ✅ **时间周期** - 支持 1月/3月/6月/1年切换
- ✅ **交互功能** - 图表缩放、拖拽、数据提示

### 技术栈
- **前端**: React 18 + TypeScript + Ant Design + ECharts
- **后端**: Mock Server (Node.js)
- **数据**: 模拟真实股票行情数据

---

## 🚀 快速启动步骤

### 方式1：使用启动脚本（推荐）

#### Windows 用户

1. 双击运行 `start-demo.bat`
2. 等待服务启动（约10-20秒）
3. 浏览器自动打开到 http://localhost:3000

#### Linux/Mac 用户

```bash
chmod +x start-demo.sh
./start-demo.sh
```

---

### 方式2：手动启动

#### 步骤1：启动 Mock 后端服务器

打开**第一个**终端窗口：

```bash
# 进入项目根目录
cd D:\ATest\Test\AI\Project\Claude\StockAnalysis

# 启动 Mock 服务器
node mock-server.js
```

✅ 看到以下输出表示成功：
```
Mock backend server running at http://localhost:8000/
API endpoints:
  GET  /health
  GET  /api/info
  GET  /api/stocks/search?keyword=xxx
  GET  /api/stocks/{code}
  GET  /api/stocks/{code}/prices?period=1m
```

#### 步骤2：启动前端应用

打开**第二个**终端窗口：

```bash
# 进入前端目录
cd D:\ATest\Test\AI\Project\Claude\StockAnalysis\frontend

# 启动前端开发服务器
npm start
```

✅ 看到以下输出表示成功：
```
Compiled successfully!

You can now view stock-analysis-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

浏览器会自动打开到 http://localhost:3000

---

## 🎮 功能演示指南

### 1. 访问应用首页

打开浏览器访问：**http://localhost:3000**

你会看到：
- 系统状态卡片（显示 API、数据库、缓存状态）
- 功能列表卡片
- 导航菜单

### 2. 进入股票分析页面

点击顶部导航栏的 **"股票分析"** 或直接访问：
**http://localhost:3000/analysis**

### 3. 搜索股票

在搜索框中输入：
- 股票名称：`平安` 或 `浦发`
- 股票代码：`000001` 或 `600000`

下拉列表会显示匹配的股票。

### 4. 查看股票详情

选择一只股票（如 "平安银行 000001.SZ"），页面会展示：

**基本信息卡片**：
- 股票代码
- 股票名称
- 公司全称
- 所属市场
- 所属行业
- 上市日期
- 当前状态

**K线图卡片**：
- 蜡烛图（红涨绿跌）
- 成交量柱状图
- 时间周期选择器

### 5. 切换时间周期

点击图表上方的按钮：
- **1月** - 显示最近30天数据
- **3月** - 显示最近90天数据
- **6月** - 显示最近180天数据
- **1年** - 显示最近365天数据

### 6. 图表交互

- **缩放**：鼠标滚轮
- **拖拽**：按住鼠标左键拖动
- **数据提示**：鼠标悬停在K线上查看详细数据
- **区域缩放**：拖动底部滑块

---

## 📊 Mock 数据说明

### 提供的模拟股票

1. **平安银行 (000001.SZ)**
   - 市场：深圳A股
   - 行业：银行
   - 提供90天行情数据

2. **浦发银行 (600000.SH)**
   - 市场：上海A股
   - 行业：银行
   - 提供90天行情数据

### API 端点

Mock Server 提供以下 API：

| 端点 | 说明 |
|------|------|
| `GET /health` | 健康检查 |
| `GET /api/info` | API 信息 |
| `GET /api/stocks/search?keyword=xxx` | 搜索股票 |
| `GET /api/stocks/{code}` | 获取股票详情 |
| `GET /api/stocks/{code}/prices?period=1m` | 获取行情数据 |

你可以在浏览器中直接访问测试：
- http://localhost:8000/health
- http://localhost:8000/api/stocks/search?keyword=平安
- http://localhost:8000/api/stocks/000001.SZ

---

## 🐛 常见问题

### Q1: 端口 8000 被占用

**错误**: `Error: listen EADDRINUSE: address already in use :::8000`

**解决方案**:

```bash
# Windows - 查找并关闭占用端口的进程
netstat -ano | findstr :8000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

或修改 `mock-server.js` 中的端口：
```javascript
const PORT = 8001;  // 改为其他端口
```

同时修改前端 API 配置 `frontend/src/services/api.ts`：
```typescript
baseURL: 'http://localhost:8001',  // 对应修改
```

### Q2: 端口 3000 被占用

**解决方案**:

```bash
# 设置环境变量使用其他端口
# Windows
set PORT=3001 && npm start

# Linux/Mac
PORT=3001 npm start
```

### Q3: 前端无法连接后端

**检查清单**:
1. ✅ Mock Server 是否正在运行（终端有输出）
2. ✅ 访问 http://localhost:8000/health 是否有响应
3. ✅ 浏览器控制台是否有跨域错误

### Q4: 图表不显示

**可能原因**:
1. 数据还在加载中（稍等片刻）
2. API 请求失败（打开浏览器 DevTools -> Network 检查）
3. 控制台有错误信息（打开浏览器 DevTools -> Console 查看）

---

## 🎨 界面截图说明

### 首页
- 顶部：导航栏（首页 | 股票分析）
- 左侧：系统状态卡片
- 右侧：功能列表卡片

### 股票分析页
- 顶部：搜索框
- 中部：股票基本信息
- 底部：K线图表

---

## 🔧 开发者选项

### 查看 API 请求

打开浏览器开发者工具：
- **Windows**: `F12` 或 `Ctrl + Shift + I`
- **Mac**: `Cmd + Option + I`

进入 **Network** 标签，可以看到所有 API 请求和响应。

### 修改 Mock 数据

编辑 `mock-server.js` 文件，修改 `mockData` 对象：

```javascript
const mockData = {
  stockSearchResults: [
    // 添加更多股票
    {
      stock_code: '600036.SH',
      name: '招商银行',
      market: 'A股',
      industry: '银行'
    }
  ]
};
```

修改后保存，重启 Mock Server 即可。

---

## 🎯 下一步：完整版（Docker）

当前演示使用 Mock 数据。要使用完整功能（真实数据、数据库、缓存等），需要：

### 1. 安装 Docker Desktop

- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: https://docs.docker.com/engine/install/

### 2. 配置 Tushare Token

1. 注册 Tushare: https://tushare.pro
2. 获取 Token
3. 编辑 `.env` 文件：
   ```env
   TUSHARE_TOKEN=your_token_here
   ```

### 3. 启动完整环境

```bash
# 启动所有服务（PostgreSQL + Redis + Backend + Frontend）
docker-compose up -d

# 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 同步股票数据
curl -X POST http://localhost:8000/api/stocks/sync
```

### 4. 访问应用

- 前端: http://localhost:3000
- API 文档: http://localhost:8000/docs

---

## 📝 技术文档

详细技术文档请查看：

- `README.md` - 项目概述
- `QUICKSTART.md` - Docker 启动指南
- `ITERATION_1_SUMMARY.md` - 迭代1完成总结
- `PROJECT_STATUS.md` - 项目当前状态

---

## 🎊 体验愉快！

如有问题，请查看上述常见问题部分或检查终端错误信息。

**当前版本**: 迭代1 (股票行情数据获取与展示)
**下一版本**: 迭代2 (技术面分析引擎 - 即将推出)
