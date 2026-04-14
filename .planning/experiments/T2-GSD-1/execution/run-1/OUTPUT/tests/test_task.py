"""
测试任务管理业务逻辑
"""
import tempfile
import os
import pytest

from todo.task import TaskManager, Task, Priority
from todo.storage import StorageManager


class TestTask:
    """测试Task数据类"""

    def test_task_creation(self):
        """测试创建任务"""
        task = Task(id=1, description="测试任务", priority=Priority.HIGH)
        assert task.id == 1
        assert task.description == "测试任务"
        assert task.priority == Priority.HIGH
        assert task.completed is False
        assert task.created_at is not None

    def test_task_priority_from_int(self):
        """测试从整数创建优先级"""
        task = Task(id=1, description="测试", priority=3)
        assert task.priority == Priority.HIGH

    def test_task_priority_from_string(self):
        """测试从字符串创建优先级"""
        task = Task(id=1, description="测试", priority="low")
        assert task.priority == Priority.LOW


class TestTaskManager:
    """测试TaskManager类"""

    def setup_method(self):
        """每个测试前创建临时存储"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.storage = StorageManager(self.temp_file.name)
        self.manager = TaskManager(self.storage)

    def teardown_method(self):
        """每个测试后删除临时文件"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_add_task(self):
        """测试添加任务"""
        task = self.manager.add_task("新任务", Priority.HIGH)
        assert task.id == 1
        assert task.description == "新任务"
        assert task.priority == Priority.HIGH

        tasks = self.manager.list_tasks()
        assert len(tasks) == 1

    def test_add_task_empty_description(self):
        """测试添加空描述任务应该报错"""
        with pytest.raises(ValueError):
            self.manager.add_task("")

    def test_add_task_whitespace_description(self):
        """测试添加只有空格的描述应该报错"""
        with pytest.raises(ValueError):
            self.manager.add_task("   ")

    def test_delete_task(self):
        """测试删除任务"""
        self.manager.add_task("任务1")
        self.manager.add_task("任务2")

        result = self.manager.delete_task(1)
        assert result is True

        tasks = self.manager.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_delete_nonexistent_task(self):
        """测试删除不存在的任务"""
        result = self.manager.delete_task(999)
        assert result is False

    def test_complete_task(self):
        """测试标记任务完成"""
        self.manager.add_task("待完成任务")

        task = self.manager.complete_task(1)
        assert task is not None
        assert task.completed is True

        tasks = self.manager.list_tasks()
        assert tasks[0].completed is True

    def test_complete_nonexistent_task(self):
        """测试标记不存在的任务完成"""
        task = self.manager.complete_task(999)
        assert task is None

    def test_list_tasks_sort_by_priority(self):
        """测试按优先级排序"""
        self.manager.add_task("低优先级", Priority.LOW)
        self.manager.add_task("高优先级", Priority.HIGH)
        self.manager.add_task("中优先级", Priority.MEDIUM)

        tasks = self.manager.list_tasks(sort_by_priority=True)
        assert len(tasks) == 3
        assert tasks[0].priority == Priority.HIGH
        assert tasks[1].priority == Priority.MEDIUM
        assert tasks[2].priority == Priority.LOW

    def test_get_task(self):
        """测试获取单个任务"""
        self.manager.add_task("测试任务")

        task = self.manager.get_task(1)
        assert task is not None
        assert task.description == "测试任务"

        task = self.manager.get_task(999)
        assert task is None

    def test_task_id_increment(self):
        """测试任务ID自动递增"""
        task1 = self.manager.add_task("任务1")
        task2 = self.manager.add_task("任务2")
        assert task1.id == 1
        assert task2.id == 2

        self.manager.delete_task(1)
        task3 = self.manager.add_task("任务3")
        assert task3.id == 3  # 应该继续递增，而不是复用已删除的ID
