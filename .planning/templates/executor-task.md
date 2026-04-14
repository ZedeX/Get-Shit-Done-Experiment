# 执行任务: {task_id}

## 任务信息
- 任务编号: {task_id}
- 模式: {mode}
- 重复次数: {repeat}

## 输入
- 计划文件: .planning/experiments/{task_id}/PLAN.md
- 步骤文件: .planning/experiments/{task_id}/STEPS.md

## 执行要求

1. 按步骤执行实验操作
2. 记录每个步骤的执行情况
3. 保存所有输出结果
4. 记录Token消耗和执行时间

## 输出

- LOG.md: 执行日志
- OUTPUT/: 输出文件目录
- METRICS.json: 指标数据

## 约束
- 超时限制: {timeout_minutes} 分钟
- 最大重试: 3次
