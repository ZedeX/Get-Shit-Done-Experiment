#!/usr/bin/env python3
"""
命令行待办事项管理工具 - GSD模式 (第二次重复)
完整模块化版本 - 为简洁起见合并展示
"""
import json
import os
import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    id: int
    description: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if isinstance(self.priority, int):
            self.priority = Priority(self.priority)
        elif isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]


class StorageManager:
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task(**task_data) for task_data in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        from dataclasses import asdict
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        task_dicts = [asdict(task) for task in tasks]
        temp_path = f"{self.file_path}.tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(task_dicts, f, ensure_ascii=False, indent=2, default=str)
            os.replace(temp_path, self.file_path)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise


class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.tasks: List[Task] = self.storage.load_tasks()
        self._next_id = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        if not description or not description.strip():
            raise ValueError("任务描述不能为空")
        task = Task(id=self._next_id, description=description.strip(), priority=priority)
        self.tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def delete_task(self, task_id: int) -> bool:
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < initial_length:
            self._save()
            return True
        return False

    def complete_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save()
                return task
        return None

    def list_tasks(self, sort_by_priority: bool = False) -> List[Task]:
        tasks = list(self.tasks)
        if sort_by_priority:
            tasks.sort(key=lambda t: (-t.priority, t.created_at))
        return tasks

    def _save(self) -> None:
        self.storage.save_tasks(self.tasks)


def print_task(task: Task) -> None:
    status = "✓" if task.completed else "○"
    priority_str = {Priority.LOW: "低", Priority.MEDIUM: "中", Priority.HIGH: "高"}[task.priority]
    print(f"{status} #{task.id:3d} [{priority_str}] {task.description}")


def print_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("暂无任务")
        return
    for task in tasks:
        print_task(task)


def main():
    parser = argparse.ArgumentParser(
        description="命令行待办事项管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s add "完成项目报告" high
  %(prog)s list --sort priority
  %(prog)s complete 1
  %(prog)s delete 2
        """
    )
    subparsers = parser.add_subparsers(title="命令", dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="添加新任务")
    add_parser.add_argument("description", help="任务描述")
    add_parser.add_argument("priority", nargs="?", default="medium",
                          choices=["low", "medium", "high"], help="优先级")

    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("id", type=int, help="任务ID")

    complete_parser = subparsers.add_parser("complete", help="标记任务完成")
    complete_parser.add_argument("id", type=int, help="任务ID")

    list_parser = subparsers.add_parser("list", help="列出所有任务")
    list_parser.add_argument("--sort", choices=["priority"], help="排序方式")

    args = parser.parse_args()
    storage = StorageManager("tasks.json")
    manager = TaskManager(storage)

    if args.command == "add":
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
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
        tasks = manager.list_tasks(sort_by_priority=args.sort == "priority")
        print_tasks(tasks)


if __name__ == "__main__":
    main()
