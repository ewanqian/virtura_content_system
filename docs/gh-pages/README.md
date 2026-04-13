# Virtura Node Weaver MCP - GitHub Pages 网站

这是 Virtura Node Weaver MCP 的产品网站，部署在 GitHub Pages 上。

## 📁 网站结构

```
docs/gh-pages/
├── index.html          # 首页
├── quickstart.html     # 快速开始
├── api.html            # API文档
├── examples.html       # 使用示例
├── release.html        # 下载中心
├── css/
│   └── style.css       # 统一样式
├── js/
│   └── main.js         # 公共脚本
└── images/             # 图片资源（预留）
```

## 🚀 部署方法

### 方法一：GitHub Pages 自动部署（推荐）

1. 将项目推送到 GitHub 仓库
2. 进入仓库的 **Settings** 页面
3. 找到 **Pages** 选项
4. 在 **Source** 中选择：
   - **Branch**: `main`（或您的主分支）
   - **Folder**: `/docs/gh-pages`
5. 点击 **Save**
6. 等待几分钟，网站会自动部署完成

访问地址：`https://<your-username>.github.io/virtura_content_system/`

### 方法二：本地预览

在项目根目录运行：

```bash
cd docs/gh-pages
python3 -m http.server 8080
```

然后在浏览器访问：`http://localhost:8080`

### 方法三：使用独立的 gh-pages 分支

```bash
# 创建 gh-pages 分支
git checkout -b gh-pages

# 只保留 docs/gh-pages 内容
cp -r docs/gh-pages/* .
rm -rf docs/

# 提交并推送
git add .
git commit -m "Deploy GitHub Pages"
git push origin gh-pages
```

然后在 GitHub Pages 设置中选择 gh-pages 分支即可。

## 🎨 设计风格

- **配色方案**：深色主题 + 蓝色+青色科技配色
- **视觉风格**：科技感、简洁专业、sharp
- **设计来源**：沿用 viewer 界面设计风格，保持产品一致性
- **响应式**：支持桌面和移动端

## 📝 页面功能说明

### 首页 (index.html)
- 产品介绍和定位
- 三层架构、三类记忆、四大模块核心特性
- 生态里程碑说明
- MCP核心工具介绍
- 安全特性和技术规格

### 快速开始 (quickstart.html)
- 环境要求
- 安装步骤（7步）
- Claude Desktop配置
- 基本使用示例
- 第一个完整流程
- 常见问题解答

### API文档 (api.html)
- 完整的MCP接口参考
- 内容类型说明
- 每个API的参数和返回值
- 使用示例代码
- 错误处理指南

### 使用示例 (examples.html)
- 基础使用（搜索、创建）
- 关联关系建立
- 完整工作流
- 内容组织与导出
- CLI命令行使用
- 高级技巧

### 下载中心 (release.html)
- 最新版本下载
- 历史版本记录
- 更新日志
- 安装说明
- 系统要求
- 常见问题

## 🔧 自定义内容

### 修改版本信息

编辑 `release.html` 中的最新版本信息：

```html
<div class="release-version">
  <h3><span class="badge primary">v1.0.0</span> Virtura Node Weaver MCP</h3>
  <span class="release-date">发布于 2026-04-13</span>
</div>
```

### 更新下载链接

修改 `release.html` 中的下载按钮链接：

```html
<a href="https://github.com/.../v1.0.0.tar.gz" class="btn btn-primary btn-small" download>
  下载源代码 (.tar.gz)
</a>
```

### 添加图片

将图片放入 `images/` 目录，然后在页面中引用：

```html
<img src="images/your-image.png" alt="描述">
```

## 📊 内容来源

所有内容基于项目文档：
- `README.md` - 主项目说明
- `README_MCP.md` - MCP服务说明
- `README_CLI.md` - CLI工具说明
- `docs/COMMANDS_MCP.md` - MCP命令文档

## 🔒 安全提示

- 网站是纯静态HTML/CSS/JS，无后端依赖
- 不收集或发送任何用户数据
- 可以安全地在本地或GitHub Pages运行

## 📄 许可证

MIT License - 与主项目一致

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进网站！

---

**最后更新**: 2026-04-13
