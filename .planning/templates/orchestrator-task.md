# 编排任务: {task_range}

## 输入

- 实验设计文档: zGSDExpierement.md
- 任务范围: {task_range} (如 T1-T3)

## 输出

为每个任务生成:
1. .planning/experiments/{task_id}/PLAN.md
2. .planning/experiments/{task_id}/STEPS.md

## PLAN.md 模板

```markdown
# 实验计划: {task_id}

## 任务信息
- 任务编号: {task_id}
- 场景类型: {scenario}
- 复杂度: {complexity}
- 任务描述: {description}

## 执行步骤
1. ...
2. ...

## 输入资源
- ...

## 输出要求
- ...

## 验收标准
- ...
```

## STEPS.md 模板

```markdown
# 执行步骤: {task_id}

## GSD模式步骤
| 步骤 | 操作 | 预期输出 |
|------|------|----------|
| 1 | ... | ... |

## 非GSD模式步骤
| 步骤 | 操作 | 预期输出 |
|------|------|----------|
| 1 | ... | ... |
```
