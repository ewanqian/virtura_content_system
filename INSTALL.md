# 快速安装指南

## 系统要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本（仅 MCP 服务需要）
- **操作系统**: macOS 10.15+, Windows 10/11, Linux (Ubuntu 20.04+)

## 快速开始

### 1. 下载并解压

```bash
unzip virtura-node-weaver-mcp-v1.0.0.zip
cd virtura-node-weaver-mcp-v1.0.0
```

### 2. 安装依赖

```bash
# 安装 Python 依赖
pip install -r cli/requirements.txt
pip install -r scripts/requirements.txt

# 安装 MCP 服务依赖（可选，如需使用 MCP 服务）
cd mcp_server && npm install && cd ..
```

### 3. 初始化配置

```bash
# 复制配置文件
cp config/mcp_config.example.yaml config/mcp_config.yaml
```

### 4. 验证安装

```bash
# 测试 CLI 工具
./weaver --help

# 测试 MCP 服务（可选）
./start_mcp_server.sh
```

## 功能模块

### 🎯 投料工厂 (Ingest Factory)
批量导入各种原始素材，自动结构化提取元数据。

```bash
# 导入素材
python3 scripts/factory_ingest.py import --dir incoming/

# 审核待处理项目
python3 scripts/factory_ingest.py review --list

# 确认审核
python3 scripts/factory_ingest.py review --confirm "批准所有"
```

### 🧬 Node Weaver CLI
命令行工具，用于管理和操作内容对象。

```bash
# 创建对象
./weaver create --type work --title "我的作品" --summary "作品描述"

# 列出对象
./weaver list --type work

# 建立关联
./weaver link --object1 work:my-work --object2 node:my-node --relation uses_method

# 导出内容
./weaver export --all --format json
```

### 🔌 MCP 服务
符合 Anthropic MCP 协议标准的服务，供 AI 助手调用。

```bash
# 启动 MCP 服务
./start_mcp_server.sh
```

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "virtura-content": {
      "command": "node",
      "args": ["/path/to/virtura-node-weaver-mcp-v1.0.0/mcp_server/src/index.js"]
    }
  }
}
```

### 👁️ 可视化观察器
纯静态页面，打开即可查看内容库。

```bash
# 启动本地服务器
python3 -m http.server 8080
```

然后在浏览器中打开：`http://localhost:8080/viewer/`

## 目录结构

```
virtura-node-weaver-mcp-v1.0.0/
├── cli/                    # CLI 工具源码
├── mcp_server/             # MCP 服务源码
├── scripts/                # 投料工厂和流水线脚本
├── schemas/                # 数据模型定义
├── docs/                   # 完整文档
├── viewer/                 # 可视化观察器
├── config/                 # 配置文件
├── data/                   # 数据目录（初始为空）
│   ├── intake/             # 投料暂存区
│   ├── objects/            # 标准对象存储
│   └── memory/             # 记忆存储
├── incoming/               # 待导入素材目录
├── exports/                # 导出目录
├── README.md               # 项目说明
├── README_CLI.md           # CLI 详细文档
├── README_MCP.md           # MCP 服务文档
├── INSTALL.md              # 本文件
└── weaver                  # CLI 入口脚本
```

## 下一步

- 查看 [README.md](./README.md) 了解项目全貌
- 查看 [README_CLI.md](./README_CLI.md) 了解 CLI 详细用法
- 查看 [README_MCP.md](./README_MCP.md) 了解 MCP 服务配置
- 查看 [docs/](./docs/) 目录获取完整文档

## 常见问题

### Q: 权限被拒绝？
A: 确保脚本有执行权限：
```bash
chmod +x weaver start_mcp_server.sh
```

### Q: Python 依赖安装失败？
A: 尝试使用虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
.\venv\Scripts\activate  # Windows
pip install -r cli/requirements.txt
```

### Q: 需要更多帮助？
A: 访问 [docs/](./docs/) 目录查看详细文档，或访问项目 GitHub 仓库。

---

**许可证**: MIT License
**版本**: v1.0.0
**发布日期**: 2026-04-13
