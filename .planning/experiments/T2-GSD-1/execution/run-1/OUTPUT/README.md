# 命令行待办事项管理工具

一个简单易用的命令行待办事项管理工具，支持任务添加、删除、标记完成、按优先级排序和数据持久化。

## 功能特性

- ✅ 添加任务（支持低/中/高优先级）
- ✅ 删除任务
- ✅ 标记任务完成
- ✅ 列出所有任务（可按优先级排序）
- ✅ JSON文件持久化存储
- ✅ 友好的命令行界面

## 安装

无需安装，直接运行即可。需要 Python 3.7+。

## 使用方法

### 添加任务

```bash
# 添加默认优先级（中）的任务
python main.py add "完成项目报告"

# 添加高优先级任务
python main.py add "紧急bug修复" high

# 添加低优先级任务
python main.py add "整理文档" low
```

### 列出任务

```bash
# 按添加顺序列出
python main.py list

# 按优先级排序（高优先级在前）
python main.py list --sort priority
```

### 标记任务完成

```bash
# 标记ID为1的任务完成
python main.py complete 1
```

### 删除任务

```bash
# 删除ID为2的任务
python main.py delete 2
```

### 查看帮助

```bash
python main.py --help
python main.py add --help
```

## 项目结构

```
todo_tool/
├── todo/
│   ├── __init__.py          # 包初始化
│   ├── storage.py           # JSON存储管理
│   ├── task.py              # 任务模型和业务逻辑
│   └── cli.py               # 命令行接口
├── main.py                  # 主程序入口
├── tests/
│   ├── __init__.py
│   ├── test_storage.py      # 存储测试
│   └── test_task.py         # 业务逻辑测试
└── README.md                # 本文档
```

## 数据存储

任务数据保存在 `tasks.json` 文件中，格式如下：

```json
[
  {
    "id": 1,
    "description": "完成项目报告",
    "priority": 3,
    "completed": false,
    "created_at": "2026-04-14T16:00:00.000000"
  }
]
```

## 运行测试

使用 pytest 运行测试：

```bash
pip install pytest
pytest tests/ -v
```

## 使用示例

```bash
# 添加几个任务
$ python main.py add "写代码" high
已添加任务: #1 写代码

$ python main.py add "写文档" medium
已添加任务: #2 写文档

$ python main.py add "休息一下" low
已添加任务: #3 休息一下

# 查看所有任务
$ python main.py list
○ #  1 [高] 写代码
○ #  2 [中] 写文档
○ #  3 [低] 休息一下

# 按优先级排序查看
$ python main.py list --sort priority
○ #  1 [高] 写代码
○ #  2 [中] 写文档
○ #  3 [低] 休息一下

# 标记任务完成
$ python main.py complete 1
已标记任务完成: #1 写代码

# 再次查看
$ python main.py list
✓ #  1 [高] 写代码
○ #  2 [中] 写文档
○ #  3 [低] 休息一下

# 删除任务
$ python main.py delete 3
已删除任务 #3
```

## 许可证

MIT License
