# 项目文件组织说明

**整理日期**: 2026-03-02
**整理目的**: 规范项目文件结构，提升可维护性

---

## 📁 整理前后对比

### 整理前（根目录混乱）
```
根目录文件数量: 25+
- 多个迭代文档散落
- 测试文件混杂
- 中英文文档混合
- 缺少分类结构
```

### 整理后（清晰结构）
```
根目录文件数量: 16
- 核心文档: 3个 (README, PRD, ROADMAP)
- 配置文件: 3个 (.env*, .gitignore, docker-compose.yml)
- 启动脚本: 2个 (start-demo.*)
- 代码文件: 1个 (mock-server.js)
- 文件夹: 7个 (结构化组织)
```

---

## 🗂️ 新的文件结构

### 根目录（Root）
```
stock-analysis/
├── PRD.md                     # 产品需求文档
├── README.md                  # 项目说明
├── PROJECT_ROADMAP.md         # 项目路线图（新建）
├── docker-compose.yml         # Docker配置
├── mock-server.js             # Mock服务器
├── start-demo.bat             # Windows启动脚本
├── start-demo.sh              # Linux/Mac启动脚本
├── .env / .env.example        # 环境变量
├── .gitignore                 # Git忽略配置
```

### docs/（文档目录）
```
docs/
├── iterations/                # 迭代文档
│   ├── ITERATION_0_SUMMARY.md
│   ├── ITERATION_1_SUMMARY.md
│   ├── ITERATION_2_DEMO.md
│   └── ITERATION_2_TEST_REPORT.md
│
├── guides/                    # 使用指南
│   ├── QUICKSTART.md
│   ├── START_DEMO.md
│   ├── 成品使用指南.md
│   └── 迭代2-技术指标展示指南.md
│
├── api/                       # API文档
│   └── API测试示例.md
│
└── PROJECT_STATUS.md          # 项目状态
```

### tests/（测试目录）
```
tests/
├── manual/                    # 手动测试
│   ├── test_indicators_direct.py
│   ├── test_indicators_standalone.py
│   └── test_indicators.json
│
└── e2e/                       # 端到端测试（未来）
```

### backend/（后端代码）
```
backend/
├── app/
│   ├── api/                   # API路由
│   ├── models/                # 数据模型
│   ├── services/              # 业务逻辑
│   └── tests/                 # 单元测试
├── requirements.txt
└── Dockerfile
```

### frontend/（前端代码）
```
frontend/
├── src/
│   ├── components/            # React组件
│   ├── pages/                 # 页面
│   ├── services/              # API服务
│   └── utils/                 # 工具函数
├── package.json
└── Dockerfile
```

### 其他目录
```
├── scripts/                   # 工具脚本
├── openspec/                  # OpenSpec工作流
├── .claude/                   # Claude Code配置
├── logs/                      # 日志目录
└── venv/                      # Python虚拟环境
```

---

## 🔄 文件迁移清单

### 迭代文档 → docs/iterations/
- ✅ ITERATION_0_SUMMARY.md
- ✅ ITERATION_1_SUMMARY.md
- ✅ ITERATION_2_DEMO.md
- ✅ ITERATION_2_TEST_REPORT.md

### 使用指南 → docs/guides/
- ✅ QUICKSTART.md
- ✅ START_DEMO.md
- ✅ 成品使用指南.md
- ✅ 迭代2-技术指标展示指南.md

### API文档 → docs/api/
- ✅ API测试示例.md

### 项目状态 → docs/
- ✅ PROJECT_STATUS.md

### 测试文件 → tests/manual/
- ✅ test_indicators_direct.py
- ✅ test_indicators_standalone.py
- ✅ test_indicators.json

### 删除文件
- ✅ nul（无用文件）

---

## 📝 新建文档

### PROJECT_ROADMAP.md（项目路线图）
**位置**: 根目录
**内容**:
- 完整的10个迭代规划
- Q1/Q2/Q3分期目标
- 技术债务管理
- 关键里程碑
- 进度追踪

**特点**:
- 基于PRD的未来规划重新梳理
- 明确每个迭代的目标和验收标准
- 提供清晰的开发路线图

---

## 🎯 组织原则

### 1. 文档分类
- **核心文档**: 放在根目录（PRD, README, ROADMAP）
- **迭代文档**: 按迭代编号组织在 `docs/iterations/`
- **使用指南**: 用户相关文档放在 `docs/guides/`
- **技术文档**: API文档放在 `docs/api/`

### 2. 测试分类
- **手动测试**: `tests/manual/`
- **自动化测试**: 后端在 `backend/app/tests/`，前端在 `frontend/src/__tests__/`
- **端到端测试**: `tests/e2e/`（未来）

### 3. 代码组织
- **前端**: `frontend/` 独立目录
- **后端**: `backend/` 独立目录
- **脚本**: `scripts/` 工具脚本
- **配置**: `.claude/`、`openspec/` 等

### 4. 临时文件
- **日志**: `logs/` 目录
- **缓存**: 在 `.gitignore` 中排除
- **虚拟环境**: `venv/` 保持在根目录

---

## 📋 文档索引

### 快速访问指南

#### 新用户
1. 阅读 [README.md](../README.md) - 了解项目
2. 查看 [PRD.md](../PRD.md) - 理解产品需求
3. 参考 [docs/guides/QUICKSTART.md](guides/QUICKSTART.md) - 快速开始

#### 开发人员
1. 查看 [PROJECT_ROADMAP.md](../PROJECT_ROADMAP.md) - 了解路线图
2. 阅读迭代文档 - 了解各功能模块
3. 参考API文档 - 了解接口规范

#### 测试人员
1. 查看 [docs/guides/START_DEMO.md](guides/START_DEMO.md) - 启动演示环境
2. 参考 [docs/api/API测试示例.md](api/API测试示例.md) - API测试
3. 使用 `tests/manual/` 中的测试脚本

---

## 🔍 查找文档速查表

| 需要 | 查看文档 | 路径 |
|------|---------|------|
| 项目介绍 | README.md | 根目录 |
| 产品需求 | PRD.md | 根目录 |
| 开发计划 | PROJECT_ROADMAP.md | 根目录 |
| 迭代总结 | ITERATION_*.md | docs/iterations/ |
| 使用教程 | 使用指南 | docs/guides/ |
| API文档 | API测试示例 | docs/api/ |
| 项目状态 | PROJECT_STATUS.md | docs/ |
| 测试脚本 | test_*.py | tests/manual/ |

---

## ✅ 整理成果

### 改进效果
1. **根目录清爽**: 文件数量减少40%
2. **分类明确**: 文档、测试、代码分离
3. **易于查找**: 按类型和功能组织
4. **维护性强**: 新文件有明确归属

### 新增价值
1. **PROJECT_ROADMAP.md**: 提供清晰的开发路线图
2. **文档分类**: 迭代、指南、API三类文档
3. **测试组织**: manual、e2e分类清晰
4. **组织文档**: 本文档说明整理逻辑

---

## 📊 文件统计

### 整理前
```
根目录: 25+ 文件
├── .md文档: 12个
├── .py文件: 3个
├── .json文件: 1个
├── 配置文件: 4个
└── 其他: 5+个
```

### 整理后
```
根目录: 16 文件
├── 核心文档: 3个
├── 配置文件: 3个
├── 脚本: 3个
└── 文件夹: 7个

docs/目录: 3个子目录
├── iterations/: 4个文档
├── guides/: 4个文档
└── api/: 1个文档

tests/目录: 1个子目录
└── manual/: 3个文件
```

---

## 🔮 未来规划

### 文档扩展
- [ ] 添加 `docs/architecture/` - 架构设计文档
- [ ] 添加 `docs/development/` - 开发指南
- [ ] 添加 `docs/deployment/` - 部署文档
- [ ] 添加 `CHANGELOG.md` - 变更日志

### 测试扩展
- [ ] 添加 `tests/e2e/` - 端到端测试
- [ ] 添加 `tests/integration/` - 集成测试
- [ ] 添加 `tests/performance/` - 性能测试

### 持续优化
- 每个迭代结束后更新文档
- 定期review文件组织
- 保持根目录简洁
- 及时归档过时文档

---

## 📞 维护说明

### 添加新文档
1. **迭代文档**: 放入 `docs/iterations/ITERATION_N_*.md`
2. **使用指南**: 放入 `docs/guides/`
3. **API文档**: 放入 `docs/api/`
4. **测试文件**: 放入 `tests/manual/` 或其他测试目录

### 文档命名规范
- **迭代文档**: `ITERATION_N_SUMMARY.md` 或 `ITERATION_N_DEMO.md`
- **使用指南**: 描述性名称，如 `技术指标使用指南.md`
- **测试文件**: `test_*.py` 或 `*_test.py`

### 定期清理
- 每季度review一次文件组织
- 归档过时文档到 `docs/archived/`
- 删除临时测试文件
- 更新 PROJECT_STATUS.md

---

**整理人**: Claude Sonnet 4.5
**整理日期**: 2026-03-02
**版本**: v1.0
