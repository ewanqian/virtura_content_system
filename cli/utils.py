#!/usr/bin/env python3
"""
Node Weaver CLI - 通用工具函数模块
包含JSON文件读写、schema验证、ID生成等功能
"""

import os
import json
import re
from datetime import datetime
import jsonschema
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
OBJECTS_DIR = DATA_DIR / "objects"

# 模式文件路径
SCHEMA_FILE = PROJECT_ROOT / "schemas" / "content-object.schema.json"

# 支持的对象类型和状态
VALID_TYPES = [
    "asset",
    "work",
    "node",
    "event",
    "venue",
    "note",
    "person",
    "collective",
    "writing",
    "spec",
    "relation",
    "concept",
    "method"
]

VALID_STATUSES = [
    "draft",
    "active",
    "archived",
    "deprecated"  # 用于软删除
]

def load_schema():
    """加载JSON模式文件"""
    try:
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载模式文件失败: {e}")
        return None

def validate_object(obj, schema=None):
    """验证对象是否符合模式"""
    if schema is None:
        schema = load_schema()
        if schema is None:
            return False, "无法加载模式文件"

    try:
        jsonschema.validate(obj, schema)
        return True, "对象验证成功"
    except jsonschema.exceptions.ValidationError as e:
        return False, f"验证失败: {e.message}"

def generate_slug(text):
    """将文本转换为slug格式 (小写，空格替换为-，移除特殊字符)"""
    # 转换为小写
    slug = text.lower()
    # 替换空格和制表符为连字符
    slug = re.sub(r'\s+', '-', slug)
    # 移除特殊字符，只保留字母、数字、连字符和下划线
    slug = re.sub(r'[^a-z0-9\-_]', '', slug)
    # 移除首尾的连字符
    slug = slug.strip('-')
    return slug

def generate_typed_id(obj_type, title):
    """生成类型化ID，格式：type:slug"""
    if obj_type not in VALID_TYPES:
        raise ValueError(f"无效的对象类型: {obj_type}")

    slug = generate_slug(title)
    return f"{obj_type}:{slug}"

def load_all_objects():
    """加载所有对象数据"""
    all_objects = []

    try:
        for filename in ["assets.json", "works.json", "nodes.json", "relations.json"]:
            file_path = OBJECTS_DIR / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_objects.extend(data)
    except Exception as e:
        print(f"❌ 加载对象数据失败: {e}")
        return []

    return all_objects

def save_objects_by_type(objects):
    """按类型保存对象到对应的JSON文件"""
    # 按类型分组对象
    objects_by_type = {obj_type: [] for obj_type in VALID_TYPES}

    for obj in objects:
        obj_type = obj.get("type")
        if obj_type in objects_by_type:
            objects_by_type[obj_type].append(obj)

    # 确定每个类型对应的文件名
    type_to_filename = {
        "asset": "assets.json",
        "work": "works.json",
        "node": "nodes.json",
        "relation": "relations.json"
    }

    # 保存到文件
    for obj_type, filename in type_to_filename.items():
        file_path = OBJECTS_DIR / filename
        try:
            # 读取现有数据
            existing_objects = []
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_objects = json.load(f)

            # 创建ID到对象的映射
            existing_ids = {obj["id"] for obj in existing_objects}
            updated_objects = []

            for obj in existing_objects:
                if obj["id"] not in [o["id"] for o in objects_by_type[obj_type]]:
                    updated_objects.append(obj)

            # 添加或更新对象
            for obj in objects_by_type[obj_type]:
                if obj["id"] in existing_ids:
                    # 更新现有对象
                    for i, existing_obj in enumerate(updated_objects):
                        if existing_obj["id"] == obj["id"]:
                            updated_objects[i] = obj
                            break
                else:
                    # 添加新对象
                    updated_objects.append(obj)

            # 保存到文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(updated_objects, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"❌ 保存 {obj_type} 对象到 {filename} 失败: {e}")

def find_object_by_id(object_id):
    """通过ID查找对象"""
    all_objects = load_all_objects()
    for obj in all_objects:
        if obj["id"] == object_id:
            return obj
    return None

def find_objects_by_type(obj_type):
    """通过类型查找对象"""
    all_objects = load_all_objects()
    return [obj for obj in all_objects if obj.get("type") == obj_type]

def create_timestamp():
    """创建当前时间戳 (ISO 8601 格式)"""
    return datetime.now().isoformat()

def create_basic_object(obj_type, title, summary=None, status="draft", primary_context="shared"):
    """创建基础对象结构"""
    if obj_type not in VALID_TYPES:
        raise ValueError(f"无效的对象类型: {obj_type}")

    object_id = generate_typed_id(obj_type, title)
    timestamp = create_timestamp()

    obj = {
        "id": object_id,
        "type": obj_type,
        "title": title,
        "summary": summary or "",
        "status": status,
        "primaryContext": primary_context,
        "owners": [],
        "tags": [],
        "sourceRefs": [],
        "relations": [],
        "memory": {
            "semantic": [],
            "episodic": [],
            "procedural": []
        },
        "timestamps": {
            "createdAt": timestamp,
            "updatedAt": timestamp
        }
    }

    return obj

def format_print(obj, indent=2):
    """格式化打印对象信息"""
    return json.dumps(obj, ensure_ascii=False, indent=indent)

def print_success(msg):
    """打印成功消息"""
    print(f"✅ {msg}")

def print_error(msg):
    """打印错误消息"""
    print(f"❌ {msg}")

def print_info(msg):
    """打印信息消息"""
    print(f"ℹ️  {msg}")

def print_warning(msg):
    """打印警告消息"""
    print(f"⚠️  {msg}")

def confirm_action(prompt):
    """获取用户确认"""
    while True:
        response = input(f"{prompt} (y/N): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no", ""]:
            return False
        else:
            print("请输入 y 或 N")

def slugify(text):
    """将文本转换为slug格式 (小写，空格替换为-，移除特殊字符)"""
    return generate_slug(text)
