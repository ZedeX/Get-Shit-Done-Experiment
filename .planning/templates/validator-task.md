# 验证任务: {task_id}

## 任务信息
- 任务编号: {task_id}
- 模式: {mode}
- 重复次数: {repeat}

## 输入
- 执行日志: .planning/experiments/{task_id}/execution/{run_id}/LOG.md
- 输出目录: .planning/experiments/{task_id}/execution/{run_id}/OUTPUT/
- 指标数据: .planning/experiments/{task_id}/execution/{run_id}/METRICS.json

## 验证要求

按照评估指标体系进行评分:

### 效率指标
- 任务完成时间: [分钟]
- 步骤数量: [个]
- Token消耗: [数量]
- 迭代次数: [次]

### 质量指标
- 结果准确率: [0-100%]
- 完整性评分: [1-10]
- 错误率: [0-100%]
- 可用性评分: [1-10]

### 过程指标
- 任务分解合理性: [1-10]
- 资源调用效率: [1-10]
- 错误修正能力: [1-10]
- 上下文管理: [1-10]

### 用户体验指标
- 指令符合度: [1-10]
- 交互流畅度: [1-10]
- 结果满意度: [1-10]
- 信任度: [1-10]

## 输出

- REPORT.md: 验证报告
- SCORES.json: 评分数据
