#!/usr/bin/env python3
"""
Node Weaver CLI - 命令实现模块
包含create、link、list、show、delete、export等命令的实现
"""

import os
import json
import csv
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from .utils import (
    load_all_objects,
    load_schema,
    validate_object,
    save_objects_by_type,
    find_object_by_id,
    find_objects_by_type,
    create_basic_object,
    format_print,
    print_success,
    print_error,
    print_info,
    print_warning,
    confirm_action,
    VALID_TYPES,
    VALID_STATUSES,
    PROJECT_ROOT,
    OBJECTS_DIR,
    DATA_DIR
)

def cmd_create(args):
    """创建新对象命令"""
    # 交互式创建模式
    if args.interactive:
        print("🚀 交互式创建模式")
        print("=" * 60)

        # 获取对象类型
        while True:
            print("\n请选择对象类型:")
            for i, obj_type in enumerate(VALID_TYPES, 1):
                print(f"{i:2d}. {obj_type}")

            try:
                choice = int(input(f"\n请输入类型编号 (1-{len(VALID_TYPES)}): "))
                if 1 <= choice <= len(VALID_TYPES):
                    obj_type = VALID_TYPES[choice - 1]
                    break
                else:
                    print_error("请输入有效的编号")
            except ValueError:
                print_error("请输入数字")

        # 获取标题
        title = input("\n请输入对象标题: ").strip()
        while not title:
            title = input("标题不能为空，请重新输入: ").strip()

        # 获取摘要 (可选)
        summary = input("\n请输入对象摘要 (可选): ").strip()

        # 获取状态
        while True:
            print("\n请选择对象状态:")
            status_list = [s for s in VALID_STATUSES if s != "deprecated"]  # 不允许直接创建已删除的对象
            for i, status in enumerate(status_list, 1):
                print(f"{i:2d}. {status}")

            try:
                choice = int(input(f"\n请输入状态编号 (1-{len(status_list)}): "))
                if 1 <= choice <= len(status_list):
                    status = status_list[choice - 1]
                    break
                else:
                    print_error("请输入有效的编号")
            except ValueError:
                print_error("请输入数字")

        # 获取主要上下文 (可选)
        context_list = ["personal", "collective", "shared", "external"]
        print("\n请选择主要上下文 (可选，默认: shared):")
        for i, context in enumerate(context_list, 1):
            print(f"{i:2d}. {context}")

        try:
            choice = input(f"请输入上下文编号 (1-{len(context_list)}，回车默认): ").strip()
            if choice:
                choice = int(choice)
                if 1 <= choice <= len(context_list):
                    primary_context = context_list[choice - 1]
                else:
                    print_warning("无效的编号，将使用默认值 shared")
                    primary_context = "shared"
            else:
                primary_context = "shared"
        except ValueError:
            print_warning("无效的输入，将使用默认值 shared")
            primary_context = "shared"

        # 确认创建
        print("\n" + "=" * 60)
        print("创建对象信息:")
        print(f"  类型: {obj_type}")
        print(f"  标题: {title}")
        if summary:
            print(f"  摘要: {summary}")
        print(f"  状态: {status}")
        print(f"  上下文: {primary_context}")

        if not confirm_action("\n确认创建此对象"):
            print_info("操作已取消")
            return

    else:
        # 参数模式
        obj_type = args.type
        title = args.title
        summary = args.summary
        status = args.status
        primary_context = args.context

    # 创建对象
    try:
        new_obj = create_basic_object(obj_type, title, summary, status, primary_context)

        # 验证对象
        schema = load_schema()
        valid, msg = validate_object(new_obj, schema)
        if not valid:
            print_error(f"对象验证失败: {msg}")
            return

        # 保存对象
        all_objects = load_all_objects()

        # 检查ID是否已存在
        if any(obj["id"] == new_obj["id"] for obj in all_objects):
            print_error(f"对象ID '{new_obj['id']}' 已存在")
            return

        all_objects.append(new_obj)
        save_objects_by_type(all_objects)

        print_success(f"对象创建成功! ID: {new_obj['id']}")
        print(f"\n详细信息:\n{format_print(new_obj)}")

    except Exception as e:
        print_error(f"创建对象失败: {e}")
        return 1

    return 0

def cmd_link(args):
    """链接两个对象命令"""
    obj1_id = args.object1
    obj2_id = args.object2
    relation_type = args.relation_type

    obj1 = find_object_by_id(obj1_id)
    obj2 = find_object_by_id(obj2_id)

    if not obj1:
        print_error(f"找不到对象: {obj1_id}")
        return 1

    if not obj2:
        print_error(f"找不到对象: {obj2_id}")
        return 1

    print_info(f"链接: {obj1['title']} ({obj1['id']}) → {obj2['title']} ({obj2['id']})")
    print_info(f"关系类型: {relation_type}")

    if not confirm_action("确认建立双向关联"):
        print_info("操作已取消")
        return 0

    # 添加关系到 obj1
    obj1_relation = {"type": relation_type, "target": obj2_id}
    if obj1_relation not in obj1.get("relations", []):
        obj1["relations"].append(obj1_relation)
        obj1["timestamps"]["updatedAt"] = datetime.now().isoformat()

    # 添加关系到 obj2
    obj2_relation = {"type": relation_type, "target": obj1_id}
    if obj2_relation not in obj2.get("relations", []):
        obj2["relations"].append(obj2_relation)
        obj2["timestamps"]["updatedAt"] = datetime.now().isoformat()

    # 保存对象
    all_objects = load_all_objects()
    for i, obj in enumerate(all_objects):
        if obj["id"] == obj1_id:
            all_objects[i] = obj1
        elif obj["id"] == obj2_id:
            all_objects[i] = obj2

    save_objects_by_type(all_objects)

    print_success("双向关联建立成功!")
    return 0

def cmd_list(args):
    """列出对象命令"""
    all_objects = load_all_objects()

    # 应用过滤器
    filtered_objects = all_objects

    if args.type:
        filtered_objects = [obj for obj in filtered_objects if obj.get("type") == args.type]

    if args.tag:
        filtered_objects = [obj for obj in filtered_objects if args.tag in obj.get("tags", [])]

    if args.status:
        filtered_objects = [obj for obj in filtered_objects if obj.get("status") == args.status]

    # 排序
    if args.sort:
        if args.sort == "title":
            filtered_objects.sort(key=lambda x: x.get("title", ""))
        elif args.sort == "id":
            filtered_objects.sort(key=lambda x: x.get("id", ""))
        elif args.sort == "type":
            filtered_objects.sort(key=lambda x: x.get("type", ""))
        elif args.sort == "status":
            filtered_objects.sort(key=lambda x: x.get("status", ""))
        elif args.sort == "updated":
            filtered_objects.sort(key=lambda x: x.get("timestamps", {}).get("updatedAt", ""), reverse=True)

    # 打印结果
    if not filtered_objects:
        print_info("没有找到符合条件的对象")
        return 0

    print(f"🔍 找到 {len(filtered_objects)} 个对象:")
    print("=" * 80)

    if args.detail:
        for obj in filtered_objects:
            print(f"\n📌 {obj['id']}")
            print(f"   类型: {obj['type']}")
            print(f"   标题: {obj['title']}")
            if "summary" in obj and obj["summary"]:
                print(f"   摘要: {obj['summary']}")
            print(f"   状态: {obj['status']}")
            if "tags" in obj and obj["tags"]:
                print(f"   标签: {', '.join(obj['tags'])}")
            if "timestamps" in obj:
                updated = obj['timestamps'].get('updatedAt', 'N/A')
                print(f"   更新: {updated}")
    else:
        for obj in filtered_objects:
            print(f"📌 {obj['id']} - {obj['title']} ({obj['type']}, {obj['status']})")

    return 0

def cmd_show(args):
    """显示对象详情命令"""
    obj_id = args.object_id

    obj = find_object_by_id(obj_id)

    if not obj:
        print_error(f"找不到对象: {obj_id}")
        return 1

    print("📋 对象详情")
    print("=" * 80)
    print(format_print(obj))

    # 显示关联关系
    if "relations" in obj and obj["relations"]:
        print("\n🔗 关联关系:")
        print("-" * 80)
        for relation in obj["relations"]:
            target = find_object_by_id(relation["target"])
            if target:
                print(f"   {relation['type']}: {target['id']} - {target['title']}")
            else:
                print(f"   {relation['type']}: {relation['target']} (目标对象未找到)")

    return 0

def cmd_delete(args):
    """删除对象命令 (软删除)"""
    obj_id = args.object_id

    obj = find_object_by_id(obj_id)

    if not obj:
        print_error(f"找不到对象: {obj_id}")
        return 1

    print_info(f"要删除的对象: {obj['title']} ({obj['id']})")
    print_info(f"当前状态: {obj['status']}")

    if obj['status'] == 'deprecated':
        print_warning("该对象已被删除")
        return 0

    if not confirm_action("确认删除此对象 (软删除，将标记为 deprecated)"):
        print_info("操作已取消")
        return 0

    # 标记为 deprecated
    obj['status'] = 'deprecated'
    obj['timestamps']['updatedAt'] = datetime.now().isoformat()

    # 保存对象
    all_objects = load_all_objects()
    for i, o in enumerate(all_objects):
        if o["id"] == obj_id:
            all_objects[i] = obj
            break

    save_objects_by_type(all_objects)

    print_success(f"对象已成功删除 (软删除)。ID: {obj_id}")
    return 0

def cmd_export(args):
    """导出对象命令"""
    # 获取要导出的对象
    if args.all:
        objects = load_all_objects()
    else:
        objects = []
        for obj_id in args.objects:
            obj = find_object_by_id(obj_id)
            if obj:
                objects.append(obj)
            else:
                print_error(f"找不到对象: {obj_id}")
                return 1

    if not objects:
        print_error("没有对象可导出")
        return 1

    # 创建输出目录
    output_dir = Path(args.output)
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # 导出格式
    format_type = args.format

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        if format_type == "json":
            filename = f"export_{timestamp}.json"
            output_path = output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(objects, f, ensure_ascii=False, indent=2)
            print_success(f"JSON导出成功: {output_path}")

        elif format_type == "markdown":
            filename = f"export_{timestamp}.md"
            output_path = output_dir / filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("# Node Library 导出数据\n\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"对象数量: {len(objects)}\n\n")

                for obj in objects:
                    f.write(f"## {obj['id']}\n")
                    f.write(f"**类型**: {obj['type']}\n")
                    f.write(f"**标题**: {obj['title']}\n")
                    if "summary" in obj and obj["summary"]:
                        f.write(f"**摘要**: {obj['summary']}\n")
                    f.write(f"**状态**: {obj['status']}\n")
                    if "tags" in obj and obj["tags"]:
                        f.write(f"**标签**: {', '.join(obj['tags'])}\n")
                    if "relations" in obj and obj["relations"]:
                        f.write(f"**关联**: {len(obj['relations'])}\n")
                    f.write("\n")

            print_success(f"Markdown导出成功: {output_path}")

        elif format_type == "csv":
            filename = f"export_{timestamp}.csv"
            output_path = output_dir / filename
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # 写入标题行
                headers = [
                    "id", "type", "title", "summary", "status", "primaryContext",
                    "owners", "tags", "sourceRefs", "relations", "memory", "createdAt", "updatedAt"
                ]
                writer.writerow(headers)

                for obj in objects:
                    row = [
                        obj["id"],
                        obj["type"],
                        obj["title"],
                        obj.get("summary", ""),
                        obj["status"],
                        obj.get("primaryContext", ""),
                        json.dumps(obj.get("owners", [])),
                        json.dumps(obj.get("tags", [])),
                        json.dumps(obj.get("sourceRefs", [])),
                        json.dumps(obj.get("relations", [])),
                        json.dumps(obj.get("memory", {})),
                        obj["timestamps"].get("createdAt", ""),
                        obj["timestamps"].get("updatedAt", "")
                    ]
                    writer.writerow(row)

            print_success(f"CSV导出成功: {output_path}")

        else:
            print_error(f"不支持的导出格式: {format_type}")
            return 1

    except Exception as e:
        print_error(f"导出失败: {e}")
        return 1

    return 0
