#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic Metadata Extraction
自动元数据提取：内置规则提取标题、年份、类型、标签、相关作品/节点字段
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from .utils import extract_year_from_text, slugify


# ============ 内容类型检测规则 ============
TYPE_KEYWORDS = {
    'note': ['笔记', 'note', 'notes', '备忘录', 'todo', 'draft', '草稿'],
    'writing': ['文章', 'essay', 'paper', 'article', 'blog', '博客', '论文', '写作'],
    'work': ['作品', 'work', 'project', '项目', 'artwork', '艺术作品', '创作'],
    'event': ['活动', 'event', '展览', 'exhibition', '展', '演出', 'performance', '会议', 'conference'],
    'node': ['节点', 'node', 'presentation', '展示', '公开'],
    'spec': ['规格', 'spec', 'specification', '设计', 'design', '方案', 'proposal'],
}

# 标签提取关键词
TAG_CANDIDATES = {
    'art': ['艺术', 'art', 'artwork', '当代艺术', 'contemporary'],
    'tech': ['技术', 'tech', 'technology', '科技', '代码', 'code'],
    'media': ['媒体', 'media', '新媒体', 'new media', '交互', 'interactive'],
    'performance': ['表演', 'performance', '演出', '剧场', 'theater'],
    'exhibition': ['展览', 'exhibition', '展', 'gallery', '画廊', 'museum', '美术馆'],
    'research': ['研究', 'research', '调研', 'study', '分析', 'analysis'],
    'documentation': ['记录', 'documentation', '文档', 'archive', '档案'],
    'personal': ['个人', 'personal', 'private', '私人'],
    'collaboration': ['合作', 'collaboration', '集体', 'collective', '团队'],
}

# 常见作品/项目名称（用于关联检测）
KNOWN_WORKS = [
    'Drop Flow', 'drop flow', '滴流',
    'Timer', 'timer', '计时器',
    'Kashiwa Titan', 'kashiwa titan', '柏 Titan',
    'Garden Memory', 'garden memory', '花园记忆',
    'Babel Bottle', 'babel bottle', '巴别塔瓶',
    'New Media Artist Simulator', '新媒体艺术家模拟器',
    'The Floating Life', 'the floating life', '浮生',
    'UFO Terminal', 'ufo terminal', 'UFO终端',
    'Loading Access', 'loading access', '加载访问',
    'Observation and Symbiosis', '观察与共生',
]

KNOWN_NODES = [
    'Hangzhou Opening', 'hangzhou opening', '杭州开幕',
    'Shanghai Broadcast', 'shanghai broadcast', '上海广播',
    'Shenzhen Live', 'shenzhen live', '深圳现场',
    'Westbound Art Fair', 'westbound art fair', '西岸艺术博览会',
    'Hangzhou Art Tech Biennale', '杭州艺术科技双年展',
    'Can Festival', 'can festival', '罐头艺术节',
    'VRPlay Hackathon', 'vrplay hackathon',
]


def extract_title(content: str, filename: Optional[str] = None) -> Tuple[str, float]:
    """
    从内容中提取标题

    Args:
        content: 文本内容
        filename: 文件名（可选）

    Returns:
        (标题, 置信度)
    """
    # 策略1：查找Markdown一级标题
    md_h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if md_h1_match:
        title = md_h1_match.group(1).strip()
        if len(title) > 3 and len(title) < 200:
            return title, 0.9

    # 策略2：查找前几行的粗体标题
    bold_match = re.search(r'^\*\*(.+?)\*\*', content, re.MULTILINE)
    if bold_match:
        title = bold_match.group(1).strip()
        if len(title) > 3 and len(title) < 200:
            return title, 0.7

    # 策略3：使用文件名（不含扩展名）
    if filename:
        from pathlib import Path
        name = Path(filename).stem
        # 清理常见的前缀后缀
        name = re.sub(r'^[\d\s\-_]+', '', name)
        name = re.sub(r'[\d\s\-_]+$', '', name)
        if len(name) > 2:
            # 将驼峰或下划线分隔转换为可读格式
            name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
            name = re.sub(r'[_-]', ' ', name)
            return name.strip(), 0.5

    # 策略4：使用第一段的前50个字符
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if lines:
        first_line = lines[0][:100].strip()
        if len(first_line) > 5:
            return first_line, 0.3

    return "Untitled", 0.1


def extract_content_type(content: str, filename: Optional[str] = None) -> Tuple[str, float]:
    """
    推断内容类型

    Args:
        content: 文本内容
        filename: 文件名

    Returns:
        (类型, 置信度)
    """
    content_lower = content.lower()
    filename_lower = (filename or "").lower()

    scores = {}

    # 基于关键词打分
    for obj_type, keywords in TYPE_KEYWORDS.items():
        score = 0.0
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 0.15
            if filename and keyword.lower() in filename_lower:
                score += 0.1
        scores[obj_type] = score

    # 基于内容结构推断
    if re.search(r'^#\s', content, re.MULTILINE) or re.search(r'\*\*.+?\*\*', content):
        scores['note'] += 0.2
        scores['writing'] += 0.15

    # 查找时间+活动的模式
    if re.search(r'\b(19|20)\d{2}\b.*(展|活动|event|exhibition)', content_lower):
        scores['event'] += 0.3
        scores['node'] += 0.2

    # 返回最高分
    if scores:
        best_type = max(scores.keys(), key=lambda k: scores[k])
        best_score = min(scores[best_type], 1.0)
        if best_score > 0.1:
            return best_type, best_score

    return 'note', 0.1


def extract_tags(content: str, max_tags: int = 10) -> List[Tuple[str, float]]:
    """
    提取标签

    Args:
        content: 文本内容
        max_tags: 最大标签数

    Returns:
        [(标签, 置信度)] 列表
    """
    content_lower = content.lower()
    tags = []

    # 基于预定义关键词提取
    for tag, keywords in TAG_CANDIDATES.items():
        score = 0.0
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 0.2
        if score > 0:
            tags.append((tag, min(score, 1.0)))

    # 提取 hashtag 样式的标签
    hashtag_matches = re.findall(r'#(\w+)', content)
    for match in hashtag_matches:
        tags.append((match.lower(), 0.8))

    # 提取方括号中的标签
    bracket_matches = re.findall(r'\[([^\]]+)\]', content)
    for match in bracket_matches:
        if len(match) < 30 and not re.search(r'\s', match):
            tags.append((match.lower(), 0.6))

    # 去重并按分数排序
    seen = set()
    unique_tags = []
    for tag, score in sorted(tags, key=lambda x: -x[1]):
        if tag not in seen:
            seen.add(tag)
            unique_tags.append((tag, score))
            if len(unique_tags) >= max_tags:
                break

    return unique_tags


def extract_related_works(content: str) -> List[Tuple[str, float]]:
    """
    提取相关作品

    Args:
        content: 文本内容

    Returns:
        [(作品名称, 置信度)] 列表
    """
    content_lower = content.lower()
    matches = []

    for work in KNOWN_WORKS:
        if work.lower() in content_lower:
            # 使用规范化的名称
            normalized = work
            # 查找最佳匹配
            for candidate in KNOWN_WORKS:
                if work.lower() == candidate.lower():
                    normalized = candidate
                    break
            matches.append((normalized, 0.8))

    # 查找 "作品: xxx" 或 "project: xxx" 模式
    project_matches = re.findall(r'(?:作品|project|work)\s*[：:]\s*([^\n\r,]+)', content, re.IGNORECASE)
    for match in project_matches:
        matches.append((match.strip(), 0.7))

    return matches


def extract_related_nodes(content: str) -> List[Tuple[str, float]]:
    """
    提取相关节点

    Args:
        content: 文本内容

    Returns:
        [(节点名称, 置信度)] 列表
    """
    content_lower = content.lower()
    matches = []

    for node in KNOWN_NODES:
        if node.lower() in content_lower:
            normalized = node
            for candidate in KNOWN_NODES:
                if node.lower() == candidate.lower():
                    normalized = candidate
                    break
            matches.append((normalized, 0.8))

    # 查找 "节点: xxx" 或 "node: xxx" 模式
    node_matches = re.findall(r'(?:节点|node|event|展览)\s*[：:]\s*([^\n\r,]+)', content, re.IGNORECASE)
    for match in node_matches:
        matches.append((match.strip(), 0.7))

    return matches


def extract_all_metadata(content: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    提取所有元数据

    Args:
        content: 文本内容
        filename: 文件名

    Returns:
        包含所有提取的元数据的字典
    """
    title, title_conf = extract_title(content, filename)
    year = extract_year_from_text(content)
    content_type, type_conf = extract_content_type(content, filename)
    tags = extract_tags(content)
    related_works = extract_related_works(content)
    related_nodes = extract_related_nodes(content)

    return {
        "title": title,
        "titleConfidence": title_conf,
        "year": year,
        "type": content_type,
        "typeConfidence": type_conf,
        "tags": [{"tag": t, "confidence": c} for t, c in tags],
        "relatedWorks": [{"name": n, "confidence": c} for n, c in related_works],
        "relatedNodes": [{"name": n, "confidence": c} for n, c in related_nodes],
    }
