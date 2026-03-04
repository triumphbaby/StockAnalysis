# 快速启动指南 (Quick Start Guide)

## 🎯 迭代 0 完成状态

✅ **已完成的工作**

1. **项目目录结构** - 完整的前后端目录组织
2. **Docker 环境配置** - Docker Compose 编排所有服务
3. **后端基础框架** - FastAPI + PostgreSQL + Redis + Celery
4. **前端基础框架** - React + TypeScript + Ant Design
5. **测试框架** - Pytest (后端) + Jest (前端)
6. **配置文件** - 环境变量、依赖管理
7. **文档** - README、项目验证脚本

## 🚀 快速启动步骤

### 前提条件

在开始之前，请确保已安装：

- ✅ **Docker Desktop** (Windows/Mac) 或 Docker Engine (Linux)
- ✅ **Docker Compose** (通常随 Docker Desktop 一起安装)

### 步骤 1: 验证项目结构

运行验证脚本确保所有文件都已正确创建：

```bash
python scripts/verify_setup.py
```

预期输出应该显示所有检查都通过（All checks passed）。

### 步骤 2: 配置环境变量

编辑 `.env` 文件，配置必要的 API 密钥：

```bash
# 使用文本编辑器打开 .env 文件
notepad .env  # Windows
# 或
nano .env     # Linux/Mac
```

**重要**: 更新以下配置（如果需要使用相关功能）：

```env
# OpenAI API (用于资讯摘要和分析)
OPENAI_API_KEY=sk-your-actual-key-here

# Tushare Token (用于A股数据)
TUSHARE_TOKEN=your-tushare-token-here

# Alpha Vantage API (用于美股数据)
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key-here
```

> **注意**: 在迭代 0 阶段，这些 API 密钥不是必需的，因为还没有实现相关功能。

### 步骤 3: 启动所有服务

使用 Docker Compose 启动所有服务：

```bash
docker-compose up -d
```

这个命令会启动以下服务：
- PostgreSQL (数据库) - 端口 5432
- Redis (缓存) - 端口 6379
- Backend API (FastAPI) - 端口 8000
- Celery Worker (异步任务)
- Celery Beat (定时任务)
- Frontend (React) - 端口 3000

### 步骤 4: 等待服务启动

首次启动可能需要 2-5 分钟（下载镜像和构建）。

查看服务状态：

```bash
docker-compose ps
```

查看服务日志：

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 步骤 5: 验证服务

#### 5.1 检查后端 API

在浏览器中访问：

- **API 文档 (Swagger)**: http://localhost:8000/docs
- **API 文档 (ReDoc)**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

或使用命令行：

```bash
curl http://localhost:8000/health
```

预期响应：

```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2024-01-01T00:00:00"
}
```

#### 5.2 检查前端应用

在浏览器中访问：

- **前端应用**: http://localhost:3000

你应该看到一个欢迎页面，显示系统状态和功能列表。

### 步骤 6: 运行测试

#### 后端测试

```bash
# 进入后端容器
docker-compose exec backend bash

# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html

# 退出容器
exit
```

#### 前端测试

```bash
# 进入前端容器
docker-compose exec frontend sh

# 运行测试
npm test -- --watchAll=false

# 运行测试并生成覆盖率报告
npm test -- --coverage --watchAll=false

# 退出容器
exit
```

## 🔧 常用命令

### Docker Compose 操作

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启特定服务
docker-compose restart backend

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 重新构建镜像
docker-compose build

# 重新构建并启动
docker-compose up -d --build
```

### 数据库操作

```bash
# 连接到 PostgreSQL
docker-compose exec postgres psql -U stockuser -d stock_db

# 查看数据库表
\dt

# 退出
\q
```

### Redis 操作

```bash
# 连接到 Redis
docker-compose exec redis redis-cli

# 查看所有键
KEYS *

# 获取特定键的值
GET key_name

# 退出
exit
```

## 🐛 常见问题

### 问题 1: 端口已被占用

**错误信息**: `Port 8000 is already allocated`

**解决方案**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# 停止冲突的服务或修改 docker-compose.yml 中的端口映射
```

### 问题 2: Docker 镜像构建失败

**解决方案**:
```bash
# 清理 Docker 缓存
docker-compose down
docker system prune -a

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

### 问题 3: 前端无法连接后端

**检查事项**:
1. 确认 `.env` 文件中的 `REACT_APP_API_URL=http://localhost:8000`
2. 确认后端服务正在运行: `docker-compose ps backend`
3. 检查后端日志: `docker-compose logs backend`

### 问题 4: 数据库连接失败

**解决方案**:
```bash
# 检查 PostgreSQL 服务状态
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres

# 重启数据库
docker-compose restart postgres
```

## 📊 验收检查清单

迭代 0 的验收标准：

- [ ] 运行 `docker-compose up -d` 成功启动所有服务
- [ ] 访问 http://localhost:8000/docs 可见 Swagger API 文档
- [ ] 访问 http://localhost:3000 可见 React 欢迎页面
- [ ] 运行 `pytest` 所有测试通过（覆盖率 > 80%）
- [ ] 运行 `npm test` 前端测试通过
- [ ] 健康检查端点返回 "healthy" 状态

## 🎯 下一步计划

**迭代 1: 股票行情数据获取与展示**

预计交付：
- 股票搜索功能
- 实时/历史行情数据获取
- K线图组件（支持日/周/月切换）
- Redis 缓存优化

详细技术方案请参考项目根目录的技术设计文档。

## 📝 开发建议

1. **代码修改自动重载**:
   - 后端: 支持热重载（uvicorn --reload）
   - 前端: 支持热更新（React Fast Refresh）

2. **添加新依赖**:
   - 后端: 在 `backend/requirements.txt` 添加后运行 `docker-compose up -d --build backend`
   - 前端: 在 `frontend/package.json` 添加后运行 `docker-compose up -d --build frontend`

3. **日志查看**:
   - 实时查看日志: `docker-compose logs -f`
   - 只查看错误: `docker-compose logs | grep ERROR`

4. **性能优化**:
   - 使用 Redis 缓存减少数据库查询
   - 前端使用 React.memo 优化组件渲染

## 🤝 需要帮助？

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 检查 `docker-compose logs` 查看详细错误信息
3. 查阅 README.md 了解项目架构
4. 运行 `python scripts/verify_setup.py` 验证配置

---

**祝开发顺利！** 🚀
