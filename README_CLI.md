# Node Weaver CLI 工具

Node Weaver CLI 是一个命令行工具，用于管理和操作 node library 中的对象。它提供了创建、链接、列出、显示、删除和导出对象等功能。

## 安装

### 1. 检查依赖

Node Weaver CLI 需要 Python 3.6 或更高版本，并依赖 `jsonschema` 库进行数据验证。

```bash
python --version
```

### 2. 安装依赖

```bash
cd /path/to/virtura_content_system
pip install -r cli/requirements.txt
```

### 3. 使脚本可执行（可选）

如果还没有执行权限，可以运行：

```bash
chmod +x /path/to/virtura_content_system/weaver
```

### 4. 验证安装

```bash
./weaver --help
```

如果看到帮助信息，说明安装成功。

## 快速开始

### 基本用法

Node Weaver CLI 支持多种命令，主要包括：

```bash
weaver [命令] [选项]
```

### 创建第一个对象

使用交互式模式创建一个新对象：

```bash
weaver create --interactive
```

或者使用参数模式：

```bash
weaver create --type work --title "我的新项目" --summary "项目描述" --status active
```

### 列出对象

列出所有工作类型的对象：

```bash
weaver list --type work
```

### 显示对象详情

显示特定对象的详细信息：

```bash
weaver show --object work:my-project
```

## 命令参考

### create - 创建新对象

#### 交互式模式

```bash
weaver create --interactive
```

#### 参数模式

```bash
weaver create --type <类型> --title <标题> [选项]
```

**选项：**
- `-t, --type`: 对象类型 (必须)
  - 支持类型：asset, work, node, event, venue, note, person, collective, writing, spec, relation, concept, method
- `-T, --title`: 对象标题 (必须)
- `-S, --summary`: 对象摘要
- `-s, --status`: 对象状态 (默认: draft)
  - 可选值：draft, active, archived
- `-c, --context`: 主要上下文 (默认: shared)
  - 可选值：personal, collective, shared, external

### list - 列出对象

```bash
weaver list [选项]
```

**选项：**
- `-t, --type`: 按类型筛选
- `-g, --tag`: 按标签筛选
- `-s, --status`: 按状态筛选
- `-d, --detail`: 显示详细信息
- `--sort`: 排序字段 (默认: updated)
  - 可选值：title, id, type, status, updated

### show - 显示对象详情

```bash
weaver show --object <对象ID>
```

**选项：**
- `-o, --object`: 要显示的对象ID (必须)

### delete - 删除对象（软删除）

```bash
weaver delete --object <对象ID>
```

**选项：**
- `-o, --object`: 要删除的对象ID (必须)

### link - 链接两个对象

```bash
weaver link --object1 <对象1ID> --object2 <对象2ID> --relation-type <关系类型>
```

**选项：**
- `-1, --object1`: 第一个对象的ID (必须)
- `-2, --object2`: 第二个对象的ID (必须)
- `-r, --relation-type`: 关系类型 (默认: related)

### export - 导出对象

```bash
weaver export [--all | --objects <ID1> <ID2> ...] --format <格式> --output <输出目录>
```

**选项：**
- `-a, --all`: 导出所有对象
- `-o, --objects`: 要导出的对象ID列表
- `-f, --format`: 导出格式 (必须)
  - 可选值：json, markdown, csv
- `-O, --output`: 输出目录 (默认: ./exports)

## 使用示例

### 1. 创建工作对象

```bash
weaver create --type work --title "上海广播艺术中心" --summary "大型新媒体艺术装置" --status active --context shared
```

### 2. 创建节点对象并链接到工作

```bash
weaver create --type node --title "上海展览" --summary "2023年在上海的展览" --status active
weaver link --object1 work:shanghai-broadcast-arts-center --object2 node:shanghai-exhibition --relation-type "presented_as"
```

### 3. 列出所有活跃的工作和节点

```bash
weaver list --status active --type work --detail
weaver list --status active --type node --detail
```

### 4. 导出数据

导出所有对象为 JSON 格式：

```bash
weaver export --all --format json --output ./my-exports
```

导出特定对象为 CSV 格式：

```bash
weaver export --objects work:shanghai-broadcast-arts-center node:shanghai-exhibition --format csv --output ./my-exports
```

## 高级功能

### 自动 ID 生成

Node Weaver CLI 会根据对象类型和标题自动生成唯一的类型化 ID。例如：
- 工作类型的 "上海广播艺术中心" 会生成：`work:shanghai-broadcast-arts-center`
- 节点类型的 "上海展览" 会生成：`node:shanghai-exhibition`

### 数据验证

所有创建和修改的对象都会根据 `schemas/content-object.schema.json` 进行验证，确保数据格式符合规范。

### 软删除

使用 `delete` 命令会将对象的状态标记为 `deprecated` 而不是物理删除，保留了数据完整性。

### 上下文

每个对象可以有不同的主要上下文：
- `personal`: 个人使用
- `collective`: 团队内部使用
- `shared`: 共享使用
- `external`: 外部使用

## 项目结构

Node Weaver CLI 的主要文件位于项目根目录下的 `cli/` 文件夹中：

```
cli/
├── __init__.py       # 包初始化文件
├── __main__.py       # 主入口脚本
├── commands.py       # 命令实现
├── utils.py          # 通用工具函数
└── requirements.txt  # 依赖列表
```

## 与其他系统的交互

Node Weaver CLI 与项目的其他部分紧密集成：

1. 数据存储在 `data/objects/` 目录中
2. 数据格式定义在 `schemas/` 目录中
3. 导出的数据可以直接用于网站、作品集或 agent 使用

## 常见问题

### Q: 我如何查看可用的对象类型？

A: 使用 `weaver list --help` 命令查看支持的对象类型。

### Q: 如何导入已有的数据？

A: 目前 CLI 工具不支持直接导入，但您可以通过手动修改 `data/objects/` 目录下的 JSON 文件来添加数据。

### Q: 我可以在其他目录使用 CLI 吗？

A: 可以，但最好在项目根目录运行 CLI 以确保正确的路径解析。

### Q: 如何重置对象到初始状态？

A: 可以使用 `weaver delete` 命令进行软删除，或直接修改对象的状态。

## 更新日志

### v1.0.0

- 初始版本
- 支持创建、链接、列出、显示、删除和导出命令
- 支持类型化 ID 和数据验证
- 提供交互式和参数式操作
