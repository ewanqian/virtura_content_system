#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Virtura Content System - Factory Ingest Script
投料工厂主脚本：批量导入、元数据提取、去重、关联检测、生成待审核清单

使用方法:
    python3 scripts/factory_ingest.py import --dir incoming/test
    python3 scripts/factory_ingest.py import --type chat --dir incoming/chat_logs
    python3 scripts/factory_ingest.py review --list
    python3 scripts/factory_ingest.py review --confirm "批准所有"
"""

import argparse
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from factory.utils import ensure_dirs, write_json, INTAKE_DIR, FACTORY_DIR
from factory.importers import import_from_directory
from factory.metadata import extract_all_metadata
from factory.deduplication import Deduplicator, detect_duplicates, generate_duplicate_report
from factory.relation_detector import RelationDetector
from factory.review import generate_review_list, save_review_list, load_review_list
from factory.confirm import process_review_instruction, list_pending_items


def command_import(args):
    """导入命令处理"""
    ensure_dirs()

    print(f"Importing from: {args.dir}")
    print(f"Import type: {args.type}")

    # 导入内容
    items = import_from_directory(args.dir, args.type)
    print(f"Imported {len(items)} items")

    # 提取元数据
    print("Extracting metadata...")
    for item in items:
        if "content" in item and "metadata" in item:
            continue  # 已经有元数据
        content = item.get("content", "")
        filename = item.get("filename")
        item["metadata"] = extract_all_metadata(content, filename)

    # 去重检测
    print("Detecting duplicates...")
    items_with_duplicates = detect_duplicates(items)
    duplicate_report = generate_duplicate_report(items_with_duplicates)
    print(f"Found {duplicate_report['totalDuplicates']} duplicates")

    # 关联检测
    print("Detecting relations...")
    relation_detector = RelationDetector()
    for item in items_with_duplicates:
        content = item.get("content", "")
        item["detectedRelations"] = relation_detector.detect_all_relations(content)

    # 保存导入的原始数据
    import_file = FACTORY_DIR / "latest_import.json"
    write_json(import_file, items_with_duplicates)
    print(f"Import data saved to: {import_file}")

    # 保存重复项报告
    duplicate_file = FACTORY_DIR / "duplicate_report.json"
    write_json(duplicate_file, duplicate_report)
    print(f"Duplicate report saved to: {duplicate_file}")

    # 生成待审核清单
    print("Generating review list...")
    review_list = generate_review_list(items_with_duplicates)
    save_review_list(review_list)

    print("\n" + "="*50)
    print(f"Import complete!")
    print(f"Total items: {review_list['totalItems']}")
    print(f"Pending review: {review_list['pendingItems']}")
    print(f"\nRun 'python3 scripts/factory_ingest.py review --list' to view pending items")
    print(f"Run 'python3 scripts/factory_ingest.py review --confirm \"批准所有\"' to approve all")

    return items_with_duplicates


def command_review(args):
    """审核命令处理"""
    if args.list:
        # 列出待审核项目
        pending = list_pending_items()
        review_list = load_review_list()

        print("="*50)
        print(f"REVIEW LIST - Total: {review_list['totalItems']}")
        print(f"  Pending: {review_list['pendingItems']}")
        print(f"  Approved: {review_list['approvedItems']}")
        print(f"  Rejected: {review_list['rejectedItems']}")
        print(f"  Modified: {review_list['modifiedItems']}")
        print("="*50)

        if not pending:
            print("No pending items!")
            return

        for idx, item in enumerate(pending, 1):
            print(f"\n{idx}. {item['id']}")
            print(f"   Source: {item.get('sourceType', 'unknown')}")

            issues = item.get('issues', [])
            if issues:
                print(f"   Issues: {len(issues)}")
                for issue in issues[:3]:
                    print(f"     - [{issue.get('severity')}] {issue.get('description')}")

            suggestions = item.get('aiSuggestions', [])
            if suggestions:
                print(f"   AI Suggestions: {len(suggestions)}")
                for sugg in suggestions[:3]:
                    field = sugg.get('field')
                    value = sugg.get('value')
                    conf = sugg.get('confidence', 0)
                    print(f"     - {field}: {value} (conf: {conf:.2f})")

    elif args.confirm:
        # 处理确认指令
        print(f"Processing instruction: {args.confirm}")

        # 尝试加载源项目
        source_items = None
        import_file = FACTORY_DIR / "latest_import.json"
        if import_file.exists():
            from factory.utils import load_json
            source_items = load_json(import_file)

        result = process_review_instruction(args.confirm, source_items)

        if result.get("success"):
            print("\n" + "="*50)
            print("Review processed successfully!")
            print(f"  Processed items: {result.get('processedItems')}")
            print(f"  Approved: {result.get('approvedItems')}")
            print(f"  Rejected: {result.get('rejectedItems')}")
            print(f"  Modified: {result.get('modifiedItems')}")
            print(f"  Canonical objects created: {result.get('canonicalObjects')}")
        else:
            print(f"\n{result.get('message')}")

    elif args.show:
        # 显示单个项目详细信息
        review_list = load_review_list()
        for item in review_list["items"]:
            if item["id"] == args.show or item["id"].endswith(args.show):
                print("="*50)
                print(f"ID: {item['id']}")
                print(f"Status: {item['status']}")
                print(f"Source: {item.get('sourceType', 'unknown')}")
                print("="*50)

                issues = item.get('issues', [])
                if issues:
                    print(f"\nIssues ({len(issues)}):")
                    for issue in issues:
                        print(f"  - [{issue.get('severity')}] {issue.get('description')}")

                suggestions = item.get('aiSuggestions', [])
                if suggestions:
                    print(f"\nAI Suggestions ({len(suggestions)}):")
                    for sugg in suggestions:
                        print(f"  - {sugg.get('field')}: {sugg.get('value')}")
                        print(f"    Confidence: {sugg.get('confidence', 0):.2f}")
                        if sugg.get('reason'):
                            print(f"    Reason: {sugg.get('reason')}")

                notes = item.get('notes', [])
                if notes:
                    print(f"\nNotes:")
                    for note in notes:
                        print(f"  - {note}")
                break
        else:
            print(f"Item not found: {args.show}")


def main():
    parser = argparse.ArgumentParser(
        description="Virtura Content System - Intake Factory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 导入目录
  python3 scripts/factory_ingest.py import --dir incoming/test

  # 导入聊天记录
  python3 scripts/factory_ingest.py import --type chat --dir incoming/chats

  # 导入图片文件夹
  python3 scripts/factory_ingest.py import --type images --dir incoming/photos

  # 列出待审核项目
  python3 scripts/factory_ingest.py review --list

  # 显示项目详情
  python3 scripts/factory_ingest.py review --show note:my-note

  # 批准所有项目
  python3 scripts/factory_ingest.py review --confirm "批准所有"

  # 批准特定项目
  python3 scripts/factory_ingest.py review --confirm "批准 note:my-note"

  # 批准编号1、2、3
  python3 scripts/factory_ingest.py review --confirm "批准 1 2 3"

  # 拒绝特定项目
  python3 scripts/factory_ingest.py review --confirm "拒绝 note:bad-note"
        """
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import content from directory")
    import_parser.add_argument("--dir", required=True, help="Directory to import from")
    import_parser.add_argument("--type", default="auto",
                              choices=["auto", "text", "json", "images", "chat"],
                              help="Import type (default: auto)")

    # Review command
    review_parser = subparsers.add_parser("review", help="Review and confirm imported items")
    review_group = review_parser.add_mutually_exclusive_group(required=True)
    review_group.add_argument("--list", action="store_true", help="List pending items")
    review_group.add_argument("--show", metavar="ID", help="Show details of specific item")
    review_group.add_argument("--confirm", metavar="INSTRUCTION", help="Process review instruction")

    args = parser.parse_args()

    if args.command == "import":
        command_import(args)
    elif args.command == "review":
        command_review(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
