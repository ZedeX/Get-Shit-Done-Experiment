# GSD实验执行指南

## 概述

本文档详细说明如何执行完整的GSD vs 非GSD对比实验。

## 实验准备 ✓

**已完成:**
- [x] 目录结构创建
- [x] 状态文件初始化
- [x] 任务模板准备
- [x] 任务定义完成

## 实验阶段

### 阶段1: 准备阶段 (Preparation)

**目标:** 确保所有输入资源和环境就绪

#### 任务清单:

1. **生成示例数据文件** (T4, T5, T6需要)
   - 销售数据CSV (T4)
   - 用户评论数据 (T5)
   - 竞品公开数据 (T6)

2. **环境检查**
   - Python环境验证
   - 必要依赖安装
   - 磁盘空间检查 (>10GB)

3. **GSD框架验证**
   - 确认GSD技能可用
   - 测试非GSD模式 (纯净Agent)

---

### 阶段2: 编排阶段 (Orchestration)

**目标:** 为每个任务生成详细的执行计划

#### 任务清单:

1. **解析实验设计**
   - 读取zGSDExpierement.md
   - 提取所有9个任务定义
   - 确认评估指标

2. **生成任务计划** (并行执行)
   - **Orchestrator 1**: T1-T3 计划生成
   - **Orchestrator 2**: T4-T6 计划生成
   - **Orchestrator 3**: T7-T9 计划生成

   每个任务生成:
   - `PLAN.md` - 详细任务计划
   - `STEPS.md` - GSD和非GSD模式步骤

3. **创建任务队列**
   - 生成54个实验任务 (9任务 × 3重复 × 2模式)
   - 设置依赖关系
   - 初始化优先级

**输出:**
```
.planning/experiments/
├── T1/
│   ├── PLAN.md
│   └── STEPS.md
├── T2/
│   ├── PLAN.md
│   └── STEPS.md
└── ... (T3-T9)
```

---

### 阶段3: 执行阶段 (Execution)

**目标:** 执行54次实验,采集过程数据

#### 执行策略: 波次并行 (Wave-based Execution)

**并行度配置:**
- 最大并发Agent: 4
- 每Wave执行4个实验

**Wave序列:**

| Wave | 实验任务 | 模式 |
|------|----------|------|
| 1 | T1-GSD-1, T1-nonGSD-1, T2-GSD-1, T2-nonGSD-1 | 并行 |
| 2 | T1-GSD-2, T1-nonGSD-2, T2-GSD-2, T2-nonGSD-2 | 并行 |
| 3 | T1-GSD-3, T1-nonGSD-3, T2-GSD-3, T2-nonGSD-3 | 并行 |
| 4 | T3-GSD-1, T3-nonGSD-1, T4-GSD-1, T4-nonGSD-1 | 并行 |
| 5 | T3-GSD-2, T3-nonGSD-2, T4-GSD-2, T4-nonGSD-2 | 并行 |
| 6 | T3-GSD-3, T3-nonGSD-3, T4-GSD-3, T4-nonGSD-3 | 并行 |
| 7 | T5-GSD-1, T5-nonGSD-1, T6-GSD-1, T6-nonGSD-1 | 并行 |
| 8 | T5-GSD-2, T5-nonGSD-2, T6-GSD-2, T6-nonGSD-2 | 并行 |
| 9 | T5-GSD-3, T5-nonGSD-3, T6-GSD-3, T6-nonGSD-3 | 并行 |
| 10 | T7-GSD-1, T7-nonGSD-1, T8-GSD-1, T8-nonGSD-1 | 并行 |
| 11 | T7-GSD-2, T7-nonGSD-2, T8-GSD-2, T8-nonGSD-2 | 并行 |
| 12 | T7-GSD-3, T7-nonGSD-3, T8-GSD-3, T8-nonGSD-3 | 并行 |
| 13 | T9-GSD-1, T9-nonGSD-1, (备用) | 并行 |
| 14 | T9-GSD-2, T9-nonGSD-2, (备用) | 并行 |
| 15 | T9-GSD-3, T9-nonGSD-3, (备用) | 并行 |

**每次实验执行内容:**
1. 读取任务计划 (PLAN.md)
2. 按模式执行 (GSD/非GSD)
3. 记录每一步操作
4. 保存输出结果
5. 记录Token消耗和时间

**每个实验输出:**
```
.planning/experiments/{task_id}/execution/{run_id}/
├── LOG.md          # 执行日志
├── METRICS.json    # 指标数据
└── OUTPUT/         # 输出文件目录
```

---

### 阶段4: 验证阶段 (Validation)

**目标:** 对所有实验结果进行质量评估

#### 任务清单:

1. **数据完整性检查**
   - 检查所有54次实验的状态文件
   - 验证必需字段完整性
   - 标记缺失数据

2. **指标评分** (并行执行)
   - **Validator 1**: T1-T3 评分
   - **Validator 2**: T4-T6 评分
   - **Validator 3**: T7-T9 评分

   每个评分包括:
   - 效率指标 (时间、步骤、Token、迭代)
   - 质量指标 (准确率、完整性、错误率、可用性)
   - 过程指标 (任务分解、资源调用、错误修正、上下文管理)
   - 用户体验指标 (指令符合度、交互流畅度、满意度、信任度)

3. **异常数据标记**
   - 检测离群值
   - 标记异常实验
   - 生成异常报告

**输出:**
```
.planning/experiments/{task_id}/validation/{run_id}/
├── REPORT.md   # 验证报告
└── SCORES.json # 评分数据
```

---

### 阶段5: 分析阶段 (Analysis)

**目标:** 生成统计分析、可视化图表和最终报告

#### 任务清单:

1. **数据汇总**
   - 收集所有评分数据
   - 按任务/场景/复杂度/模式分组
   - 计算统计量 (均值、标准差、中位数)

2. **统计检验**
   - 独立样本t检验 / Mann-Whitney U检验
   - 计算效应量 (Cohen's d)
   - 双因素方差分析 (Two-way ANOVA)

3. **可视化生成**
   - 效率对比图 (分组柱状图)
   - 质量指标雷达图
   - 场景-复杂度矩阵热力图
   - 指标相关性散点图

4. **报告撰写**
   - 汇总对比分析
   - 优势边界分析
   - 结论与建议
   - 生成最终报告

**输出:**
```
.planning/experiment-results/
├── SUMMARY.json              # 总体汇总
├── AGGREGATED/               # 聚合数据CSV
│   ├── efficiency_comparison.csv
│   ├── quality_comparison.csv
│   ├── process_comparison.csv
│   └── user_experience_comparison.csv
├── visualizations/           # 可视化图表
│   ├── efficiency_comparison.png
│   ├── quality_radar_code.png
│   ├── quality_radar_data.png
│   ├── quality_radar_creative.png
│   ├── advantage_heatmap.png
│   └── correlation_scatter.png
└── FINAL_REPORT.md           # 最终报告
```

---

## 执行命令参考

### 开始实验

```bash
cd z-exp

# 查看当前状态
ls -la .planning/

# 读取任务定义
cat .planning/tasks-definition.json
```

### 阶段1: 准备阶段

```bash
# 生成示例数据
# (需要手动执行或编写脚本)
```

### 阶段2: 编排阶段

```bash
# 为T1-T3生成计划
# (使用编排Agent)

# 为T4-T6生成计划
# (使用编排Agent)

# 为T7-T9生成计划
# (使用编排Agent)
```

### 阶段3: 执行阶段

```bash
# Wave 1 - 并行执行4个实验
# T1-GSD-1, T1-nonGSD-1, T2-GSD-1, T2-nonGSD-1

# Wave 2 - 并行执行4个实验
# T1-GSD-2, T1-nonGSD-2, T2-GSD-2, T2-nonGSD-2

# ... 继续后续Wave
```

### 阶段4: 验证阶段

```bash
# 验证T1-T3结果
# (使用验证Agent)

# 验证T4-T6结果
# (使用验证Agent)

# 验证T7-T9结果
# (使用验证Agent)
```

### 阶段5: 分析阶段

```bash
# 数据汇总与统计分析
# 生成可视化图表
# 撰写最终报告
```

---

## 断点续传

实验支持断点续传。所有状态持久化到文件:

- `.planning/experiment-state.json` - 全局状态
- `.planning/experiment-queue.json` - 任务队列
- `.planning/experiments/*/STATUS.json` - 任务状态

如需恢复实验,检查上述文件即可继续。

---

## 注意事项

1. **顺序执行**: 阶段必须按顺序执行 (准备 → 编排 → 执行 → 验证 → 分析)
2. **波次并行**: 执行阶段内部采用波次并行,Wave间顺序执行
3. **数据备份**: 定期备份 `.planning/` 目录
4. **异常处理**: 单个实验失败不影响整体,标记后继续
5. **时间预估**: 完整实验预计5-7天
