# Node Library MVP 执行计划

## 总目标
两周内把 Node Library 跑到“我今天就能拿它整理内容”的状态。

---

## Phase 1｜今天就要能用
### 目标
本地启动 + 导图 + 看图 + 分类 + 搜索

### 要做的事
1. 保持当前本地 viewer 可运行
2. 确认 `data/nodes.json` 可被界面读取
3. 保证 5 个主视图可工作：
   - Image Wall
   - Practice Map
   - Archive
   - 荣誉墙
   - Public Nodes
4. 修复所有本地图片路径问题
5. 建立最小目录约定：
   - incoming
   - processed
   - thumbs
   - manifests
   - exports

### 完成标准
- 双击或命令启动后能看到界面
- 新图片进入后能被 ingest
- 能在 viewer 中看到结果
- 能搜索、筛选、点开详情

---

## Phase 2｜这周内跑顺
### 目标
让它真正开始替代“手动混乱整理”

### 要做的事
1. 完成 ingest 流程
   - 重命名
   - hash
   - 缩略图
   - 生成初始节点
2. 补人工 review 字段
   - owner
   - type
   - work
   - year
   - featured
   - duplicate
   - notes
3. 导出三种结果：
   - clean JSON
   - review CSV
   - markdown brief pack
4. README 改成产品 README，而不是实验说明

### 完成标准
- 我能把一个项目的图全部丢进去
- 它能帮我初步整理
- 我能快速 review
- 我能导出一个包给 GPT / Trae / SoloCoder

---

## Phase 3｜下周开始扩展
### 目标
从“图片整理器”升级成“内容节点工具”

### 要做的事
1. 增加 event 结构
2. 增加 venue 结构
3. 增加 note 结构
4. markdown brief pack 里写入：
   - current assets
   - related events
   - venue/spec notes
   - suggested uses
5. 为 portfolio 输出 clean data

### 完成标准
- 同一个项目不只是有图，还有事件、场地、说明
- agent 能接到更完整的上下文
- portfolio 能吃到导出的 clean data

---

## 暂不做
- 重型数据库后台
- 在线协作编辑
- 完整视频资产处理
- 全自动多站同步

---

## 当前最重要的执行原则
1. 先用起来，再抽象
2. 先导出 clean data，再谈多站系统
3. 先保证本地工作流稳定，再考虑拆仓
4. 页面不是重点，整理和导出才是重点
