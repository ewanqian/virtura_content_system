# Virtura Content System - Node Weaver
### 🧬 个人/团队文化基因结构化存储与编织系统 | Local-First, Agent-Native

Node Weaver 是 VIRTURA 内容系统的核心本地工具，从原 Node Library 升级而来，目标是把零散的创作、方法、思想、事件转化为可沉淀、可复用、可关联的标准化节点，实现文化基因的传承与进化。

它不是传统的CMS，不是素材库，不是笔记软件，它是**文化基因编织器**：
- 把各种形式的原始素材变成结构化的标准节点
- 建立节点之间的关联关系，形成知识图谱
- 沉淀为长期可复用的文化资产，给AI、网站、作品集、团队协作使用

---

## ✨ 核心特性

### 🎯 三层核心架构
| 层级 | 功能 |
|------|------|
| **Intake 投料层** | 批量导入各种原始素材，自动结构化提取元数据 |
| **Canonical 标准对象层** | 统一格式的标准对象：作品/节点/资产/关系/概念/方法/事件 |
| **Export 导出层** | 输出各种格式给不同使用场景 |

### 🧠 三类记忆存储（对齐AI记忆架构）
- **Semantic 事实记忆**：作品、资产、概念、方法等稳定事实
- **Episodic 事件记忆**：项目历程、活动、事件等发生过的内容
- **Procedural 流程记忆**：工作方法、流程、规范等可复用的经验

### 🛠️ 四大核心模块
1. **投料工厂（Ingest Factory）**
   - 支持批量导入：聊天记录导出(.txt/.json/.md)、Markdown笔记、图片文件夹、旧数据备份
   - 自动元数据提取：AI识别标题、年份、类型、标签、关联关系
   - 自动去重：文件哈希+内容指纹双重检测重复内容
   - 自然语言审核：支持中文指令批量确认/修改提取结果

2. **Node Weaver CLI（节点编织器命令行）**
   - 核心命令：`create`创建对象、`link`双向关联、`list`搜索过滤、`show`查看详情、`delete`软删除、`export`多格式导出
   - 自动生成全局唯一Typed ID：格式如`work:drop-flow`、`node:ai-generation-method`
   - 内置Schema校验：保证数据格式规范统一
   - 全中文友好输出，适合自然语言指令调用

3. **MCP 标准服务**
   - 符合Anthropic MCP协议规范，所有Claude对话和AI代理可直接调用
   - 核心API：搜索内容、获取对象详情、创建对象、建立关联、导出内容
   - 本地运行，不需要网络，默认仅返回非敏感内容，安全可靠
   - 支持与workspace tracker无缝对接

4. **全中文可视化观察器**
   - 5种视图：系统概览、作品地图、资产墙、归档、公共信号
   - 直观查看内容密度、关联关系、公共信号
   - 纯静态页面，不需要服务端，打开即可使用

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+（仅MCP服务需要）

### 1. 安装依赖
```bash
# 安装Python依赖
pip install -r cli/requirements.txt
pip install -r scripts/requirements.txt

# （可选）安装MCP服务依赖
cd mcp_server && npm install
```

### 2. 跑通第一个流程
```bash
# 1. 把要导入的素材放进incoming目录
# 2. 投料工厂批量导入，生成待审核清单
python3 scripts/factory_ingest.py import --dir incoming/

# 3. 查看待审核项目
python3 scripts/factory_ingest.py review --list

# 4. 审核确认，生成标准对象
python3 scripts/factory_ingest.py review --confirm "批准所有"

# 5. 一键运行全流水线，生成viewer数据
python3 scripts/build_pipeline.py

# 6. 启动本地服务查看可视化界面
python3 -m http.server 8080
# 打开 http://localhost:8080/viewer/ 即可浏览
```

### 3. 快速操作示例
```bash
# 列出所有作品
./weaver list --type work

# 创建新节点
./weaver create --type node --title "AI生成工作流" --tags "AI,工作流"

# 给两个对象建立关联
./weaver link --object1 work:drop-flow --object2 node:ai-generation-workflow --relation uses_method

# （可选）启动MCP服务，让其他AI对话可以访问你的内容库
./start_mcp_server.sh
```

---

## 🔗 和 Workspace Tracker 的关系
两个系统是互补的分层架构，边界清晰，天然打通：
| 系统 | 定位 | 存储内容 |
|------|------|----------|
| **Content System（本项目）** | 📦 长期沉淀层 | 已经固化的、有长期价值的内容对象 |
| **Workspace Tracker** | ⚡ 过程执行层 | 正在进行的任务、对话上下文、临时决策 |

**协作规则**：Workspace Tracker执行过程中可以直接检索Content System的历史资源，任务完成后一键沉淀到Content System成为标准节点。

---

## ❓ 它不是什么
- ❌ 不是在线SaaS服务，完全本地优先，数据100%归你所有
- ❌ 不是传统笔记软件，不支持自由编辑，只维护结构化标准对象
- ❌ 不是企业级DAM系统，专注个人/小型团队的文化基因沉淀
- ❌ 不是图数据库，内置轻量级关联能力，满足中小规模需求

---

## 📚 文档索引
- [架构说明](./docs/CONTENT_SYSTEM_STRATEGY.md)：核心设计思路和架构规划
- [命令参考](./docs/COMMANDS.md)：所有脚本和CLI命令的详细说明
- [新手引导](./docs/MVP_ONBOARDING.md)：从零开始使用的完整指南
- [工厂流水线](./docs/FACTORY_PIPELINE.md)：投料工厂的详细工作流程
- [Workspace Tracker对接协议](./docs/WORKSPACE_TRACKER_HANDOFF.md)：两个系统的对接规范
- [优先级规划](./docs/PRIORITY_BACKLOG.md)：后续开发计划
- [CLI工具使用说明](./README_CLI.md)：Node Weaver CLI详细文档
- [MCP服务使用说明](./README_MCP.md)：MCP服务安装配置指南

---

## 当前阶段
✅ MVP已完成，具备完整的闭环能力，可以投入日常使用。
目标是尽快跑顺工作流，把分散的内容逐步沉淀为标准化的文化资产。

---

## License
MIT
