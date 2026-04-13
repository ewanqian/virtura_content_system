# Virtura Content System - MCP Server

这是一个符合 Anthropic Model Context Protocol (MCP) 标准的服务，用于与 Virtura Content System 交互。

## 功能特性

### 核心 MCP 工具

1. **content_system_search** - 搜索内容对象
   - 支持关键词搜索
   - 按类型过滤
   - 按标签过滤
   - 按年份过滤
   - 分页支持

2. **content_system_get** - 获取对象详情
   - 接受 Typed ID 参数（格式：type:id）
   - 返回对象的完整详情
   - 包含所有关联关系

3. **content_system_create** - 创建新对象
   - 支持所有内容类型
   - 自动生成或自定义 ID
   - 完整的字段验证

4. **content_system_link** - 建立对象关联
   - 双向关系支持
   - 多种关系类型
   - 可附加描述和元数据

5. **content_system_export** - 导出内容
   - JSON、CSV、Markdown 格式
   - 灵活的过滤条件
   - 按 ID 批量导出

### 安全特性

- 默认仅返回非敏感内容
- 敏感字段需要显式授权
- 支持 API 密钥认证
- 完整的审计日志

## 安装

```bash
cd mcp_server
npm install
```

## 配置

复制示例配置文件：

```bash
cp ../config/mcp_config.example.yaml ../config/mcp_config.yaml
```

编辑 `../config/mcp_config.yaml` 配置文件以设置：

- 服务器端口和主机
- 内容目录路径
- 安全设置
- 日志选项

## 使用方法

### 作为 stdio 服务器（默认，用于 Claude Desktop）

```bash
cd mcp_server
npm start
```

### 作为 HTTP 服务器

```bash
cd mcp_server
npm start -- --http
```

### 配置 Claude Desktop

在 Claude Desktop 配置文件中添加：

```json
{
  "mcpServers": {
    "virtura-content": {
      "command": "node",
      "args": ["/path/to/virtura_content_system/mcp_server/src/index.js"]
    }
  }
}
```

## 命令文档

详细的命令使用说明请参考 [docs/COMMANDS.md](./docs/COMMANDS.md)。

## 运行测试

```bash
cd mcp_server
npm test
```

## 目录结构

```
virtura_content_system/
├── config/
│   ├── mcp_config.example.yaml
│   └── mcp_config.yaml (需要创建)
├── mcp_server/
│   ├── src/
│   │   ├── index.js          # 服务器入口
│   │   ├── config.js         # 配置加载
│   │   ├── logger.js         # 日志系统
│   │   ├── contentStore.js   # 内容存储和查询
│   │   └── tools/            # MCP 工具
│   │       ├── search.js
│   │       ├── get.js
│   │       ├── create.js
│   │       ├── link.js
│   │       ├── export.js
│   │       └── index.js
│   ├── test/
│   │   └── test.js           # 测试脚本
│   ├── logs/                 # 日志文件目录
│   └── package.json
├── docs/
│   └── COMMANDS.md
└── README_MCP.md
```

## 内容类型

支持以下内容类型：

- `person` - 艺术家、协作者、组织者
- `collective` - 团队、组织、网络
- `work` - 作品、系列、项目
- `node` - 公开呈现、营地、表演、展览、工作坊
- `asset` - 图片、海报、视频、文件
- `writing` - 文章、评论、研究笔记、策展文本
- `venue` - 空间、放映环境、播放上下文
- `spec` - 分辨率、帧率、编码、硬件、交付要求
- `relation` - 对象间的关系

## 许可

MIT License
