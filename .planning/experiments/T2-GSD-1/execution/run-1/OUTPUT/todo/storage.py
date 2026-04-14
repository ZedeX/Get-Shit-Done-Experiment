"""
JSON存储管理器 - 负责任务数据的持久化
"""
import json
import os
from dataclasses import asdict
from typing import List

from .task import Task


class StorageManager:
    """管理任务数据的JSON存储"""

    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        """从JSON文件加载任务列表"""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Task(**task_data) for task_data in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            # 文件损坏或格式错误，返回空列表
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """将任务列表保存到JSON文件"""
        # 确保目录存在
        dir_path = os.path.dirname(self.file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        # 转换为可序列化的字典列表
        task_dicts = [asdict(task) for task in tasks]

        # 写入文件（原子操作）
        temp_path = f"{self.file_path}.tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(task_dicts, f, ensure_ascii=False, indent=2, default=str)
            # 原子替换
            os.replace(temp_path, self.file_path)
        except Exception:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
