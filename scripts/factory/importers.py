#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Import Scripts
批量导入脚本：支持导入聊天记录(.txt/.md/.json)、Markdown笔记文件夹、图片文件夹、旧nodes.json备份
"""

import json
import re
from typing import Any, Dict, List, Optional
from pathlib import Path
from .utils import load_json, write_json, now_iso, typed_id, is_image_file, is_text_file, scan_directory, ensure_dirs
from .metadata import extract_all_metadata


class BaseImporter:
    """导入器基类"""

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        导入单个文件

        Args:
            file_path: 文件路径

        Returns:
            导入的项目列表
        """
        raise NotImplementedError()

    def import_directory(self, directory: Path, pattern: str = "*") -> List[Dict[str, Any]]:
        """
        导入目录中的所有文件

        Args:
            directory: 目录路径
            pattern: 文件匹配模式

        Returns:
            导入的项目列表
        """
        all_items = []
        for file_path in scan_directory(directory, pattern):
            if file_path.is_file():
                try:
                    items = self.import_file(file_path)
                    all_items.extend(items)
                except Exception as e:
                    print(f"Error importing {file_path}: {e}")

        return all_items


class TextImporter(BaseImporter):
    """
    文本文件导入器：支持 .txt, .md, .markdown 文件
    """

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if not is_text_file(file_path):
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return []

        metadata = extract_all_metadata(content, str(file_path))

        return [{
            "id": typed_id("note", file_path.stem),
            "filename": file_path.name,
            "path": str(file_path),
            "content": content,
            "metadata": metadata,
            "createdAt": now_iso(),
            "importedAt": now_iso(),
            "sourceType": "text",
        }]


class JSONImporter(BaseImporter):
    """
    JSON文件导入器：支持 .json 文件和旧的 nodes.json 备份
    """

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if not str(file_path).endswith('.json'):
            return []

        data = load_json(file_path)
        if not data:
            return []

        items = []

        # 处理旧的nodes.json格式
        if isinstance(data, list):
            for item in data:
                item_id = item.get("id", typed_id("node", item.get("title_guess", "untitled")))
                items.append({
                    "id": item_id,
                    "filename": item.get("filename", ""),
                    "path": item.get("path", str(file_path)),
                    "content": item.get("notes", ""),
                    "metadata": {
                        "title": item.get("title_guess", item.get("filename", "")),
                        "year": item.get("year_guess"),
                        "type": "node",
                        "relatedWorks": item.get("related_work_guess", ""),
                        "relatedNodes": item.get("related_node_guess", ""),
                    },
                    "createdAt": item.get("created_at", now_iso()),
                    "importedAt": now_iso(),
                    "sourceType": "json_nodes",
                })
        elif isinstance(data, dict):
            # 处理其他JSON格式
            if "nodes" in data:
                return self.import_file(file_path)
            else:
                item_id = typed_id("note", file_path.stem)
                items.append({
                    "id": item_id,
                    "filename": file_path.name,
                    "path": str(file_path),
                    "content": str(data),
                    "metadata": extract_all_metadata(str(data), str(file_path)),
                    "createdAt": now_iso(),
                    "importedAt": now_iso(),
                    "sourceType": "json",
                })

        return items


class ImageImporter(BaseImporter):
    """
    图片文件导入器：支持图片文件(.jpg, .jpeg, .png, .gif, .webp等)
    """

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if not is_image_file(file_path):
            return []

        # 对于图片文件，我们创建基础记录
        item_id = typed_id("asset", file_path.stem)
        return [{
            "id": item_id,
            "filename": file_path.name,
            "path": str(file_path),
            "content": "",
            "metadata": {
                "title": file_path.stem,
                "type": "asset",
            },
            "createdAt": now_iso(),
            "importedAt": now_iso(),
            "sourceType": "image",
        }]


class DirectoryImporter(BaseImporter):
    """
    目录导入器：递归导入目录中的所有内容
    """

    def __init__(self, skip_hidden: bool = True):
        self.skip_hidden = skip_hidden
        self.text_importer = TextImporter()
        self.json_importer = JSONImporter()
        self.image_importer = ImageImporter()

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if self.skip_hidden and file_path.name.startswith('.'):
            return []

        if file_path.is_dir():
            return self.import_directory(file_path)

        if is_text_file(file_path):
            return self.text_importer.import_file(file_path)
        elif file_path.suffix.lower() == '.json':
            return self.json_importer.import_file(file_path)
        elif is_image_file(file_path):
            return self.image_importer.import_file(file_path)
        else:
            print(f"Skipping unsupported file type: {file_path}")
            return []

    def import_directory(self, directory: Path, pattern: str = "*") -> List[Dict[str, Any]]:
        items = []
        for file_path in scan_directory(directory, pattern):
            if self.skip_hidden and file_path.name.startswith('.'):
                continue
            items.extend(self.import_file(file_path))
        return items


class ChatHistoryImporter(BaseImporter):
    """
    聊天记录导入器：支持常见的聊天格式
    """

    def import_file(self, file_path: Path) -> List[Dict[str, Any]]:
        if not is_text_file(file_path):
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
            except:
                return []

        # 简单的聊天记录解析（支持常见格式）
        messages = []
        # 匹配时间戳+发送者格式
        time_sender_pattern = re.compile(r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}[:]\d{1,2})[^\n]*?(?:<.*?>|【.*?】|.*?:)', re.MULTILINE)
        matches = list(time_sender_pattern.finditer(content))

        if matches:
            # 按时间戳分割消息
            for i, match in enumerate(matches):
                start = match.end()
                end = matches[i+1].start() if i+1 < len(matches) else len(content)
                message = content[start:end].strip()
                if message:
                    messages.append({
                        "timestamp": match.group(1),
                        "sender": match.group(0).split(':')[0].strip(),
                        "content": message
                    })

        if not messages:
            # 简单分割为段落
            paragraphs = content.split('\n\n')
            messages = [{"content": p} for p in paragraphs if p.strip()]

        # 创建一个合并的聊天记录笔记
        chat_content = '\n'.join([f"• {msg.get('content', '')}" for msg in messages])

        metadata = extract_all_metadata(content, str(file_path))

        return [{
            "id": typed_id("note", file_path.stem),
            "filename": file_path.name,
            "path": str(file_path),
            "content": chat_content,
            "metadata": metadata,
            "createdAt": now_iso(),
            "importedAt": now_iso(),
            "sourceType": "chat",
        }]


def import_from_directory(directory: str, import_type: str = "auto") -> List[Dict[str, Any]]:
    """
    从目录批量导入内容

    Args:
        directory: 目录路径
        import_type: 导入类型 ('auto', 'text', 'json', 'images', 'chat')

    Returns:
        导入的项目列表
    """
    ensure_dirs()

    directory = Path(directory)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if import_type == "auto":
        importer = DirectoryImporter()
    elif import_type == "text":
        importer = TextImporter()
    elif import_type == "json":
        importer = JSONImporter()
    elif import_type == "images":
        importer = ImageImporter()
    elif import_type == "chat":
        importer = ChatHistoryImporter()
    else:
        raise ValueError(f"Unsupported import type: {import_type}")

    return importer.import_directory(directory)
