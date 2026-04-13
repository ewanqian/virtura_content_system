#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relation Detection and Suggestion
关联检测：自动匹配已有节点，给出关联建议
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from .utils import load_json, typed_id, OBJECTS_DIR
from .metadata import KNOWN_WORKS, KNOWN_NODES


class RelationDetector:
    """关联检测器：分析内容与现有对象的关联关系"""

    def __init__(self):
        self.works = []
        self.nodes = []
        self.other_objects = []
        self._load_objects()

    def _load_objects(self) -> None:
        """加载所有已存在的对象用于关联检测"""
        # 加载作品 (works)
        works = load_json(OBJECTS_DIR / "works.json") or []
        for work in works:
            self.works.append({
                "id": work["id"],
                "title": work["title"],
                "titleLower": work["title"].lower(),
                "type": "work"
            })

        # 加载节点 (nodes)
        nodes = load_json(OBJECTS_DIR / "nodes.json") or []
        for node in nodes:
            self.nodes.append({
                "id": node["id"],
                "title": node["title"],
                "titleLower": node["title"].lower(),
                "type": "node"
            })

        # 加载其他类型对象
        assets = load_json(OBJECTS_DIR / "assets.json") or []
        for asset in assets:
            self.other_objects.append({
                "id": asset["id"],
                "title": asset.get("title", ""),
                "titleLower": asset.get("title", "").lower(),
                "type": "asset"
            })

    def _find_matches(self, content: str, candidates: List[Dict]) -> List[Tuple[str, float]]:
        """
        在内容中查找与候选对象的匹配

        Args:
            content: 待匹配的内容
            candidates: 候选对象列表

        Returns:
            [(对象ID, 匹配分数)] 列表
        """
        content_lower = content.lower()
        matches = []

        for candidate in candidates:
            score = 0.0

            # 完全匹配
            if candidate["titleLower"] in content_lower:
                score += 0.8

            # 部分匹配（关键词匹配）
            for term in candidate["title"].split():
                if len(term) > 3 and term.lower() in content_lower:
                    score += 0.1

            if score > 0.2:
                matches.append((candidate["id"], min(score, 1.0)))

        return sorted(matches, key=lambda x: x[1], reverse=True)

    def detect_work_relations(self, content: str) -> List[Dict[str, Any]]:
        """
        检测与作品的关联关系

        Args:
            content: 文本内容

        Returns:
            关联建议列表
        """
        matches = self._find_matches(content, self.works)
        # 也检查已知作品名称
        for work_name in KNOWN_WORKS:
            if work_name.lower() in content.lower():
                work_id = typed_id("work", work_name)
                # 检查是否已在匹配结果中
                found = any(match[0] == work_id for match in matches)
                if not found:
                    matches.append((work_id, 0.7))

        return [{"targetId": target_id, "confidence": float(conf)} for target_id, conf in matches]

    def detect_node_relations(self, content: str) -> List[Dict[str, Any]]:
        """
        检测与节点的关联关系

        Args:
            content: 文本内容

        Returns:
            关联建议列表
        """
        matches = self._find_matches(content, self.nodes)
        # 检查已知节点名称
        for node_name in KNOWN_NODES:
            if node_name.lower() in content.lower():
                node_id = typed_id("node", node_name)
                found = any(match[0] == node_id for match in matches)
                if not found:
                    matches.append((node_id, 0.7))

        return [{"targetId": target_id, "confidence": float(conf)} for target_id, conf in matches]

    def detect_other_relations(self, content: str) -> List[Dict[str, Any]]:
        """
        检测与其他对象的关联关系

        Args:
            content: 文本内容

        Returns:
            关联建议列表
        """
        matches = self._find_matches(content, self.other_objects)
        return [{"targetId": target_id, "confidence": float(conf)} for target_id, conf in matches]

    def detect_all_relations(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        检测所有类型的关联关系

        Args:
            content: 文本内容

        Returns:
            按类型分类的关联建议
        """
        return {
            "works": self.detect_work_relations(content),
            "nodes": self.detect_node_relations(content),
            "other": self.detect_other_relations(content)
        }


def suggest_relations(content: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    静态方法：检测内容的关联关系

    Args:
        content: 文本内容

    Returns:
        关联建议
    """
    detector = RelationDetector()
    return detector.detect_all_relations(content)


def generate_relation_report(content: str) -> Dict[str, Any]:
    """
    生成关联关系报告

    Args:
        content: 文本内容

    Returns:
        关联关系报告
    """
    detector = RelationDetector()

    work_relations = detector.detect_work_relations(content)
    node_relations = detector.detect_node_relations(content)
    other_relations = detector.detect_other_relations(content)

    return {
        "totalRelations": len(work_relations) + len(node_relations) + len(other_relations),
        "works": work_relations,
        "nodes": node_relations,
        "other": other_relations,
    }
