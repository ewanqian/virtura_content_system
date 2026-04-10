# VIRTURA-Content / 接入指南（简版）

## 这是什么
VIRTURA-Content 是一套 file-based 的内容协议层，用来给 portfolio、Collective、SpacePort、Newsroom 和 viewer 提供统一内容源。

## 第一步先做什么
1. 新建 GitHub 仓库：`VIRTURA-Content`
2. 上传初始化目录结构
3. 上传 schemas、content 示例对象、site profiles
4. 在 `VIRTURA-SpacePort/stations/` 下新增 `content-protocol-station/README.md`

## 不要先做什么
- 不要先做重型后台
- 不要先做数据库
- 不要先做拖拽式管理页面
- 不要把 frontend 组件继续当内容源

## 推荐顺序
1. 先有 schema
2. 再有 content objects
3. 再有 generation scripts
4. 再接 portfolio
5. 再扩到 collective / newsroom / viewer

## 第一版目标
只要先把：
- Drop Flow
- TIMER
- Kashiwa
- UFO Terminal
- Hangzhou Opening
- 一个 venue/spec

跑通，就已经成立。
