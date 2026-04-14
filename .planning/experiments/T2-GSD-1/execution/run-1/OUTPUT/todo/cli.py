"""
命令行接口模块
"""
import argparse
import sys
from typing import List, Optional

from .task import TaskManager, Task, Priority
from .storage import StorageManager


def print_task(task: Task) -> None:
    """打印单个任务"""
    status = "✓" if task.completed else "○"
    priority_str = {
        Priority.LOW: "低",
        Priority.MEDIUM: "中",
        Priority.HIGH: "高"
    }[task.priority]
    print(f"{status} #{task.id:3d} [{priority_str}] {task.description}")


def print_tasks(tasks: List[Task]) -> None:
    """打印任务列表"""
    if not tasks:
        print("暂无任务")
        return

    for task in tasks:
        print_task(task)


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="命令行待办事项管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s add "完成项目报告" high       # 添加高优先级任务
  %(prog)s list --sort priority            # 按优先级列出任务
  %(prog)s complete 1                      # 标记ID为1的任务完成
  %(prog)s delete 2                        # 删除ID为2的任务
        """
    )

    subparsers = parser.add_subparsers(title="命令", dest="command", required=True)

    # add 命令
    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("description", help="任务描述")
    add_parser.add_argument(
        "priority", nargs="?", default="medium",
        choices=["low", "medium", "high"],
        help="优先级 (low/medium/high, 默认: medium)"
    )

    # delete 命令
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务ID")

    # complete 命令
    complete_parser = subparsers.add_parser("complete", help="标记任务完成")
    complete_parser.add_argument("id", type=int, help="任务ID")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有任务")
    list_parser.add_argument(
        "--sort", choices=["priority"],
        help="排序方式 (priority: 按优先级)"
    )

    return parser


def run() -> None:
    """运行CLI应用"""
    parser = create_parser()
    args = parser.parse_args()

    # 初始化存储和管理器
    storage = StorageManager("tasks.json")
    manager = TaskManager(storage)

    if args.command == "add":
        priority_map = {
            "low": Priority.LOW,
            "medium": Priority.MEDIUM,
            "high": Priority.HIGH
        }
        try:
            task = manager.add_task(args.description, priority_map[args.priority])
            print(f"已添加任务: #{task.id} {task.description}")
        except ValueError as e:
            print(f"错误: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        if manager.delete_task(args.id):
            print(f"已删除任务 #{args.id}")
        else:
            print(f"错误: 未找到任务 #{args.id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "complete":
        task = manager.complete_task(args.id)
        if task:
            print(f"已标记任务完成: #{task.id} {task.description}")
        else:
            print(f"错误: 未找到任务 #{args.id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "list":
        sort_by_priority = args.sort == "priority"
        tasks = manager.list_tasks(sort_by_priority=sort_by_priority)
        print_tasks(tasks)
