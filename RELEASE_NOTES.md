# Virtura Node Weaver MCP v1.0.0 - 太空站体系首个正式MCP发布

## 🎉 里程碑意义

标志 VIRTURA 生态从 AI 使用者转型为工具制作者，首个对外发布的标准 MCP 服务。这是一个本地优先的文化基因编织系统，将零散的创作、方法、思想、事件转化为可沉淀、可复用、可关联的标准化节点，实现文化资产的传承与进化。

## ✨ 核心新功能

三大模块完整发布，形成完整闭环能力：

### 1. 投料工厂 (Ingest Factory)
- **批量导入**: 支持聊天记录导出(.txt/.json/.md)、Markdown笔记、图片文件夹、旧数据备份
- **自动元数据提取**: AI识别标题、年份、类型、标签、关联关系
- **双重去重**: 文件哈希+内容指纹双重检测重复内容
- **自然语言审核**: 支持中文指令批量确认/修改提取结果

### 2. Node Weaver CLI (节点编织器命令行)
- **完整命令体系**: `create`创建对象、`link`双向关联、`list`搜索过滤、`show`查看详情、`delete`软删除、`export`多格式导出
- **智能ID生成**: 自动生成格式如`work:drop-flow`、`node:ai-generation-method`的全局唯一Typed ID
- **内置校验**: 基于JSON Schema的数据格式规范验证
- **中文友好**: 全中文输出，符合自然语言指令调用习惯

### 3. MCP 标准服务
- **完全符合 MCP 协议规范**: 所有 Claude 对话和 AI 代理可直接调用
- **核心 API**:
  - `content_system_search`: 搜索内容对象，支持多维度过滤
  - `content_system_get`: 获取对象详情，包含所有关联关系
  - `content_system_create`: 创建新对象，自动ID生成和校验
  - `content_system_link`: 建立对象关联，支持双向关系
  - `content_system_export`: 导出内容，支持JSON/CSV/Markdown格式
- **本地运行**: 无需网络，默认仅返回非敏感内容，安全可靠

## 📋 完整功能列表

### 内容系统核心功能
- **对象管理**: 创建、删除、更新、查询12种标准对象类型
- **关联系统**: 建立和管理对象间的关系网络
- **搜索系统**: 全文搜索、类型/标签/状态/年份过滤
- **导出系统**: 多格式导出支持(JSON/Markdown/CSV)

### 内容类型支持
- **作品 (Work)**: 创作、项目、装置、产品
- **节点 (Node)**: 展览、活动、表演、工作坊
- **资产 (Asset)**: 图片、海报、视频、文件
- **人物 (Person)**: 艺术家、协作者、组织者
- **集体 (Collective)**: 团队、组织、网络
- **关系 (Relation)**: 对象间的关联关系
- **写作 (Writing)**: 文章、评论、研究笔记
- **规范 (Spec)**: 技术规范、交付要求
- **场地 (Venue)**: 空间、展览环境
- **概念 (Concept)**: 想法、理念、理论
- **方法 (Method)**: 工作方法、流程、规范
- **事件 (Event)**: 项目历程、活动、事件

### 数据架构
- **三层核心架构**: Intake 投料层 → Canonical 标准对象层 → Export 导出层
- **三类记忆存储**: Semantic 事实记忆、Episodic 事件记忆、Procedural 流程记忆
- **轻量级关联**: 内置图数据库功能，满足中小规模需求

### 安全特性
- **本地优先**: 数据100%本地存储，完全掌控
- **访问控制**: API密钥认证，敏感字段授权机制
- **审计日志**: 完整的操作记录和追踪

## 🚀 快速开始

```bash
# 1. 解压安装包
unzip virtura-node-weaver-mcp-v1.0.0.zip
cd virtura-node-weaver-mcp-v1.0.0

# 2. 安装依赖
pip install -r cli/requirements.txt
pip install -r scripts/requirements.txt
cd mcp_server && npm install && cd ..

# 3. 配置服务
cp config/mcp_config.example.yaml config/mcp_config.yaml

# 4. 启动MCP服务
./start_mcp_server.sh

# 5. 在浏览器中打开观察器
python3 -m http.server 8080
# 访问 http://localhost:8080/viewer/
```

## 📦 下载包说明

### 包含内容

**核心程序文件**:
- `/cli/`: Node Weaver CLI 源码和依赖
- `/mcp_server/`: MCP 服务实现和配置
- `/scripts/`: 投料工厂和流水线脚本
- `/schemas/`: 完整的数据模型定义
- `/viewer/`: 可视化观察器（静态HTML页面）
- `/node-database-system/`: 节点数据库系统实现

**文档**:
- `README.md`: 项目总览
- `README_CLI.md`: CLI 详细使用说明
- `README_MCP.md`: MCP 服务配置指南
- `INSTALL.md`: 快速安装指南
- `/docs/`: 完整文档目录（架构说明、命令参考、使用指南）

**配置文件**:
- `/config/`: 配置文件模板
- `weaver`: CLI 入口脚本
- `start_mcp_server.sh`: 启动脚本

**示例和归档**:
- `/archive/`: 历史项目架构和示例内容
- `/node_library_mvp_pack/`: MVP 开发计划和文档
- `/incoming/`: 待导入素材目录（初始为空）
- `/data/`: 数据存储目录（包含空的标准结构）

### 目录结构

```
virtura-node-weaver-mcp-v1.0.0/
├── cli/                 # CLI 工具
├── mcp_server/          # MCP 服务
├── scripts/             # 投料工厂和流水线
├── schemas/             # 数据模型
├── docs/                # 文档目录
├── viewer/              # 可视化观察器
├── node-database-system/# 节点数据库系统
├── config/              # 配置文件
├── data/                # 数据存储（初始结构）
├── archive/             # 历史和示例内容
├── README*.md           # 文档文件
├── INSTALL.md           # 本文件
└── weaver/start_mcp_server.sh  # 入口脚本
```

## 📖 文档资源

- **架构说明**: `/docs/CONTENT_SYSTEM_STRATEGY.md`
- **命令参考**: `/docs/COMMANDS.md`
- **快速开始**: `/docs/MVP_ONBOARDING.md`
- **工厂流水线**: `/docs/FACTORY_PIPELINE.md`
- **MCP 接口**: `/docs/COMMANDS_MCP.md`
- **API 文档**: `/docs/gh-pages/api.html`
- **使用示例**: `/docs/gh-pages/examples.html`

## 🔧 系统要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本（仅 MCP 服务）
- **操作系统**: macOS 10.15+, Windows 10/11, Linux (Ubuntu 20.04+)
- **内存**: 至少 2GB，建议 4GB 以上
- **存储**: 至少 100MB 可用空间

## 📝 License

MIT License

---

**发布日期**: 2026年04月13日
**项目地址**: https://github.com/ewanqian/virtura_content_system
**技术支持**: 请访问项目 GitHub 仓库提交 Issue

---
