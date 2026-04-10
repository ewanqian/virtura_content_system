# 给本地 coder 的任务清单

## 本轮目标
让 Node Library 真正进入可用状态，而不是继续停留在概念 demo。

---

## P0｜马上做
1. 明确仓库首页的双层关系：
   - 仓库 / 系统名：virtura_content_system
   - 产品名：Node Library
2. 替换 README 为产品化版本
3. 保证 viewer 能稳定读取本地 `data/nodes.json`
4. 保证图片路径在本地运行下不丢失
5. 把导出目录建好：
   - exports/website
   - exports/portfolio
   - exports/review-sheets
   - exports/brief-packs

---

## P1｜这一轮补上
1. 增加 markdown brief pack 导出脚本
2. 增加 review CSV 导出脚本
3. 增加 clean JSON 导出脚本
4. 在界面里或脚本里保留：
   - owner
   - type
   - related work
   - year
   - featured
   - notes
5. 不要急着上视频支持

---

## P2｜下一轮做
1. 增加 event / venue / note 三类对象
2. 让 brief pack 可以包含事件、场地和用途建议
3. 为 portfolio 生成 clean data 包

---

## 这轮不要做
- 不要做重型在线 CMS
- 不要做复杂用户系统
- 不要做过度花哨动画
- 不要先拆太多仓库
