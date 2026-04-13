#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Review List Generation
待审核清单生成：输出到data/intake/review_needed.json，包含AI提取结果和修改建议
"""

import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from .utils import write_json, now_iso, INTAKE_DIR, OBJECTS_DIR, load_json, typed_id


REVIEW_FILE = INTAKE_DIR / "review_needed.json"


class ReviewItem:
    """表示一个待审核的项目"""

    def __init__(self, item_id: str, source_type: str = "unknown"):
        self.item_id = item_id
        self.sourceType = source_type
        self.aiSuggestions: List[Dict[str, Any]] = []
        self.issues: List[str] = []
        self.status = "pending"  # pending | approved | rejected | modified
        self.notes: List[str] = []

    def add_suggestion(self, field: str, value: Any, confidence: float = 0.0, reason: str = ""):
        """
        添加AI建议

        Args:
            field: 字段名
            value: 建议值
            confidence: 置信度 (0-1)
            reason: 建议理由
        """
        self.aiSuggestions.append({
            "field": field,
            "value": value,
            "confidence": confidence,
            "reason": reason
        })

    def add_issue(self, issue_type: str, description: str, severity: str = "medium"):
        """
        添加问题描述

        Args:
            issue_type: 问题类型
            description: 问题描述
            severity: 严重程度 (low | medium | high)
        """
        self.issues.append({
            "type": issue_type,
            "description": description,
            "severity": severity
        })

    def add_note(self, note: str):
        """添加备注"""
        self.notes.append(note)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.item_id,
            "sourceType": self.sourceType,
            "aiSuggestions": self.aiSuggestions,
            "issues": self.issues,
            "status": self.status,
            "notes": self.notes
        }


class ReviewList:
    """待审核清单管理"""

    def __init__(self):
        self.items: Dict[str, ReviewItem] = {}

    def add_item(self, item: ReviewItem):
        """添加待审核项目"""
        self.items[item.item_id] = item

    def get_item(self, item_id: str) -> Optional[ReviewItem]:
        """获取项目"""
        return self.items.get(item_id)

    def mark_approved(self, item_id: str):
        """标记为已批准"""
        if item_id in self.items:
            self.items[item_id].status = "approved"

    def mark_rejected(self, item_id: str):
        """标记为已拒绝"""
        if item_id in self.items:
            self.items[item_id].status = "rejected"

    def mark_modified(self, item_id: str):
        """标记为已修改"""
        if item_id in self.items:
            self.items[item_id].status = "modified"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "generatedAt": now_iso(),
            "totalItems": len(self.items),
            "pendingItems": len([i for i in self.items.values() if i.status == "pending"]),
            "approvedItems": len([i for i in self.items.values() if i.status == "approved"]),
            "rejectedItems": len([i for i in self.items.values() if i.status == "rejected"]),
            "modifiedItems": len([i for i in self.items.values() if i.status == "modified"]),
            "items": [item.to_dict() for item in self.items.values()],
        }


def generate_review_list(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成待审核清单

    Args:
        items: 已导入项目列表

    Returns:
        待审核清单（JSON结构）
    """
    review_list = ReviewList()

    for item in items:
        review_item = ReviewItem(item.get("id", ""), item.get("sourceType", "unknown"))

        # 检查元数据质量
        metadata = item.get("metadata", {})

        if "title" in metadata and (not metadata["title"] or len(metadata["title"]) < 3):
            review_item.add_issue("missing_title", "标题过短或缺失", "high")

        if "titleConfidence" in metadata and metadata["titleConfidence"] < 0.5:
            review_item.add_suggestion(
                "title",
                metadata["title"],
                metadata["titleConfidence"],
                "标题置信度较低"
            )

        if "typeConfidence" in metadata and metadata["typeConfidence"] < 0.5:
            review_item.add_suggestion(
                "type",
                metadata["type"],
                metadata["typeConfidence"],
                "类型置信度较低"
            )

        # 检查年份信息
        if "year" in metadata and metadata["year"]:
            if metadata["year"] < 1900 or metadata["year"] > 2100:
                review_item.add_issue("invalid_year", f"年份 {metadata['year']} 无效", "medium")

        # 检查标签数量
        if "tags" in metadata and len(metadata["tags"]) == 0:
            review_item.add_suggestion("tags", [], 0.1, "未检测到标签，建议手动添加")

        # 检查关联关系
        if "relatedWorks" in metadata and len(metadata["relatedWorks"]) == 0:
            review_item.add_suggestion("relatedWorks", [], 0.1, "未检测到相关作品，建议手动添加")

        if "relatedNodes" in metadata and len(metadata["relatedNodes"]) == 0:
            review_item.add_suggestion("relatedNodes", [], 0.1, "未检测到相关节点，建议手动添加")

        # 检查内容长度
        if item.get("content") and len(item.get("content")) < 20:
            review_item.add_issue("short_content", "内容过短", "low")

        # 检查重复项
        if item.get("isDuplicate"):
            review_item.add_issue("duplicate", f"重复内容，已存在于: {item.get('duplicateOf')}", "high")

        review_list.add_item(review_item)

    return review_list.to_dict()


def save_review_list(data: Dict[str, Any]) -> None:
    """保存待审核清单到文件"""
    write_json(REVIEW_FILE, data)
    print(f"Review list saved to: {REVIEW_FILE}")


def load_review_list() -> Dict[str, Any]:
    """加载待审核清单"""
    return load_json(REVIEW_FILE) or {
        "generatedAt": now_iso(),
        "totalItems": 0,
        "pendingItems": 0,
        "approvedItems": 0,
        "rejectedItems": 0,
        "modifiedItems": 0,
        "items": []
    }


def update_review_status(item_id: str, status: str = "pending", notes: Optional[str] = None) -> bool:
    """
    更新项目审核状态

    Args:
        item_id: 项目ID
        status: 新状态 (pending | approved | rejected | modified)
        notes: 备注

    Returns:
        是否成功
    """
    review_list = load_review_list()
    for item in review_list["items"]:
        if item["id"] == item_id:
            item["status"] = status
            if notes:
                if "notes" not in item:
                    item["notes"] = []
                item["notes"].append(notes)
            save_review_list(review_list)
            return True
    return False


def process_to_objects(review_list: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    将已审核的项目转换为规范对象

    Args:
        review_list: 待审核清单

    Returns:
        转换后的规范对象列表
    """
    processed_objects = []

    for item in review_list["items"]:
        if item["status"] in ["approved", "modified"]:
            processed_objects.append(_convert_to_canonical(item))

    return processed_objects


def _convert_to_canonical(item: Dict[str, Any]) -> Dict[str, Any]:
    """转换为规范格式的对象"""
    base_obj = {
        "id": item["id"],
        "type": "note",  # 默认类型
        "title": "Untitled",
        "status": "draft",
        "timestamps": {
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
        }
    }

    # 应用AI建议
    for suggestion in item.get("aiSuggestions", []):
        field = suggestion["field"]
        value = suggestion["value"]

        if field == "title":
            base_obj["title"] = value
        elif field == "type":
            base_obj["type"] = value
        elif field == "tags":
            base_obj["tags"] = [t.get("tag") for t in value if "tag" in t]
        elif field == "year":
            if "memory" not in base_obj:
                base_obj["memory"] = {}
            if "semantic" not in base_obj["memory"]:
                base_obj["memory"]["semantic"] = []
            base_obj["memory"]["semantic"].append(str(value))
        elif field in ["relatedWorks", "relatedNodes"]:
            if "relations" not in base_obj:
                base_obj["relations"] = []
            for rel in value:
                name = rel.get("name", "")
                if name:
                    rel_type = "work" if field == "relatedWorks" else "node"
                    base_obj["relations"].append({
                        "type": "related",
                        "target": typed_id(rel_type, name)
                    })

    return base_obj
