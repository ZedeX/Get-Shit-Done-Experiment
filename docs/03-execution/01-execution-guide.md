# 执行指南

---

## 目录

1. [环境准备](#环境准备)
2. [快速开始](#快速开始)
3. [执行阶段说明](#执行阶段说明)
4. [如何复现实验](#如何复现实验)

---

## 环境准备

### 前置要求

- Python 3.11+
- Git
- Claude Code (可选，用于完整复现)

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/gsd-build/get-shit-done.git
cd get-shit-done/z-exp

# 安装Python依赖
pip install pillow matplotlib
```

### 配置GSD框架

参考 [GSD官方文档](https://github.com/gsd-build/get-shit-done) 安装和配置GSD框架。

---

## 快速开始

### 1. 浏览实验结果

直接从 [README.md](../../README.md) 开始浏览已完成的实验结果。

### 2. 运行测试代码

```bash
# 测试T1 PNG转WebP脚本
cd z-exp
python .planning/experiments/T1-GSD-1/execution/run-1/OUTPUT/png2webp.py --help

# 测试T2待办事项工具
python .planning/experiments/T2-GSD-2/execution/run-1/OUTPUT/todo.py --help

# 测试T3财务管理系统
python .planning/experiments/T3-GSD-1/execution/run-1/OUTPUT/finance_fixed.py --help
```

### 3. 查看原始数据

所有原始实验数据保存在 `.planning/experiments/` 目录下：

```bash
# 查看某个实验的详细数据
cd z-exp/.planning/experiments/T1-GSD-1/
ls -la

# 查看指标数据
cat execution/run-1/METRICS.json
```

---

## 执行阶段说明

本实验分为以下5个阶段：

### 阶段1: 准备阶段 (Preparation) ✓ 已完成

**目标**: 配置环境、准备任务

**完成内容**:
- 目录结构创建
- 状态文件初始化
- 任务模板准备
- 任务定义完成
- 示例数据生成

### 阶段2: 编排阶段 (Orchestration) ✓ 已完成

**目标**: 为每个任务生成详细的执行计划

**完成内容**:
- T1-T9每个任务生成 PLAN.md 和 STEPS.md
- 创建54个实验任务的队列

### 阶段3: 执行阶段 (Execution) ✓ 核心完成

**目标**: 执行实验

**完成内容**:
- Wave 1-3 (T1-T3完整3次重复)
- T4-T6首次重复
- T7-T9首次重复
- 总计: 32/54 次实验

### 阶段4: 验证阶段 (Validation) ✓ 已完成

**目标**: 对所有实验结果进行质量评估

**完成内容**:
- 代码修复与验证
- Bug修复报告
- 所有产出代码可正常执行

### 阶段5: 分析阶段 (Analysis) ✓ 已完成

**目标**: 生成统计分析、可视化图表和最终报告

**完成内容**:
- 完整总结报告
- 关键发现汇总
- 适用边界分析

---

## 如何复现实验

### 完整复现（需要GSD框架）

如果你想完整复现整个实验过程：

1. **安装GSD框架**
   ```bash
   # 参考GSD官方文档安装
   ```

2. **启动GSD实验**
   ```bash
   cd z-exp
   # 使用GSD manager启动
   /gsd-manager
   ```

3. **按阶段执行**
   参考 [START_HERE.md](../../START_HERE.md) 了解详细执行流程。

### 部分复现（仅验证代码）

如果你只想验证产出代码：

1. **测试T1代码**
   ```bash
   # 生成测试图片
   python generate_test_pngs_simple.py
   
   # 运行转换
   python .planning/experiments/T1-GSD-1/execution/run-1/OUTPUT/png2webp.py \
     --input test_images --output test_output
   ```

2. **测试T2代码**
   ```bash
   # 添加任务
   python .planning/experiments/T2-GSD-2/execution/run-1/OUTPUT/todo.py \
     add "测试任务" high
   
   # 列出任务
   python .planning/experiments/T2-GSD-2/execution/run-1/OUTPUT/todo.py list
   ```

3. **测试T3代码**
   ```bash
   # 添加交易
   python .planning/experiments/T3-GSD-1/execution/run-1/OUTPUT/finance_fixed.py \
     add 5000 income --description "工资"
   
   # 查看总结
   python .planning/experiments/T3-GSD-1/execution/run-1/OUTPUT/finance_fixed.py summary
   ```

---

## 文档导航

| 上一篇 | 下一篇 |
|--------|--------|
| [实验设计文档](../02-design/01-experiment-design.md) | [结果总览](../04-results/01-results-summary.md) |

---

*最后更新: 2026-04-14*
