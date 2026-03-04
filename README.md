# 股票研究分析工具 (Stock Analysis Platform)

[![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)](https://github.com/yourusername/stock-analysis)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRD](https://img.shields.io/badge/PRD-完整-brightgreen.svg)](PRD.md)
[![UI](https://img.shields.io/badge/UI-Glassmorphism-blueviolet.svg)](#)

智能化的股票研究辅助工具，提供技术面分析、基本面分析、资讯采集和综合分析报告。采用现代化深色主题+玻璃拟态设计，打造专业、沉浸的金融科技体验。

---

## 📋 目录

- [特性](#特性)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [开发进度](#开发进度)
- [文档](#文档)
- [贡献](#贡献)

---

## ✨ 特性

### 已实现功能 ✅

#### 🎨 UI/UX (v0.4.0 新增)
- **深色模式主题**: 现代化金融科技风格,专业沉浸
- **玻璃拟态设计**: Glassmorphism效果,毛玻璃质感
- **微动效交互**: 悬停提升、渐变过渡、发光效果
- **渐变文字**: 科技感渐变标题
- **响应式设计**: 完美适配各种屏幕尺寸

#### 📈 功能特性
- **股票搜索**: 支持代码、名称搜索
- **K线图展示**: 交互式K线图，支持缩放拖拽
- **技术指标分析**:
  - MA均线系统 (MA5/10/20/60)
  - 布林带 (BOLL)
  - MACD指标
  - RSI指标
  - KDJ指标
- **时间周期切换**: 1月/3月/6月/1年
- **动态布局**: 智能多grid布局系统

### 规划中功能 📅
- 资讯采集与展示
- 基本面分析模块
- 综合分析报告
- AI驱动的形态识别
- 策略回测平台

---

## 🚀 快速开始

### 前置要求
- Node.js >= 18.x
- Python >= 3.11
- Docker (可选)

### 安装步骤

#### 1. 克隆项目
```bash
git clone https://github.com/yourusername/stock-analysis.git
cd stock-analysis
```

#### 2. 启动后端 (Mock Server)
```bash
node mock-server.js
```
后端运行在: http://localhost:8000

#### 3. 启动前端
```bash
cd frontend
npm install
npm start
```
前端运行在: http://localhost:3000

### 快速演示
使用提供的启动脚本一键启动：

**Windows**:
```bash
start-demo.bat
```

**Linux/Mac**:
```bash
./start-demo.sh
```

访问: http://localhost:3000/analysis

---

## 📁 项目结构

```
stock-analysis/
├── backend/                    # 后端代码（FastAPI，待迁移）
│   ├── app/
│   │   ├── api/               # API路由
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 业务逻辑
│   │   └── tests/             # 后端测试
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # 前端代码（React + TypeScript）
│   ├── public/
│   ├── src/
│   │   ├── components/        # React组件
│   │   ├── pages/             # 页面
│   │   ├── services/          # API服务
│   │   └── utils/             # 工具函数
│   ├── package.json
│   └── Dockerfile
│
├── docs/                       # 文档目录
│   ├── iterations/            # 迭代文档
│   │   ├── ITERATION_0_SUMMARY.md
│   │   ├── ITERATION_1_SUMMARY.md
│   │   ├── ITERATION_2_DEMO.md
│   │   └── ITERATION_2_TEST_REPORT.md
│   ├── guides/                # 使用指南
│   │   ├── QUICKSTART.md
│   │   ├── START_DEMO.md
│   │   ├── 成品使用指南.md
│   │   └── 迭代2-技术指标展示指南.md
│   ├── api/                   # API文档
│   │   └── API测试示例.md
│   └── PROJECT_STATUS.md      # 项目状态
│
├── tests/                      # 测试目录
│   ├── manual/                # 手动测试
│   │   ├── test_indicators_direct.py
│   │   ├── test_indicators_standalone.py
│   │   └── test_indicators.json
│   └── e2e/                   # 端到端测试（待添加）
│
├── scripts/                    # 工具脚本
│   ├── init_db.sh
│   └── deploy.sh
│
├── openspec/                   # OpenSpec工作流
│   └── changes/
│       └── technical-indicators/
│
├── .claude/                    # Claude Code配置
│   ├── memory/
│   └── skills/
│
├── logs/                       # 日志目录
│
├── mock-server.js             # Mock后端服务器
├── docker-compose.yml         # Docker编排配置
├── PRD.md                     # 产品需求文档
├── PROJECT_ROADMAP.md         # 项目路线图
├── README.md                  # 本文件
├── start-demo.bat             # Windows启动脚本
├── start-demo.sh              # Linux/Mac启动脚本
├── .env.example               # 环境变量示例
└── .gitignore
```

---

## 🛠 技术栈

### 后端
| 技术 | 版本 | 用途 |
|------|------|------|
| FastAPI | 0.104+ | Web框架（规划） |
| Node.js | 18+ | Mock Server（当前） |
| PostgreSQL | 14+ | 关系型数据库 |
| Redis | 7+ | 缓存 |
| Pandas | 2.x | 数据处理 |

### 前端
| 技术 | 版本 | 用途 |
|------|------|------|
| React | 18.x | UI框架 |
| TypeScript | 5.x | 类型系统 |
| Ant Design | 5.x | UI组件库 |
| ECharts | 5.x | 图表库 |
| Axios | 1.x | HTTP客户端 |

### 开发工具
| 工具 | 用途 |
|------|------|
| Docker | 容器化 |
| Git | 版本控制 |
| ESLint | 代码检查 |
| Prettier | 代码格式化 |

---

## 📊 开发进度

### 总体进度: 30% (3/10 迭代完成)

#### Q1 短期规划 (60%)
- ✅ **迭代0**: 项目初始化 - 100%
- ✅ **迭代1**: 股票数据获取与展示 - 100%
- ✅ **迭代2**: 技术面分析引擎 - 100%
- ⏳ **迭代3**: 资讯采集与展示 - 0%
- ⏳ **迭代4**: 基本面分析模块 - 0%
- ⏳ **迭代5**: 综合分析报告 - 0%

#### Q2 中期规划 (0%)
- ⏳ **迭代6**: K线形态自动识别
- ⏳ **迭代7**: 财报风险智能预警
- ⏳ **迭代8**: 个性化资讯推荐

#### Q3 长期规划 (0%)
- ⏳ **迭代9**: 策略回测平台
- ⏳ **迭代10**: 开放API平台

详见: [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)

---

## 📚 文档

### 核心文档
- **[PRD.md](PRD.md)** - 产品需求文档
- **[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)** - 项目路线图
- **[docs/guides/QUICKSTART.md](docs/guides/QUICKSTART.md)** - 快速开始指南

### 迭代文档
- **[迭代0总结](docs/iterations/ITERATION_0_SUMMARY.md)** - 项目初始化
- **[迭代1总结](docs/iterations/ITERATION_1_SUMMARY.md)** - 数据获取与展示
- **[迭代2演示](docs/iterations/ITERATION_2_DEMO.md)** - 技术指标分析
- **[迭代2测试报告](docs/iterations/ITERATION_2_TEST_REPORT.md)** - 后端测试

### 使用指南
- **[成品使用指南](docs/guides/成品使用指南.md)** - 完整功能介绍
- **[技术指标指南](docs/guides/迭代2-技术指标展示指南.md)** - 技术指标使用
- **[启动演示](docs/guides/START_DEMO.md)** - 演示环境启动

### API文档
- **[API测试示例](docs/api/API测试示例.md)** - API使用示例

---

## 🎮 使用示例

### 1. 搜索股票
访问 http://localhost:3000/analysis，在搜索框输入:
```
平安
```
或
```
000001
```

### 2. 查看技术指标
选择股票后，勾选想要的技术指标：
- ☑️ MA均线 - 4条均线叠加
- ☑️ 布林带 - 上中下轨道
- ☑️ MACD - 柱状图+DIF/DEA
- ☑️ RSI - 超买超卖指标
- ☑️ KDJ - 随机指标

### 3. 切换周期
点击周期按钮切换查看不同时间段：
- 1个月
- 3个月
- 6个月
- 1年

### 4. 交互操作
- **缩放**: 鼠标滚轮
- **拖拽**: 鼠标拖动图表
- **查看数值**: 鼠标悬停

---

## 🧪 测试

### API测试
```bash
# 健康检查
curl http://localhost:8000/health

# 获取股票数据
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=1m"

# 获取技术指标
curl "http://localhost:8000/api/stocks/000001.SZ/prices?period=1m&indicators=ma,macd,rsi,kdj,boll"
```

---

## 📄 许可证

本项目采用 MIT 许可证

---

## 🙏 致谢

- [Tushare](https://tushare.pro/) - 金融数据接口
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Ant Design](https://ant.design/) - UI组件库
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架

---

**当前版本**: v0.4.0 (UI/UX现代化升级)
**最后更新**: 2026-02-28
**维护状态**: 🟢 活跃开发中
