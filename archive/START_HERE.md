# GSD实验启动指南

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 GSD ► 实验准备完成 ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 实验环境已就绪!

实验准备阶段已完成。以下是当前状态:

### 已完成的工作 ✓

- [x] **目录结构创建** - .planning/ 及子目录已就绪
- [x] **状态文件初始化** - experiment-state.json, experiment-queue.json
- [x] **任务模板准备** - orchestrator/executor/validator 模板
- [x] **任务定义完成** - tasks-definition.json (9个任务)
- [x] **示例数据生成** - T4/T5/T6 输入数据已创建
- [x] **执行文档撰写** - EXECUTION_GUIDE.md

### 目录结构

```
z-exp/
├── .planning/
│   ├── experiment-state.json          # 全局状态
│   ├── experiment-queue.json          # 任务队列
│   ├── tasks-definition.json          # 9个任务定义
│   ├── templates/                     # 任务模板
│   │   ├── orchestrator-task.md
│   │   ├── executor-task.md
│   │   └── validator-task.md
│   ├── experiment-results/            # (待生成)
│   ├── experiments/                   # (待生成)
│   ├── messages/                      # (待生成)
│   └── checkpoints/                   # (待生成)
├── input_data/                        # 示例输入数据
│   ├── sales_data_T4.csv             # T4销售数据
│   ├── reviews_data_T5.json          # T5评论数据
│   └── competitor_data_T6.json       # T6竞品数据
├── zGSDExpierement.md                 # 实验设计文档
├── zGSDExecutionPlan.md               # 执行方案
├── EXECUTION_GUIDE.md                 # 详细执行指南
├── README.md                          # 项目概述
└── START_HERE.md                      # 本文件
```

---

## 下一步: 开始实验

实验分为5个阶段,请按顺序执行:

### 阶段1: 准备阶段 (Preparation) ✓ 已完成

---

### 阶段2: 编排阶段 (Orchestration)

**目标:** 为每个任务生成详细的执行计划

**需要做:**
1. 为T1-T9每个任务生成 PLAN.md 和 STEPS.md
2. 创建54个实验任务的队列

**如何开始:**
```
# 方式1: 使用GSD框架 (推荐)
/gsd-manager

# 方式2: 手动编排
请告诉我:"开始编排阶段",我会为T1-T9生成详细计划
```

---

### 阶段3: 执行阶段 (Execution)

**目标:** 执行54次实验 (9任务 × 3重复 × 2模式)

**执行策略:**
- 波次并行,每波4个实验
- 共14-15个Wave

---

### 阶段4: 验证阶段 (Validation)

**目标:** 对所有实验结果进行质量评估

---

### 阶段5: 分析阶段 (Analysis)

**目标:** 生成统计分析、可视化图表和最终报告

---

## 快速开始

**选项A: 使用GSD Manager (推荐)**
```
输入: /gsd-manager
```

**选项B: 手动逐步执行**
```
告诉我:"开始编排阶段"
```

**选项C: 查看详细指南**
```
阅读: EXECUTION_GUIDE.md
```

---

## 实验任务概览

| 任务 | 场景 | 复杂度 | 描述 |
|------|------|--------|------|
| T1 | 代码开发 | 简单 | PNG转WebP脚本 |
| T2 | 代码开发 | 中等 | 命令行待办工具 |
| T3 | 代码开发 | 复杂 | 个人财务管理系统 |
| T4 | 数据分析 | 简单 | 销售数据分析 |
| T5 | 数据分析 | 中等 | 用户评论分析 |
| T6 | 数据分析 | 复杂 | 竞品态势分析 |
| T7 | 创意生成 | 简单 | 智能手表广告文案 |
| T8 | 创意生成 | 中等 | 在线学习平台品牌设计 |
| T9 | 创意生成 | 复杂 | 压力管理App产品方案 |

---

## 准备就绪!

请选择下一步操作:

1. **开始编排阶段** - 为T1-T9生成详细计划
2. **查看详细指南** - 阅读 EXECUTION_GUIDE.md
3. **查看任务定义** - 读取 .planning/tasks-definition.json

请告诉我您想做什么?
