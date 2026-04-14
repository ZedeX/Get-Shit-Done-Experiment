# 执行步骤: T3

## GSD模式步骤

| 步骤 | 操作 | 预期输出 |
|------|------|----------|
| 1 | 详细需求分析，用例建模 | 需求规格说明书 |
| 2 | 系统架构设计 (分层架构) | 架构设计文档 |
| 3 | 数据库 schema 设计 | ER图 + schema.sql |
| 4 | API接口设计 (RESTful) | API文档 |
| 5 | 创建项目结构 (MVC) | 项目骨架 |
| 6 | 配置依赖 (SQLAlchemy, matplotlib, etc.) | requirements.txt |
| 7 | 实现数据模型 (Transaction, Budget, Category) | models.py |
| 8 | 实现数据库CRUD操作 | crud.py |
| 9 | 实现业务逻辑服务层 | services/ |
| 10 | 实现CLI命令组 | cli/ |
| 11 | 实现可视化报表模块 (matplotlib) | visualizer.py |
| 12 | 实现CSV导入导出功能 | importer_exporter.py |
| 13 | 编写单元测试 | tests/ |
| 14 | 集成测试和端到端测试 | 测试报告 |
| 15 | 数据备份和恢复功能 | backup.py |
| 16 | 代码审查和性能优化 | 优化后的代码 |
| 17 | 用户手册和开发文档 | docs/ |
| 18 | 安全审计 (SQL注入, 数据验证) | 安全报告 |

## 非GSD模式步骤

| 步骤 | 操作 | 预期输出 |
|------|------|----------|
| 1 | 创建finance.py主文件 | finance.py |
| 2 | 定义Transaction类 | 数据类 |
| 3 | 实现添加收支记录 | add功能 |
| 4 | 实现列表显示 | list功能 |
| 5 | 添加JSON存储 | 持久化 |
| 6 | 添加简单的分类功能 | 分类 |
| 7 | 实现简单的统计显示 | 统计 |
| 8 | 添加matplotlib图表 | 可视化 |
| 9 | 测试基本功能 | 可运行系统 |
| 10 | 根据需要扩展功能 | 扩展功能 |

## 关键文件

- **主程序**: `finance.py` 或 `main.py`
- **数据库**: `finance.db` (SQLite)
- **数据文件**: `data.json`
- **文档**: `README.md`, `USER_GUIDE.md`
