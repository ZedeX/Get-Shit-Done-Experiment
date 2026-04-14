# GSD vs 非GSD模式Agent表现对比实验

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code](https://img.shields.io/badge/Claude-Code-orange.svg)](https://claude.ai)

> 系统性评估GSD（Get Shit Done）框架对AI Agent任务完成表现的影响

---

## 快速导航

| 阶段 | 文档 | 状态 |
|------|------|------|
| 🎯 **背景介绍** | [项目背景与目标](docs/01-background/01-introduction.md) | ✓ |
| 📋 **实验设计** | [完整实验设计文档](docs/02-design/01-experiment-design.md) | ✓ |
| 🚀 **执行指南** | [如何复现实验](docs/03-execution/01-execution-guide.md) | ✓ |
| 📊 **结果汇总** | [实验结果总览](docs/04-results/01-results-summary.md) | ✓ |
| 📈 **数据分析** | [统计分析与可视化](docs/05-analysis/01-statistical-analysis.md) | ✓ |
| ✅ **质量验证** | [代码修复与验证报告](docs/06-validation/01-validation-summary.md) | ✓ |

---

## 实验概述

本实验系统性评估GSD（Get Shit Done）框架对AI Agent任务完成表现的影响，明确其在不同复杂度任务和应用场景中的实际效果差异与适用边界。

### 使用的技能与工具

- **GSD Framework**: [get-shit-done](https://github.com/gsd-build/get-shit-done) - 结构化AI任务执行框架
- **Claude Code**: AI驱动的代码编辑器与执行环境
- **Python 3.11+**: 实验代码运行环境

### 实验规模

- **9个任务** × **3次重复** × **2种模式** = **54次实验**
- **3种场景**：代码开发、数据分析、创意生成
- **3种复杂度**：简单、中等、复杂

### 当前进度

- ✅ **已完成**: 32/54 次实验 (59%)
- ✅ **代码验证**: 所有产出代码已修复并验证可执行
- ✅ **透明度记录**: 所有实验包含完整执行记录

---

## 实验任务矩阵

| 任务编号 | 场景类型 | 复杂度 | 任务描述 | 状态 |
|----------|----------|--------|----------|------|
| **T1** | 代码开发 | 简单 | PNG到WebP批量转换脚本 | ✓ 3/3 |
| **T2** | 代码开发 | 中等 | 命令行待办事项管理工具 | ✓ 3/3 |
| **T3** | 代码开发 | 复杂 | 个人财务管理系统 | ✓ 3/3 |
| **T4** | 数据分析 | 简单 | 销售数据分析 | ✓ 1/3 |
| **T5** | 数据分析 | 中等 | 电商用户评论分析 | ✓ 1/3 |
| **T6** | 数据分析 | 复杂 | 竞品竞争态势分析 | ✓ 1/3 |
| **T7** | 创意生成 | 简单 | 智能手表广告文案 | ✓ 1/3 |
| **T8** | 创意生成 | 中等 | 在线学习平台品牌设计 | ✓ 1/3 |
| **T9** | 创意生成 | 复杂 | 压力管理App产品方案 | ✓ 1/3 |

---

## 关键发现摘要

### 1. GSD优势随复杂度增加而显著提升

| 复杂度 | GSD评分 | non-GSD评分 | GSD优势 | 优势度 |
|--------|---------|-------------|---------|--------|
| 简单 | 92.5 | 75.5 | +17.0 | +23% |
| 中等 | 93.5 | 71.5 | +22.0 | +31% |
| 复杂 | 95.0 | 65.0 | +30.0 | +46% |

### 2. 零迭代是GSD的核心竞争优势

| 复杂度 | GSD迭代 | non-GSD迭代 | 减少 |
|--------|---------|-------------|------|
| 简单 | 0次 | 1次 | 1次 |
| 中等 | 0次 | 2次 | 2次 |
| 复杂 | 0次 | 3-4次 | 3-4次 |

### 3. 跨场景一致性表现

| 场景 | GSD优势度 | 备注 |
|------|-----------|------|
| 代码开发 | +33% | 最显著，结构化强 |
| 数据分析 | +28% | 显著，逻辑清晰 |
| 创意生成 | +25% | 明显，需要更多判断 |

---

## 目录结构

```
z-exp/
├── README.md                           # 本文件（项目入口）
├── docs/                               # 重新组织的文档
│   ├── 01-background/                  # 背景介绍
│   │   ├── 01-introduction.md         # 项目介绍与目标
│   │   └── 02-related-work.md         # 相关工作与参考
│   ├── 02-design/                     # 实验设计
│   │   ├── 01-experiment-design.md    # 完整实验设计
│   │   ├── 02-task-definitions.md     # 任务定义详情
│   │   └── 03-metrics-framework.md    # 评估指标框架
│   ├── 03-execution/                  # 执行记录
│   │   ├── 01-execution-guide.md      # 执行指南
│   │   ├── 02-wave1-summary.md        # Wave 1总结
│   │   ├── 03-wave2-summary.md        # Wave 2总结
│   │   └── 04-wave3-summary.md        # Wave 3总结
│   ├── 04-results/                     # 结果汇总
│   │   ├── 01-results-summary.md      # 结果总览
│   │   ├── 02-code-dev-results.md     # 代码开发场景结果
│   │   ├── 03-data-analysis-results.md # 数据分析场景结果
│   │   └── 04-creative-results.md     # 创意生成场景结果
│   ├── 05-analysis/                    # 深度分析
│   │   ├── 01-statistical-analysis.md # 统计分析
│   │   ├── 02-visualizations.md       # 可视化图表
│   │   └── 03-applicability-boundary.md # 适用边界分析
│   └── 06-validation/                  # 质量验证
│       ├── 01-validation-summary.md   # 验证总览
│       ├── 02-bugfix-report.md         # Bug修复报告
│       └── 03-code-samples.md          # 代码样例
├── .planning/                          # 原始实验数据
│   ├── experiment-state.json            # 全局状态
│   ├── experiment-queue.json            # 任务队列
│   ├── tasks-definition.json            # 任务定义
│   └── experiments/                     # 各实验详细记录
├── input_data/                          # 实验输入数据
│   ├── sales_data_T4.csv               # T4销售数据
│   ├── reviews_data_T5.json            # T5评论数据
│   └── competitor_data_T6.json         # T6竞品数据
├── test_images/                         # 测试图片
└── [原始报告文件...]                   # 保留原始报告作为参考
```

---

## 如何使用本仓库

### 1. 浏览实验结果

从 [README.md](README.md) 开始，按导航链接浏览各个阶段的文档。

### 2. 复现实验

参考 [docs/03-execution/01-execution-guide.md](docs/03-execution/01-execution-guide.md) 了解如何复现实验。

### 3. 查看原始数据

所有原始实验数据保存在 `.planning/experiments/` 目录下，包含：
- 完整执行日志
- 透明度记录
- 产出代码
- 指标数据

---

## 关键结论

### 推荐使用场景

**强烈推荐使用GSD**:
- 复杂任务（所有场景）
- 生产级代码开发
- 需要高质量文档的任务
- 长期维护的项目
- 安全相关的任务

**可选使用GSD**:
- 中等复杂度任务
- 需要一定质量的快速原型
- 学习和教育场景

**不推荐使用GSD**:
- 简单的一次性脚本
- 快速探索性任务
- Token预算极其有限的场景

---

## 贡献与反馈

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License - 详见 [LICENSE](../LICENSE)

---

## 引用

如果您在研究中使用了本实验的数据，请引用：

```bibtex
@misc{gsd-vs-nongs-2026,
  author = {GSD Experiment Team},
  title = {GSD vs non-GSD AI Agent Performance Comparison},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/gsd-build/get-shit-done}
}
```

---

## 致谢

- [GSD Framework](https://github.com/gsd-build/get-shit-done) - 提供结构化任务执行框架
- [Claude Code](https://claude.ai) - AI驱动的代码编辑环境

---

*最后更新: 2026-04-14*
