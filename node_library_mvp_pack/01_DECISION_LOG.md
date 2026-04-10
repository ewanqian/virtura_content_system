# Node Library / VIRTURA Content System
## 决议记录（MVP 版）

## 本轮决议

### 1. 保留上位系统名
保留 `virtura_content_system` 作为上位系统 / 协议层 / 架构层名称。

它负责：
- 内容协议
- 导出逻辑
- 与 VIRTURA 生态的关系
- future skills / agents / site profiles
- portfolio / collective / newsroom / viewer 的共通逻辑

### 2. 建立产品名
将本地可下载、可运行、可整理素材、可导出给 agent 的工具明确命名为：

# Node Library

副标题建议：
**A local-first asset and content organizer for agent workflows**

中文可写：
**一个面向本地整理、内容导出与 agent 工作流的节点化内容工具**

### 3. 近期不拆双仓独立演化
当前阶段不建议把 `Node Library` 完全拆成一个独立逻辑仓，再让 `virtura_content_system` 另走一套。

更稳的方式是：
- 继续使用 `virtura_content_system` 作为主仓
- 在仓内明确 `Node Library` 是第一号产品实例
- 先把 ingest / review / export / brief pack 跑顺
- 等工作流稳定后，再考虑是否拆独立产品仓

### 4. 当前目标
当前不是做重型 CMS，也不是做完整多站协议发布。

当前目标只有一个：

# 让 Node Library 尽快可用，支持你开始整理内容，并能导出给 agent / 网站 / 作品集使用

---

## MVP 的范围

### 必做
- 本地运行查看器
- 支持图片 ingest / 索引 / 分类
- 支持 review / featured / duplicate 标记
- 支持按 project / year / owner / type 查看
- 支持导出 markdown brief pack
- 支持导出 JSON clean data
- 支持导出 review CSV

### 暂缓
- 视频完整支持
- 文档 / PDF 深度处理
- 场地 viewer 全功能
- 多站同步自动化
- 完整 web admin
- 完整 schema validator

---

## 当前产品定义

Node Library 不是只做图片墙。
它的真正角色是：

- 本地素材整理器
- 节点式内容组织器
- agent 可调用的导出器
- portfolio / VIRTURA 内容系统的前置整理层

---

## 第一阶段对象模型（简化版）

目前先支持 5 类对象：

1. asset
2. work
3. event
4. venue
5. note

说明：
先不要把 schema 做得过重。先让这五类对象足以支撑：
- 图片整理
- 项目归类
- 公开节点
- 场地与规格备注
- brief 输出

等跑顺以后，再进入更完整的：
- person
- collective
- writing
- spec
- relation
