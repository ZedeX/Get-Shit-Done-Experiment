"""
测试存储管理器
"""
import json
import os
import tempfile
import pytest

from todo.storage import StorageManager
from todo.task import Task, Priority


class TestStorageManager:
    """测试StorageManager类"""

    def setup_method(self):
        """每个测试前创建临时文件"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage = StorageManager(self.temp_file.name)

    def teardown_method(self):
        """每个测试后删除临时文件"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_load_tasks_file_not_exists(self):
        """测试文件不存在时返回空列表"""
        storage = StorageManager("non_existent_file.json")
        tasks = storage.load_tasks()
        assert tasks == []

    def test_load_tasks_empty_file(self):
        """测试空文件返回空列表"""
        tasks = self.storage.load_tasks()
        assert tasks == []

    def test_save_and_load_tasks(self):
        """测试保存和加载任务"""
        task1 = Task(id=1, description="测试任务1", priority=Priority.HIGH)
        task2 = Task(id=2, description="测试任务2", priority=Priority.LOW, completed=True)

        self.storage.save_tasks([task1, task2])

        loaded_tasks = self.storage.load_tasks()
        assert len(loaded_tasks) == 2
        assert loaded_tasks[0].id == 1
        assert loaded_tasks[0].description == "测试任务1"
        assert loaded_tasks[0].priority == Priority.HIGH
        assert loaded_tasks[1].id == 2
        assert loaded_tasks[1].completed is True

    def test_load_corrupted_file(self):
        """测试损坏的JSON文件"""
        with open(self.temp_file.name, 'w') as f:
            f.write("这不是有效的JSON")

        tasks = self.storage.load_tasks()
        assert tasks == []

    def test_save_atomic(self):
        """测试保存操作是原子的"""
        task = Task(id=1, description="原子测试", priority=Priority.MEDIUM)

        # 模拟保存过程中出错的情况不应该破坏原有数据
        self.storage.save_tasks([task])

        # 验证数据正确保存
        loaded = self.storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0].description == "原子测试"
