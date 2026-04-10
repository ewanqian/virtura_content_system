# Node Library
### A local-first asset and content organizer for agent workflows

Node Library 是一个本地优先的内容整理工具，用来帮助个人或团队把零散图片、项目记录、公开节点、场地信息与整理说明，逐步组织成可被 agent、网站、作品集与媒体包使用的 clean data。

它不是传统的网页 CMS，也不是只用来看图的素材文件夹。
它更像一个“节点式内容整理器”：

- 把素材变成节点
- 把节点挂到作品 / 事件 / 场地 / 用途上
- 最后导出给 agent 和网站使用

---

## 它适合谁

- 正在整理个人作品集的人
- 正在维护团队素材库的人
- 需要给 agent 提供可用上下文的人
- 需要为 portfolio / website / media kit 提供 clean data 的人

---

## 当前能做什么

- 导入图片
- 自动生成缩略图与基础索引
- 在本地 viewer 里浏览内容
- 按 type / owner / project / year 查看
- 做 featured / duplicate 标记
- 导出给网站、作品集或 agent 使用的数据包

---

## 它不是什么

- 不是在线后台
- 不是多用户 SaaS
- 不是最终网站
- 不是完整 DAM 企业系统

---

## 当前的五个主要视图

- Image Wall
- Practice Map
- Archive
- 荣誉墙
- Public Nodes

---

## 推荐工作流

1. 把新图放进 incoming
2. 跑 ingest
3. 自动生成缩略图、基础记录和 hash
4. 在 viewer 中检查与筛选
5. 用 agent 辅助补标题、项目、说明、用途
6. 人工 review
7. 导出：
   - clean JSON
   - review CSV
   - markdown brief pack

---

## 导出类型

### 1. JSON clean data
给网站和程序用

### 2. Review CSV
给人工快速整理

### 3. Markdown Brief Pack
给 GPT / Claude / Trae / SoloCoder 这种 agent 使用

---

## 和 VIRTURA 的关系

Node Library 是 `virtura_content_system` 的第一号本地产品实例。

- `virtura_content_system` 负责上位内容协议与未来多站接入
- `Node Library` 负责本地整理、review、导出与 agent 工作流

也就是说：

Node Library 是可立即使用的工具；
virtura_content_system 是它的上位系统与未来扩展框架。

---

## 当前阶段目标

当前目标不是做大，而是尽快跑顺：

- 我能开始整理内容
- 我能导出给 agent 使用
- 我能给 portfolio 提供 clean data
- 我能一点一点把本地数据库做起来
