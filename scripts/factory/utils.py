#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intake Factory Utilities
投料工厂工具函数：通用辅助函数、路径管理、ID生成等
"""

import os
import re
import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from pathlib import Path


# ============ 路径配置 ============
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
INTAKE_DIR = DATA_DIR / "intake"
OBJECTS_DIR = DATA_DIR / "objects"
INCOMING_DIR = PROJECT_ROOT / "incoming"
FACTORY_DIR = INTAKE_DIR / "factory"
THUMBS_DIR = PROJECT_ROOT / "thumbs"


def ensure_dirs() -> None:
    """确保所有必要的目录存在"""
    for path in [INTAKE_DIR, OBJECTS_DIR, INCOMING_DIR, FACTORY_DIR, THUMBS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    """获取当前ISO格式时间戳"""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    """
    将字符串转换为URL友好的slug格式

    Args:
        value: 输入字符串

    Returns:
        slug格式字符串
    """
    value = (value or "").strip().lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9\u4e00-\u9fa5]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def typed_id(prefix: str, value: str) -> str:
    """
    生成带类型前缀的ID

    Args:
        prefix: 类型前缀 (如 'asset', 'work', 'node')
        value: 用于生成slug的值

    Returns:
        格式化的ID，如 'asset:my-photo-2023'
    """
    return f"{prefix}:{slugify(value)}"


def compute_file_hash(file_path: Union[str, Path], chunk_size: int = 65536) -> str:
    """
    计算文件的SHA-256哈希值

    Args:
        file_path: 文件路径
        chunk_size: 分块读取大小

    Returns:
        十六进制哈希字符串
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return ""

    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def compute_content_fingerprint(content: str) -> str:
    """
    计算文本内容的指纹（用于去重）

    Args:
        content: 文本内容

    Returns:
        内容指纹哈希
    """
    # 标准化内容：移除空白、小写、移除标点
    normalized = re.sub(r'\s+', '', content.lower())
    normalized = re.sub(r'[^\w\u4e00-\u9fa5]', '', normalized)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()


def load_json(file_path: Union[str, Path]) -> Any:
    """
    加载JSON文件

    Args:
        file_path: JSON文件路径

    Returns:
        解析后的JSON数据
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return None
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """
    写入JSON文件

    Args:
        file_path: 目标文件路径
        data: 要写入的数据
        indent: 缩进空格数
    """
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    获取文件扩展名（小写，不带点）

    Args:
        file_path: 文件路径

    Returns:
        扩展名，如 'txt', 'md', 'jpg'
    """
    return Path(file_path).suffix.lower().lstrip('.')


def is_image_file(file_path: Union[str, Path]) -> bool:
    """判断是否为图片文件"""
    ext = get_file_extension(file_path)
    return ext in {'jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp', 'tiff'}


def is_text_file(file_path: Union[str, Path]) -> bool:
    """判断是否为文本文件"""
    ext = get_file_extension(file_path)
    return ext in {'txt', 'md', 'markdown', 'json', 'csv', 'html', 'htm', 'xml'}


def scan_directory(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
    """
    扫描目录下的文件

    Args:
        directory: 目录路径
        pattern: glob匹配模式

    Returns:
        文件路径列表
    """
    directory = Path(directory)
    if not directory.exists():
        return []
    return sorted(directory.rglob(pattern))


def build_content_object(
    obj_id: str,
    obj_type: str,
    title: str,
    **kwargs
) -> Dict[str, Any]:
    """
    构建符合content-object.schema.json规范的对象

    Args:
        obj_id: 对象ID
        obj_type: 对象类型
        title: 标题
        **kwargs: 其他可选字段

    Returns:
        完整的内容对象
    """
    timestamp = now_iso()

    obj = {
        "id": obj_id,
        "type": obj_type,
        "title": title,
        "status": kwargs.get("status", "draft"),
        "timestamps": {
            "createdAt": kwargs.get("createdAt", timestamp),
            "updatedAt": timestamp
        }
    }

    # 添加可选字段
    if "summary" in kwargs:
        obj["summary"] = kwargs["summary"]
    if "primaryContext" in kwargs:
        obj["primaryContext"] = kwargs["primaryContext"]
    if "owners" in kwargs:
        obj["owners"] = kwargs["owners"]
    if "tags" in kwargs:
        obj["tags"] = kwargs["tags"]
    if "sourceRefs" in kwargs:
        obj["sourceRefs"] = kwargs["sourceRefs"]
    if "relations" in kwargs:
        obj["relations"] = kwargs["relations"]
    if "memory" in kwargs:
        obj["memory"] = kwargs["memory"]

    return obj


def extract_year_from_text(text: str) -> Optional[int]:
    """
    从文本中提取年份

    Args:
        text: 输入文本

    Returns:
        提取的年份，或None
    """
    # 匹配 1900-2099 范围内的年份
    match = re.search(r'\b(19|20)\d{2}\b', text)
    if match:
        return int(match.group(0))
    return None
