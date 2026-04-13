#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deduplication Module
自动去重：通过文件哈希、内容指纹检测重复内容
"""

import hashlib
from typing import Any, Dict, List, Optional, Set, Tuple
from pathlib import Path
from .utils import compute_file_hash, compute_content_fingerprint, load_json, write_json, INTAKE_DIR, OBJECTS_DIR


class Deduplicator:
    """重复内容检测和标记器"""

    def __init__(self):
        self.hash_index = {}
        self.fingerprint_index = {}
        self._load_existing_hashes()

    def _load_existing_hashes(self) -> None:
        """加载已存在内容的哈希值索引"""
        # 加载现有的intake记录
        intake_assets = load_json(INTAKE_DIR / "assets.json") or []
        for asset in intake_assets:
            if "fingerprint" in asset:
                self.fingerprint_index[asset["fingerprint"]] = asset["id"]
            if "path" in asset:
                file_hash = compute_file_hash(asset["path"])
                if file_hash:
                    self.hash_index[file_hash] = asset["id"]

        # 加载现有的对象记录
        asset_objects = load_json(OBJECTS_DIR / "assets.json") or []
        for obj in asset_objects:
            for ref in obj.get("sourceRefs", []):
                if ref.get("kind") == "file" and "ref" in ref:
                    file_hash = compute_file_hash(ref["ref"])
                    if file_hash:
                        self.hash_index[file_hash] = obj["id"]

    def check_file_duplicate(self, file_path: Path) -> Optional[str]:
        """
        检查文件是否已经存在（通过哈希）

        Args:
            file_path: 要检查的文件路径

        Returns:
            如果是重复，返回已存在的ID；否则返回None
        """
        file_hash = compute_file_hash(file_path)
        if file_hash and file_hash in self.hash_index:
            return self.hash_index[file_hash]
        return None

    def check_content_duplicate(self, content: str) -> Optional[str]:
        """
        检查内容是否重复（通过内容指纹）

        Args:
            content: 要检查的文本内容

        Returns:
            如果是重复，返回已存在的ID；否则返回None
        """
        fingerprint = compute_content_fingerprint(content)
        if fingerprint and fingerprint in self.fingerprint_index:
            return self.fingerprint_index[fingerprint]
        return None

    def add_to_index(self, item_id: str, content: str = "", file_path: Optional[Path] = None) -> None:
        """
        添加新项目到去重索引

        Args:
            item_id: 项目ID
            content: 文本内容（用于生成指纹）
            file_path: 文件路径（用于生成哈希）
        """
        if content:
            fingerprint = compute_content_fingerprint(content)
            if fingerprint:
                self.fingerprint_index[fingerprint] = item_id
        if file_path and file_path.exists():
            file_hash = compute_file_hash(file_path)
            if file_hash:
                self.hash_index[file_hash] = item_id

    def find_near_duplicates(self, content: str, threshold: float = 0.9) -> List[Dict[str, Any]]:
        """
        查找近似重复的内容（文本相似度）

        Args:
            content: 待比较的文本
            threshold: 相似度阈值 (0.0-1.0)

        Returns:
            近似重复的项目列表
        """
        near_duplicates = []
        content_words = set(content.lower().split())
        min_overlap = threshold * len(content_words)

        # 简单的词重叠检测（用于演示）
        all_assets = []
        intake_assets = load_json(INTAKE_DIR / "assets.json") or []
        asset_objects = load_json(OBJECTS_DIR / "assets.json") or []

        for asset in intake_assets:
            asset_text = str(asset.get("titleGuess", "")) + " " + str(asset.get("notes", ""))
            asset_words = set(asset_text.lower().split())
            overlap = len(content_words & asset_words)
            if overlap >= min_overlap and overlap > 0:
                near_duplicates.append({
                    "id": asset["id"],
                    "type": "intake",
                    "similarity": min(overlap / len(content_words), 1.0)
                })

        for obj in asset_objects:
            obj_text = str(obj.get("title", "")) + " " + str(obj.get("summary", ""))
            obj_words = set(obj_text.lower().split())
            overlap = len(content_words & obj_words)
            if overlap >= min_overlap and overlap > 0:
                near_duplicates.append({
                    "id": obj["id"],
                    "type": "object",
                    "similarity": min(overlap / len(content_words), 1.0)
                })

        return sorted(near_duplicates, key=lambda x: x["similarity"], reverse=True)


def detect_duplicates(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    批量检测重复项

    Args:
        items: 待检测的项目列表

    Returns:
        包含重复信息的项目列表
    """
    deduplicator = Deduplicator()
    results = []

    for item in items:
        result = item.copy()
        result["isDuplicate"] = False
        result["duplicateOf"] = None

        # 检查文件重复
        if "path" in item and item["path"]:
            existing_id = deduplicator.check_file_duplicate(Path(item["path"]))
            if existing_id and existing_id != item.get("id"):
                result["isDuplicate"] = True
                result["duplicateOf"] = existing_id
        # 检查内容重复
        elif "content" in item and item["content"]:
            existing_id = deduplicator.check_content_duplicate(item["content"])
            if existing_id and existing_id != item.get("id"):
                result["isDuplicate"] = True
                result["duplicateOf"] = existing_id

        results.append(result)
        deduplicator.add_to_index(result.get("id", ""), item.get("content", ""),
                                 Path(item["path"]) if "path" in item and item["path"] else None)

    return results


def generate_duplicate_report(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成重复项报告

    Args:
        items: 包含重复信息的项目列表

    Returns:
        重复项报告
    """
    duplicates = [item for item in items if item.get("isDuplicate")]

    return {
        "totalItems": len(items),
        "totalDuplicates": len(duplicates),
        "duplicates": duplicates,
    }
