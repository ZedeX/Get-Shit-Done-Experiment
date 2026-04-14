"""
任务模型和业务逻辑
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import IntEnum


class Priority(IntEnum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    """任务数据模型"""
    id: int
    description: str
    priority: Priority = Priority.MEDIUM
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        # 确保priority是枚举类型
        if isinstance(self.priority, int):
            self.priority = Priority(self.priority)
        elif isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]


class TaskManager:
    """任务管理核心业务逻辑"""

    def __init__(self, storage):
        self.storage = storage
        self.tasks: List[Task] = self.storage.load_tasks()
        self._next_id = self._calculate_next_id()

    def _calculate_next_id(self) -> int:
        """计算下一个可用的任务ID"""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, description: str, priority: Priority = Priority.MEDIUM) -> Task:
        """添加新任务"""
        if not description or not description.strip():
            raise ValueError("任务描述不能为空")

        task = Task(
            id=self._next_id,
            description=description.strip(),
            priority=priority
        )
        self.tasks.append(task)
        self._next_id += 1
        self._save()
        return task

    def delete_task(self, task_id: int) -> bool:
        """删除任务，返回是否成功"""
        initial_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < initial_length:
            self._save()
            return True
        return False

    def complete_task(self, task_id: int) -> Optional[Task]:
        """标记任务完成，返回更新后的任务"""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save()
                return task
        return None

    def list_tasks(self, sort_by_priority: bool = False) -> List[Task]:
        """列出所有任务，可选择按优先级排序"""
        tasks = list(self.tasks)
        if sort_by_priority:
            # 按优先级降序（高优先级在前），然后按创建时间升序
            tasks.sort(key=lambda t: (-t.priority, t.created_at))
        return tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def _save(self) -> None:
        """保存任务到存储"""
        self.storage.save_tasks(self.tasks)
