// Virtura Node Weaver MCP 网站主脚本

document.addEventListener('DOMContentLoaded', function() {
  // 初始化导航栏
  initNavbar();
  // 初始化代码复制按钮
  initCodeCopy();
  // 高亮当前页导航
  highlightActiveNav();
});

// 导航栏功能
function initNavbar() {
  const toggle = document.querySelector('.navbar-toggle');
  const nav = document.querySelector('.navbar-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('active');
    });
  }

  // 点击链接后关闭移动端菜单
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      if (nav) {
        nav.classList.remove('active');
      }
    });
  });

  // 点击页面其他位置关闭菜单
  document.addEventListener('click', function(e) {
    const navbar = document.querySelector('.navbar');
    if (nav && navbar && !navbar.contains(e.target)) {
      nav.classList.remove('active');
    }
  });
}

// 代码块复制功能
function initCodeCopy() {
  const codeBlocks = document.querySelectorAll('.code-block');

  codeBlocks.forEach(block => {
    // 检查是否已有复制按钮
    if (block.querySelector('.code-copy')) return;

    // 创建复制按钮
    const header = document.createElement('div');
    header.className = 'code-header';

    // 检测代码语言
    const lang = detectCodeLanguage(block);
    if (lang) {
      const langSpan = document.createElement('span');
      langSpan.className = 'code-lang';
      langSpan.textContent = lang;
      header.appendChild(langSpan);
    }

    const copyBtn = document.createElement('button');
    copyBtn.className = 'code-copy';
    copyBtn.textContent = '复制';

    // 占位空间
    const spacer = document.createElement('div');
    spacer.style.cssText = 'display: flex; align-items: center; gap: 8px;';
    spacer.appendChild(copyBtn);

    if (!lang) {
      header.style.cssText = 'justify-content: flex-end;';
    }
    header.appendChild(spacer);

    // 插入到code-block的开头
    block.insertBefore(header, block.firstChild);

    // 复制事件
    copyBtn.addEventListener('click', function() {
      const code = block.querySelector('pre');
      if (code) {
        copyToClipboard(code.textContent).then(() => {
          copyBtn.textContent = '已复制!';
          copyBtn.classList.add('copied');
          setTimeout(() => {
            copyBtn.textContent = '复制';
            copyBtn.classList.remove('copied');
          }, 2000);
        }).catch(err => {
          console.error('复制失败:', err);
          copyBtn.textContent = '复制失败';
          setTimeout(() => {
            copyBtn.textContent = '复制';
          }, 2000);
        });
      }
    });
  });
}

// 检测代码语言
function detectCodeLanguage(block) {
  const code = block.querySelector('code');
  if (code) {
    const classList = code.className;
    if (classList.includes('language-')) {
      return classList.match(/language-(\w+)/)?.[1];
    }
  }

  const text = block.textContent;
  if (text.includes('{') && text.includes('}') && (text.includes('"') || text.includes("'"))) {
    if (text.includes('import') || text.includes('export') || text.includes('const') || text.includes('function')) {
      return 'javascript';
    }
    if (text.includes('json')) return 'json';
  }
  if (text.includes('#') && !text.includes('#!/') && text.includes('\n#')) return 'bash';
  if (text.includes('pip install') || text.includes('python')) return 'bash';
  if (text.includes('npm install') || text.includes('node')) return 'bash';

  return null;
}

// 复制到剪贴板
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (err) {
    // 降级方案
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand('copy');
      return true;
    } finally {
      document.body.removeChild(textarea);
    }
  }
}

// 高亮当前页面的导航链接
function highlightActiveNav() {
  const currentPath = window.location.pathname;
  const currentFile = currentPath.split('/').pop() || 'index.html';

  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentFile) {
      link.classList.add('active');
    } else if (currentFile === '' && href === 'index.html') {
      link.classList.add('active');
    }
  });
}

// 平滑滚动到锚点
function scrollToAnchor(anchorId) {
  const element = document.getElementById(anchorId);
  if (element) {
    const navHeight = document.querySelector('.navbar')?.offsetHeight || 80;
    const elementTop = element.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
    window.scrollTo({
      top: elementTop,
      behavior: 'smooth'
    });
  }
}

// 页面内锚点链接处理
document.addEventListener('click', function(e) {
  const target = e.target.closest('a[href^="#"]');
  if (target) {
    const href = target.getAttribute('href');
    if (href.length > 1) {
      e.preventDefault();
      const anchorId = href.substring(1);
      scrollToAnchor(anchorId);
      history.pushState(null, null, href);
    }
  }
});
