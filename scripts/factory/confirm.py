#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Review Confirmation Script
审核确认脚本：支持通过自然语言指令批量修改确认，确认后输出到canonical对象层
"""

import re
import json
from typing import Any, Dict, List, Optional
from pathlib import Path
from .utils import load_json, write_json, now_iso, typed_id, build_content_object, INTAKE_DIR, OBJECTS_DIR
from .review import load_review_list, save_review_list


REVIEW_FILE = INTAKE_DIR / "review_needed.json"


def parse_instruction(instruction: str) -> List[Dict[str, Any]]:
    """
    解析自然语言指令，生成操作列表

    Args:
        instruction: 自然语言指令

    Returns:
        操作列表
    """
    operations = []

    # 批准所有项目
    if re.search(r'(批准|approve|通过|确认)\s*(所有|全部|all)', instruction, re.IGNORECASE):
        operations.append({"action": "approve_all"})

    # 批准特定项目
    if re.search(r'(批准|approve|通过|确认)', instruction, re.IGNORECASE):
        # 提取ID或编号
        id_matches = re.findall(r'[#@]?([\w-]+(?::[\w-]+)?)', instruction)
        for match in id_matches:
            if any(kw in instruction for kw in ["批准", "approve", "通过", "确认"]):
                operations.append({"action": "approve", "item_id": match})

        # 提取编号（如 "批准1、2、3"）
        number_matches = re.findall(r'(?:批准|通过|确认|approve)\s*(\d+(?:[、，,]\s*\d+)*)', instruction)
        for match in number_matches:
            numbers = re.split(r'[、，,]', match)
            for num in numbers:
                if num.strip():
                    operations.append({"action": "approve_index", "index": int(num.strip()) - 1})

    # 拒绝操作
    if re.search(r'(拒绝|reject|删除|删除掉|不批准)', instruction, re.IGNORECASE):
        id_matches = re.findall(r'[#@]?([\w-]+(?::[\w-]+)?)', instruction)
        for match in id_matches:
            if any(kw in instruction for kw in ["拒绝", "reject", "删除", "不批准"]):
                operations.append({"action": "reject", "item_id": match})

        number_matches = re.findall(r'(?:拒绝|删除|reject)\s*(\d+(?:[、，,]\s*\d+)*)', instruction)
        for match in number_matches:
            numbers = re.split(r'[、，,]', match)
            for num in numbers:
                if num.strip():
                    operations.append({"action": "reject_index", "index": int(num.strip()) - 1})

    # 修改操作
    if re.search(r'(修改|编辑|edit|change)', instruction, re.IGNORECASE):
        # 提取字段修改
        field_pattern = r'(标题|title|类型|type|标签|tags|年份|year|summary|摘要)'
        field_matches = re.findall(field_pattern + r'\s*[为是改为:]\s*["\']?([^"\',\s]+)', instruction)
        for field, value in field_matches:
            field_map = {
                "标题": "title", "title": "title",
                "类型": "type", "type": "type",
                "标签": "tags", "tags": "tags",
                "年份": "year", "year": "year",
                "摘要": "summary", "summary": "summary"
            }
            operations.append({
                "action": "modify",
                "field": field_map.get(field, field),
                "value": value
            })

    # 添加备注
    if re.search(r'(备注|note|注释)', instruction, re.IGNORECASE):
        note_match = re.search(r'(?:备注|note|注释)\s*[：:]\s*(.*)', instruction)
        if note_match:
            operations.append({"action": "add_note", "note": note_match.group(1).strip()})

    if not operations:
        operations.append({"action": "help"})

    return operations


def apply_operations(review_list: Dict[str, Any], operations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    应用操作到待审核清单

    Args:
        review_list: 待审核清单
        operations: 操作列表

    Returns:
        更新后的待审核清单
    """
    updated_list = review_list.copy()

    for op in operations:
        action = op.get("action")

        if action == "approve_all":
            for item in updated_list["items"]:
                item["status"] = "approved"

        elif action == "approve":
            item_id = op.get("item_id")
            for item in updated_list["items"]:
                if item["id"] == item_id or item["id"].endswith(item_id):
                    item["status"] = "approved"

        elif action == "approve_index":
            idx = op.get("index", 0)
            if 0 <= idx < len(updated_list["items"]):
                updated_list["items"][idx]["status"] = "approved"

        elif action == "reject":
            item_id = op.get("item_id")
            for item in updated_list["items"]:
                if item["id"] == item_id or item["id"].endswith(item_id):
                    item["status"] = "rejected"

        elif action == "reject_index":
            idx = op.get("index", 0)
            if 0 <= idx < len(updated_list["items"]):
                updated_list["items"][idx]["status"] = "rejected"

        elif action == "modify":
            field = op.get("field")
            value = op.get("value")
            for item in updated_list["items"]:
                if item["status"] in ["pending", "modified"]:
                    item["status"] = "modified"
                    item[f"modified_{field}"] = value

        elif action == "add_note":
            note = op.get("note")
            for item in updated_list["items"]:
                if item["status"] == "pending":
                    if "notes" not in item:
                        item["notes"] = []
                    item["notes"].append(note)

    return updated_list


def convert_to_canonical_objects(review_list: Dict[str, Any], source_items: Optional[List[Dict]] = None) -> List[Dict]:
    """
    将已审核的项目转换为规范对象并输出到objects层

    Args:
        review_list: 待审核清单
        source_items: 源导入项目列表（用于获取原始数据）

    Returns:
        转换后的规范对象列表
    """
    canonical_objects = []

    for idx, item in enumerate(review_list["items"]):
        if item["status"] in ["approved", "modified"]:
            # 尝试从源项目获取数据
            source_data = {}
            if source_items and idx < len(source_items):
                source_data = source_items[idx]

            # 构建基础对象
            obj = build_content_object(
                item["id"],
                _determine_type(item, source_data),
                _determine_title(item, source_data),
                summary=_determine_summary(item, source_data),
                status="draft",
                primaryContext="personal",
                tags=_determine_tags(item, source_data),
                sourceRefs=_determine_source_refs(item, source_data),
                relations=_determine_relations(item, source_data)
            )

            canonical_objects.append(obj)

    return canonical_objects


def _determine_type(item: Dict, source_data: Dict) -> str:
    if "modified_type" in item:
        return item["modified_type"]
    metadata = source_data.get("metadata", {})
    return metadata.get("type", "note")


def _determine_title(item: Dict, source_data: Dict) -> str:
    if "modified_title" in item:
        return item["modified_title"]
    metadata = source_data.get("metadata", {})
    return metadata.get("title", "Untitled")


def _determine_summary(item: Dict, source_data: Dict) -> str:
    if "modified_summary" in item:
        return item["modified_summary"]
    content = source_data.get("content", "")
    if content:
        return content[:200] + "..." if len(content) > 200 else content
    return ""


def _determine_tags(item: Dict, source_data: Dict) -> List[str]:
    if "modified_tags" in item:
        return [t.strip() for t in item["modified_tags"].split(",")]
    metadata = source_data.get("metadata", {})
    tags = metadata.get("tags", [])
    return [t.get("tag", "") for t in tags if isinstance(t, dict) and "tag" in t]


def _determine_source_refs(item: Dict, source_data: Dict) -> List[Dict]:
    refs = []
    if "path" in source_data:
        refs.append({"kind": "file", "ref": source_data["path"]})
    if "filename" in source_data:
        refs.append({"kind": "filename", "ref": source_data["filename"]})
    return refs


def _determine_relations(item: Dict, source_data: Dict) -> List[Dict]:
    relations = []
    metadata = source_data.get("metadata", {})

    for work in metadata.get("relatedWorks", []):
        name = work.get("name", "") if isinstance(work, dict) else work
        if name:
            relations.append({"type": "related", "target": typed_id("work", name)})

    for node in metadata.get("relatedNodes", []):
        name = node.get("name", "") if isinstance(node, dict) else node
        if name:
            relations.append({"type": "related", "target": typed_id("node", name)})

    return relations


def save_canonical_objects(objects: List[Dict], category: str = "nodes") -> None:
    """
    保存规范对象到objects目录

    Args:
        objects: 对象列表
        category: 对象类别 ('nodes', 'works', 'assets', 'notes')
    """
    target_file = OBJECTS_DIR / f"{category}.json"
    existing_objects = load_json(target_file) or []

    # 合并对象（按ID去重）
    existing_by_id = {obj["id"]: obj for obj in existing_objects}
    for obj in objects:
        existing_by_id[obj["id"]] = obj

    write_json(target_file, list(existing_by_id.values()))
    print(f"Saved {len(objects)} canonical objects to {target_file}")


def process_review_instruction(instruction: str, source_items: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """
    处理审核指令的主函数

    Args:
        instruction: 自然语言审核指令
        source_items: 源导入项目列表

    Returns:
        处理结果报告
    """
    review_list = load_review_list()

    operations = parse_instruction(instruction)

    if any(op.get("action") == "help" for op in operations):
        return {
            "success": False,
            "message": "可用指令示例：\n"
                      "- '批准所有'\n"
                      "- '批准 item:xxx'\n"
                      "- '拒绝 1 2 3'\n"
                      "- '修改标题为新标题'\n"
                      "- '备注：需要进一步检查'"
        }

    review_list = apply_operations(review_list, operations)
    save_review_list(review_list)

    canonical_objects = convert_to_canonical_objects(review_list, source_items)

    if canonical_objects:
        # 按类型分组保存
        type_groups: Dict[str, List[Dict]] = {}
        for obj in canonical_objects:
            obj_type = obj.get("type", "node")
            if obj_type not in type_groups:
                type_groups[obj_type] = []
            type_groups[obj_type].append(obj)

        # 保存到对应的文件
        for obj_type, objs in type_groups.items():
            category_map = {
                "work": "works",
                "asset": "assets",
                "note": "nodes",  # 笔记作为node保存
                "node": "nodes",
            }
            category = category_map.get(obj_type, "nodes")
            save_canonical_objects(objs, category)

    return {
        "success": True,
        "processedItems": len(review_list["items"]),
        "approvedItems": len([i for i in review_list["items"] if i["status"] == "approved"]),
        "rejectedItems": len([i for i in review_list["items"] if i["status"] == "rejected"]),
        "modifiedItems": len([i for i in review_list["items"] if i["status"] == "modified"]),
        "canonicalObjects": len(canonical_objects),
    }


def list_pending_items() -> List[Dict]:
    """列出所有待审核的项目"""
    review_list = load_review_list()
    return [item for item in review_list["items"] if item["status"] == "pending"]
