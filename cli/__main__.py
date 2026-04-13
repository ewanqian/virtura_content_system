#!/usr/bin/env python3
"""
Node Weaver CLI - 主入口脚本
支持create、link、list、show、delete、export等命令
"""

import argparse
import sys
from pathlib import Path

from .utils import (
    PROJECT_ROOT,
    print_error,
    print_info,
    VALID_TYPES,
    VALID_STATUSES
)
from .commands import (
    cmd_create,
    cmd_link,
    cmd_list,
    cmd_show,
    cmd_delete,
    cmd_export
)

def main():
    parser = argparse.ArgumentParser(
        prog="weaver",
        description="Node Weaver CLI - 节点编织器命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  创建对象:
    weaver create --interactive
    weaver create --type work --title "我的新项目" --summary "项目描述"

  链接对象:
    weaver link --object1 work:my-project --object2 node:my-node --relation-type "presented_as"

  列出对象:
    weaver list --type work
    weaver list --tag "art" --status active

  显示详情:
    weaver show --object work:my-project

  删除对象:
    weaver delete --object work:my-project

  导出数据:
    weaver export --all --format json --output ./exports
    weaver export --objects work:my-project node:my-node --format csv --output ./exports

更多帮助信息:
  weaver [命令] --help

项目文档:
  查看 docs/COMMANDS.md 了解完整命令列表
  查看 README_CLI.md 了解详细使用说明
        """
    )

    # 创建子命令解析器
    subparsers = parser.add_subparsers(title="可用命令", dest="command")

    # create 命令
    parser_create = subparsers.add_parser("create", help="创建新对象")
    group_create = parser_create.add_mutually_exclusive_group(required=True)
    group_create.add_argument("-i", "--interactive", action="store_true", help="交互式创建模式")
    group_create.add_argument("-t", "--type", choices=VALID_TYPES, help="对象类型")
    parser_create.add_argument("-T", "--title", help="对象标题 (参数模式时需要)")
    parser_create.add_argument("-S", "--summary", help="对象摘要")
    parser_create.add_argument("-s", "--status", choices=[s for s in VALID_STATUSES if s != "deprecated"],
                             default="draft", help="对象状态 (默认: draft)")
    parser_create.add_argument("-c", "--context", choices=["personal", "collective", "shared", "external"],
                             default="shared", help="主要上下文 (默认: shared)")

    # link 命令
    parser_link = subparsers.add_parser("link", help="链接两个对象")
    parser_link.add_argument("-1", "--object1", required=True, help="第一个对象ID (如 work:my-project)")
    parser_link.add_argument("-2", "--object2", required=True, help="第二个对象ID (如 node:my-node)")
    parser_link.add_argument("-r", "--relation-type", default="related", help="关系类型 (默认: related)")

    # list 命令
    parser_list = subparsers.add_parser("list", help="列出对象")
    parser_list.add_argument("-t", "--type", choices=VALID_TYPES, help="按类型筛选")
    parser_list.add_argument("-g", "--tag", help="按标签筛选")
    parser_list.add_argument("-s", "--status", choices=VALID_STATUSES, help="按状态筛选")
    parser_list.add_argument("-d", "--detail", action="store_true", help="显示详细信息")
    parser_list.add_argument("--sort", choices=["title", "id", "type", "status", "updated"],
                           default="updated", help="排序字段 (默认: updated)")

    # show 命令
    parser_show = subparsers.add_parser("show", help="显示对象详情")
    parser_show.add_argument("-o", "--object", required=True, dest="object_id", help="对象ID")

    # delete 命令
    parser_delete = subparsers.add_parser("delete", help="删除对象 (软删除)")
    parser_delete.add_argument("-o", "--object", required=True, dest="object_id", help="对象ID")

    # export 命令
    parser_export = subparsers.add_parser("export", help="导出对象")
    group_export = parser_export.add_mutually_exclusive_group(required=True)
    group_export.add_argument("-a", "--all", action="store_true", help="导出所有对象")
    group_export.add_argument("-o", "--objects", nargs="+", help="要导出的对象ID列表")
    parser_export.add_argument("-f", "--format", choices=["json", "markdown", "csv"],
                              required=True, help="导出格式")
    parser_export.add_argument("-O", "--output", default="./exports",
                              help="输出目录 (默认: ./exports)")

    # 通用选项
    parser.add_argument("-v", "--version", action="version",
                      version="Node Weaver CLI v1.0.0", help="显示版本信息")
    parser.add_argument("-q", "--quiet", action="store_true", help="安静模式，只显示错误信息")

    args = parser.parse_args()

    # 检查命令是否被提供
    if not args.command:
        parser.print_help()
        return 0

    # 执行命令
    try:
        if args.command == "create":
            return cmd_create(args)
        elif args.command == "link":
            return cmd_link(args)
        elif args.command == "list":
            return cmd_list(args)
        elif args.command == "show":
            return cmd_show(args)
        elif args.command == "delete":
            return cmd_delete(args)
        elif args.command == "export":
            return cmd_export(args)
        else:
            print_error(f"未知命令: {args.command}")
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print("\n操作已取消")
        return 0
    except Exception as e:
        if args.quiet:
            print_error(str(e))
        else:
            import traceback
            print_error(f"执行命令时发生错误: {e}")
            print("\n详细信息:")
            print(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
