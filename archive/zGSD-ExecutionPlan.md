# GSD实验多Agent协作执行方案

## 一、系统架构概览

### 1.1 架构模式选择

采用 **Supervisor/Orchestrator 模式**，配合 **分层并行执行** 策略。

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户/实验管理员                                │
│                    (启动实验、监控进度、审核结果)                         │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         主控Agent (Supervisor)                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐             │
│  │  流程编排   │  任务分配   │  进度跟踪   │  异常处理   │             │
│  └─────────────┴─────────────┴─────────────┴─────────────┘             │
│                                                                         │
│  状态存储: .planning/experiment-state.json                              │
│  任务队列: .planning/experiment-queue.json                              │
│  结果汇总: .planning/experiment-results.json                            │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│  编排Agent池   │         │  执行Agent池   │         │  验证Agent池   │
│ (Orchestrator)│         │ (Executor)    │         │ (Validator)   │
├───────────────┤         ├───────────────┤         ├───────────────┤
│ - 步骤撰写    │         │ - 实验执行    │         │ - 结果验收    │
│ - 任务分解    │         │ - 数据采集    │         │ - 质量评估    │
│ - 计划生成    │         │ - 过程记录    │         │ - 异常检测    │
└───────┬───────┘         └───────┬───────┘         └───────┬───────┘
        │                         │                         │
        └─────────────────────────┼─────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         调试Agent (Debugger)                            │
│                    (按需激活，处理异常与错误修复)                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 核心设计原则

| 原则 | 说明 |
|------|------|
| **Context Isolation** | 每个子Agent拥有独立上下文窗口，避免上下文污染 |
| **State Persistence** | 所有状态持久化到文件系统，支持断点续传 |
| **Parallel Execution** | 独立任务并行执行，依赖任务顺序执行 |
| **Fail-Safe** | 单点故障不影响整体，支持任务重试与恢复 |
| **Direct Pass-Through** | 子Agent可直接输出结果，避免"电话游戏"问题 |

---

## 二、Agent角色定义

### 2.1 主控Agent (Supervisor Agent)

```yaml
name: gsd-experiment-supervisor
description: 实验流程全局监控与协调中心
context_window: 200000
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - LS
  - RunCommand
  - Task  # 用于启动子Agent

responsibilities:
  - 实验流程编排与调度
  - 任务队列管理
  - 进度监控与报告
  - 异常检测与恢复
  - 结果汇总与整合

state_file: .planning/experiment-state.json
```

### 2.2 编排Agent (Orchestrator Agent)

```yaml
name: gsd-experiment-orchestrator
description: 实验步骤撰写与任务分解
context_window: 200000
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

responsibilities:
  - 解析实验设计文档
  - 生成标准化实验步骤
  - 分解任务为可执行单元
  - 创建实验执行计划

output:
  - .planning/experiments/{task_id}/PLAN.md
  - .planning/experiments/{task_id}/STEPS.md
```

### 2.3 执行Agent (Executor Agent)

```yaml
name: gsd-experiment-executor
description: 实验操作执行与数据采集
context_window: 200000
tools:
  - Read
  - Write
  - Edit
  - RunCommand
  - Glob
  - Grep
  - WebSearch
  - WebFetch

responsibilities:
  - 执行具体实验操作
  - 记录执行过程数据
  - 采集实验输出
  - 保存中间结果

output:
  - .planning/experiments/{task_id}/execution/{run_id}/
  - .planning/experiments/{task_id}/execution/{run_id}/LOG.md
  - .planning/experiments/{task_id}/execution/{run_id}/OUTPUT/
```

### 2.4 验证Agent (Validator Agent)

```yaml
name: gsd-experiment-validator
description: 实验结果验收与质量评估
context_window: 200000
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

responsibilities:
  - 验证实验完成度
  - 评估结果质量
  - 填写评估指标表格
  - 检测异常数据

output:
  - .planning/experiments/{task_id}/validation/{run_id}/REPORT.md
  - .planning/experiments/{task_id}/validation/{run_id}/SCORES.json
```

### 2.5 调试Agent (Debugger Agent)

```yaml
name: gsd-experiment-debugger
description: 异常处理与错误修复
context_window: 200000
tools:
  - Read
  - Write
  - Edit
  - RunCommand
  - Glob
  - Grep

responsibilities:
  - 分析失败原因
  - 制定修复方案
  - 执行修复操作
  - 验证修复效果

trigger: 按需激活 (on-failure)
output:
  - .planning/experiments/{task_id}/debug/{debug_id}/ANALYSIS.md
  - .planning/experiments/{task_id}/debug/{debug_id}/FIX.md
```

---

## 三、通信协议设计

### 3.1 状态文件协议

所有Agent间通信通过文件系统实现，确保状态持久化和可追溯。

#### 3.1.1 全局状态文件

**路径**: `.planning/experiment-state.json`

```json
{
  "experiment_id": "EXP-2026-04-14-001",
  "status": "running",
  "started_at": "2026-04-14T10:00:00Z",
  "updated_at": "2026-04-14T12:30:00Z",
  "config": {
    "total_tasks": 9,
    "repeats": 3,
    "modes": ["GSD", "non-GSD"],
    "parallel_limit": 4
  },
  "progress": {
    "total_experiments": 54,
    "completed": 12,
    "running": 4,
    "pending": 38,
    "failed": 0
  },
  "current_phase": "execution",
  "active_agents": [
    {"agent_id": "executor-001", "task": "T1-GSD-1", "status": "running"},
    {"agent_id": "executor-002", "task": "T1-nonGSD-1", "status": "running"},
    {"agent_id": "executor-003", "task": "T2-GSD-1", "status": "running"},
    {"agent_id": "executor-004", "task": "T2-nonGSD-1", "status": "running"}
  ],
  "checkpoints": [
    {"phase": "preparation", "completed_at": "2026-04-14T09:00:00Z"},
    {"phase": "orchestration", "completed_at": "2026-04-14T10:00:00Z"}
  ]
}
```

#### 3.1.2 任务队列文件

**路径**: `.planning/experiment-queue.json`

```json
{
  "queue_id": "QUEUE-001",
  "created_at": "2026-04-14T10:00:00Z",
  "tasks": [
    {
      "task_id": "T1-GSD-1",
      "experiment_task": "T1",
      "mode": "GSD",
      "repeat": 1,
      "status": "pending",
      "priority": 1,
      "dependencies": [],
      "assigned_agent": null,
      "created_at": "2026-04-14T10:00:00Z",
      "started_at": null,
      "completed_at": null,
      "retry_count": 0,
      "max_retries": 3
    }
  ],
  "completed_tasks": [],
  "failed_tasks": []
}
```

#### 3.1.3 任务状态文件

**路径**: `.planning/experiments/{task_id}/STATUS.json`

```json
{
  "task_id": "T1-GSD-1",
  "experiment_task": "T1",
  "mode": "GSD",
  "repeat": 1,
  "status": "completed",
  "phases": {
    "orchestration": {
      "status": "completed",
      "started_at": "2026-04-14T10:00:00Z",
      "completed_at": "2026-04-14T10:05:00Z",
      "output": ".planning/experiments/T1-GSD-1/PLAN.md"
    },
    "execution": {
      "status": "completed",
      "started_at": "2026-04-14T10:05:00Z",
      "completed_at": "2026-04-14T10:45:00Z",
      "output": ".planning/experiments/T1-GSD-1/execution/run-1/"
    },
    "validation": {
      "status": "completed",
      "started_at": "2026-04-14T10:45:00Z",
      "completed_at": "2026-04-14T10:50:00Z",
      "output": ".planning/experiments/T1-GSD-1/validation/run-1/REPORT.md"
    }
  },
  "metrics": {
    "completion_time_minutes": 45,
    "token_usage": 125000,
    "steps_count": 23,
    "iteration_count": 1
  },
  "scores": {
    "accuracy": 95,
    "completeness": 9,
    "usability": 8,
    "satisfaction": 9
  }
}
```

### 3.2 消息传递协议

#### 3.2.1 任务分配消息

**路径**: `.planning/messages/{agent_id}/assignment.json`

```json
{
  "message_id": "MSG-2026-04-14-001",
  "message_type": "task_assignment",
  "timestamp": "2026-04-14T10:00:00Z",
  "sender": "supervisor",
  "receiver": "executor-001",
  "payload": {
    "task_id": "T1-GSD-1",
    "task_type": "execution",
    "experiment_task": "T1",
    "mode": "GSD",
    "repeat": 1,
    "task_description": "编写一个Python脚本，实现将指定目录下所有PNG图片批量转换为WebP格式",
    "input_resources": [
      ".planning/experiments/T1-GSD-1/PLAN.md",
      ".planning/experiments/T1-GSD-1/STEPS.md"
    ],
    "output_requirements": {
      "log_file": ".planning/experiments/T1-GSD-1/execution/run-1/LOG.md",
      "output_dir": ".planning/experiments/T1-GSD-1/execution/run-1/OUTPUT/"
    },
    "constraints": {
      "timeout_minutes": 60,
      "max_retries": 3
    }
  }
}
```

#### 3.2.2 状态更新消息

**路径**: `.planning/messages/supervisor/status-update.json`

```json
{
  "message_id": "MSG-2026-04-14-002",
  "message_type": "status_update",
  "timestamp": "2026-04-14T10:30:00Z",
  "sender": "executor-001",
  "receiver": "supervisor",
  "payload": {
    "task_id": "T1-GSD-1",
    "status": "running",
    "progress_percent": 60,
    "current_step": "执行脚本编写",
    "steps_completed": 14,
    "steps_total": 23,
    "token_usage": 75000,
    "errors_encountered": [],
    "estimated_completion": "2026-04-14T10:45:00Z"
  }
}
```

#### 3.2.3 完成通知消息

**路径**: `.planning/messages/supervisor/completion.json`

```json
{
  "message_id": "MSG-2026-04-14-003",
  "message_type": "task_completion",
  "timestamp": "2026-04-14T10:50:00Z",
  "sender": "validator-001",
  "receiver": "supervisor",
  "payload": {
    "task_id": "T1-GSD-1",
    "status": "completed",
    "completion_time_minutes": 45,
    "output_location": ".planning/experiments/T1-GSD-1/",
    "metrics": {
      "completion_time_minutes": 45,
      "token_usage": 125000,
      "steps_count": 23,
      "iteration_count": 1
    },
    "scores": {
      "accuracy": 95,
      "completeness": 9,
      "usability": 8,
      "satisfaction": 9
    },
    "issues_found": [],
    "requires_review": false
  }
}
```

#### 3.2.4 异常报告消息

**路径**: `.planning/messages/supervisor/error-report.json`

```json
{
  "message_id": "MSG-2026-04-14-004",
  "message_type": "error_report",
  "timestamp": "2026-04-14T10:35:00Z",
  "sender": "executor-002",
  "receiver": "supervisor",
  "payload": {
    "task_id": "T1-nonGSD-1",
    "error_type": "execution_failure",
    "error_message": "脚本执行超时，超过60分钟限制",
    "error_details": {
      "last_successful_step": 18,
      "failed_step": "验证脚本功能",
      "error_output": "TimeoutError: Execution exceeded 3600 seconds"
    },
    "context": {
      "token_usage": 180000,
      "steps_completed": 18,
      "retry_count": 0
    },
    "suggested_action": "retry_with_increased_timeout",
    "requires_debugger": true
  }
}
```

### 3.3 直接输出协议

为避免"电话游戏"问题，子Agent可通过 `forward_message` 机制直接输出结果：

```json
{
  "message_type": "direct_response",
  "sender": "executor-001",
  "content": "## 实验执行完成\n\n任务T1-GSD-1已完成，产出文件位于...",
  "bypass_supervisor": true
}
```

---

## 四、任务分配机制

### 4.1 任务分解策略

```
实验设计文档 (zGSDExpierement.md)
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                    任务分解树                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Experiment (EXP-001)                                       │
│  ├── Phase 1: Preparation (准备阶段)                        │
│  │   ├── P1-1: 环境配置                                     │
│  │   ├── P1-2: 任务准备                                     │
│  │   └── P1-3: 评估工具准备                                 │
│  │                                                         │
│  ├── Phase 2: Orchestration (编排阶段)                      │
│  │   ├── P2-1: 解析实验设计文档                             │
│  │   ├── P2-2: 生成9组任务计划                              │
│  │   └── P2-3: 创建任务队列                                 │
│  │                                                         │
│  ├── Phase 3: Execution (执行阶段)                          │
│  │   ├── T1-GSD × 3次                                      │
│  │   ├── T1-nonGSD × 3次                                   │
│  │   ├── T2-GSD × 3次                                      │
│  │   ├── ... (共54次实验)                                  │
│  │   └── T9-nonGSD × 3次                                   │
│  │                                                         │
│  ├── Phase 4: Validation (验证阶段)                         │
│  │   ├── V-1: 数据完整性检查                                │
│  │   ├── V-2: 指标评分汇总                                  │
│  │   └── V-3: 异常数据标记                                  │
│  │                                                         │
│  └── Phase 5: Analysis (分析阶段)                           │
│      ├── A-1: 统计检验                                      │
│      ├── A-2: 可视化生成                                    │
│      └── A-3: 报告撰写                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 任务优先级规则

| 优先级 | 规则 | 示例 |
|--------|------|------|
| P0 (最高) | 阻塞性任务 | 环境配置失败需立即处理 |
| P1 | 准备阶段任务 | 任务计划生成 |
| P2 | 执行阶段任务 | 实验执行 |
| P3 | 验证阶段任务 | 结果验收 |
| P4 (最低) | 分析阶段任务 | 报告生成 |

### 4.3 依赖关系图

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ P1: 准备    │────▶│ P2: 编排    │────▶│ P3: 执行    │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌─────────────┐             │
                    │ P4: 验证    │◀────────────┘
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ P5: 分析    │
                    └─────────────┘

执行阶段内部并行:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Wave 1 (并行): T1-GSD-1, T1-nonGSD-1, T2-GSD-1, T2-nonGSD-1
│                                                         │
│  Wave 2 (并行): T1-GSD-2, T1-nonGSD-2, T2-GSD-2, T2-nonGSD-2
│                                                         │
│  Wave 3 (并行): T1-GSD-3, T1-nonGSD-3, T2-GSD-3, T2-nonGSD-3
│                                                         │
│  ... (按批次并行执行)                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.4 任务分配流程

```
┌─────────────────────────────────────────────────────────────────┐
│                      主控Agent任务分配流程                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 检查任务队列                                                 │
│     │                                                          │
│     ▼                                                          │
│  2. 筛选可执行任务                                               │
│     │  - 状态为 pending                                         │
│     │  - 依赖任务已完成                                          │
│     │  - 未超过并行限制                                          │
│     │                                                          │
│     ▼                                                          │
│  3. 按优先级排序                                                 │
│     │                                                          │
│     ▼                                                          │
│  4. 分配Agent                                                   │
│     │  - 检查可用Agent池                                         │
│     │  - 分配最适合的Agent类型                                   │
│     │  - 更新任务状态为 assigned                                 │
│     │                                                          │
│     ▼                                                          │
│  5. 发送任务分配消息                                             │
│     │  - 创建 assignment.json                                   │
│     │  - 更新 experiment-state.json                             │
│     │                                                          │
│     ▼                                                          │
│  6. 监控执行状态                                                 │
│     │  - 定期检查状态更新消息                                    │
│     │  - 处理完成/异常消息                                       │
│     │                                                          │
│     ▼                                                          │
│  7. 更新全局状态                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、并行度控制策略

### 5.1 并行度配置

```json
{
  "parallel_config": {
    "max_concurrent_agents": 4,
    "max_concurrent_per_type": {
      "orchestrator": 2,
      "executor": 4,
      "validator": 2,
      "debugger": 1
    },
    "resource_limits": {
      "max_total_tokens_per_wave": 2000000,
      "max_api_calls_per_minute": 60
    },
    "wave_strategy": "dependency_based"
  }
}
```

### 5.2 波次执行策略

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          波次执行模型                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Wave Analysis Algorithm:                                               │
│                                                                         │
│  1. 获取所有 pending 状态任务                                           │
│  2. 按依赖关系构建 DAG (有向无环图)                                      │
│  3. 拓扑排序确定执行顺序                                                │
│  4. 将无依赖任务分配到同一 Wave                                          │
│  5. 每个 Wave 内任务并行执行                                            │
│  6. Wave 间顺序执行                                                     │
│                                                                         │
│  Example:                                                               │
│                                                                         │
│  Wave 1 (并行度=4):                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ T1-GSD-1     │ │ T1-nonGSD-1  │ │ T2-GSD-1     │ │ T2-nonGSD-1  │   │
│  │ (executor-1) │ │ (executor-2) │ │ (executor-3) │ │ (executor-4) │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                                         │
│  Wave 2 (并行度=4):                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ T1-GSD-2     │ │ T1-nonGSD-2  │ │ T2-GSD-2     │ │ T2-nonGSD-2  │   │
│  │ (executor-1) │ │ (executor-2) │ │ (executor-3) │ │ (executor-4) │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                                         │
│  ...                                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3 动态并行度调整

```python
def calculate_parallel_capacity():
    """
    动态计算当前可用并行度
    """
    config = load_config()
    state = load_state()
    
    max_agents = config['max_concurrent_agents']
    active_count = len(state['active_agents'])
    
    available_slots = max_agents - active_count
    
    if available_slots <= 0:
        return 0
    
    token_budget = config['resource_limits']['max_total_tokens_per_wave']
    current_usage = sum(agent['token_usage'] for agent in state['active_agents'])
    
    if current_usage >= token_budget * 0.8:
        return max(1, available_slots // 2)
    
    return available_slots
```

### 5.4 资源竞争处理

| 场景 | 处理策略 |
|------|----------|
| Token预算不足 | 暂停新任务分配，等待当前任务完成 |
| API限流 | 实现指数退避重试，降低并行度 |
| 文件锁冲突 | 使用文件锁机制，顺序化文件写入 |
| 内存不足 | 减少并行Agent数量，分批执行 |

---

## 六、结果整合方法

### 6.1 数据汇总结构

```
.planning/experiment-results/
├── SUMMARY.json                    # 总体汇总
├── BY_TASK/                        # 按任务分组
│   ├── T1/
│   │   ├── GSD/
│   │   │   ├── run-1/
│   │   │   │   ├── STATUS.json
│   │   │   │   ├── METRICS.json
│   │   │   │   └── SCORES.json
│   │   │   ├── run-2/
│   │   │   └── run-3/
│   │   └── nonGSD/
│   │       └── ...
│   ├── T2/
│   └── ...
├── BY_SCENARIO/                    # 按场景分组
│   ├── code_development/
│   ├── data_analysis/
│   └── creative_generation/
├── BY_COMPLEXITY/                  # 按复杂度分组
│   ├── simple/
│   ├── medium/
│   └── complex/
└── AGGREGATED/                     # 聚合数据
    ├── efficiency_comparison.csv
    ├── quality_comparison.csv
    ├── process_comparison.csv
    └── user_experience_comparison.csv
```

### 6.2 汇总流程

```
┌─────────────────────────────────────────────────────────────────┐
│                       结果整合流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: 收集所有任务状态文件                                    │
│  │       glob: .planning/experiments/*/STATUS.json              │
│  │                                                              │
│  ▼                                                              │
│  Step 2: 验证数据完整性                                          │
│  │       - 检查必需字段                                          │
│  │       - 验证数值范围                                          │
│  │       - 标记异常数据                                          │
│  │                                                              │
│  ▼                                                              │
│  Step 3: 按维度分组                                              │
│  │       - 按任务 (T1-T9)                                        │
│  │       - 按场景 (代码/数据/创意)                               │
│  │       - 按复杂度 (简单/中等/复杂)                             │
│  │       - 按模式 (GSD/nonGSD)                                   │
│  │                                                              │
│  ▼                                                              │
│  Step 4: 计算统计量                                              │
│  │       - 均值、标准差、中位数                                  │
│  │       - GSD优势度                                             │
│  │       - 效应量 (Cohen's d)                                    │
│  │                                                              │
│  ▼                                                              │
│  Step 5: 生成汇总文件                                            │
│  │       - SUMMARY.json                                          │
│  │       - comparison_tables.csv                                 │
│  │                                                              │
│  ▼                                                              │
│  Step 6: 触发分析阶段                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 汇总数据格式

**SUMMARY.json**:
```json
{
  "experiment_id": "EXP-2026-04-14-001",
  "completed_at": "2026-04-20T18:00:00Z",
  "total_duration_hours": 120,
  "summary": {
    "total_experiments": 54,
    "successful": 52,
    "failed": 2,
    "success_rate": 96.3
  },
  "by_mode": {
    "GSD": {
      "avg_completion_time": 42.5,
      "avg_accuracy": 92.3,
      "avg_completeness": 8.7,
      "avg_satisfaction": 8.9,
      "total_token_usage": 12500000
    },
    "nonGSD": {
      "avg_completion_time": 58.2,
      "avg_accuracy": 78.5,
      "avg_completeness": 6.8,
      "avg_satisfaction": 7.2,
      "total_token_usage": 18200000
    }
  },
  "gsd_advantage": {
    "completion_time": -27.0,
    "accuracy": 17.6,
    "completeness": 27.9,
    "satisfaction": 23.6
  },
  "by_complexity": {
    "simple": {...},
    "medium": {...},
    "complex": {...}
  },
  "by_scenario": {
    "code_development": {...},
    "data_analysis": {...},
    "creative_generation": {...}
  },
  "statistical_tests": {
    "completion_time": {
      "test": "Mann-Whitney U",
      "p_value": 0.003,
      "significant": true,
      "cohens_d": 0.82
    }
  }
}
```

---

## 七、异常处理机制

### 7.1 异常类型分类

| 异常类型 | 严重程度 | 处理策略 |
|----------|----------|----------|
| 任务超时 | 中 | 自动重试(最多3次)，增加超时时间 |
| 资源耗尽 | 高 | 暂停新任务，等待资源释放 |
| 执行错误 | 中 | 触发调试Agent分析修复 |
| 数据异常 | 低 | 标记异常，继续执行 |
| Agent崩溃 | 高 | 重启Agent，恢复任务状态 |
| 通信失败 | 中 | 重试消息传递，检查文件锁 |

### 7.2 异常处理流程

```
┌─────────────────────────────────────────────────────────────────┐
│                       异常处理流程                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  异常检测                                                        │
│  │  - 监控任务状态更新                                           │
│  │  - 检测超时任务                                               │
│  │  - 分析错误报告消息                                           │
│  │                                                              │
│  ▼                                                              │
│  异常分类                                                        │
│  │  - 确定异常类型                                               │
│  │  - 评估严重程度                                               │
│  │  - 判断是否需要人工干预                                       │
│  │                                                              │
│  ▼                                                              │
│  ┌─────────────┬─────────────┬─────────────┐                    │
│  │   自动处理   │   调试修复   │   人工介入   │                    │
│  └──────┬──────┴──────┬──────┴──────┬──────┘                    │
│         │             │             │                           │
│         ▼             ▼             ▼                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                │
│  │ 重试任务    │ │ 激活调试    │ │ 暂停实验    │                │
│  │ 更新状态    │ │ Agent分析   │ │ 通知管理员  │                │
│  │ 记录日志    │ │ 修复方案    │ │ 等待决策    │                │
│  └─────────────┘ └─────────────┘ └─────────────┘                │
│         │             │             │                           │
│         └─────────────┴─────────────┘                           │
│                       │                                         │
│                       ▼                                         │
│              恢复执行/标记失败                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 调试Agent激活规则

```python
def should_activate_debugger(error_report):
    """
    判断是否需要激活调试Agent
    """
    conditions = [
        error_report['retry_count'] >= 2,
        error_report['error_type'] in ['execution_failure', 'logic_error'],
        error_report.get('requires_debugger', False),
        error_report['context']['token_usage'] > 150000
    ]
    
    return any(conditions)
```

### 7.4 断点续传机制

```json
{
  "checkpoint": {
    "experiment_id": "EXP-2026-04-14-001",
    "checkpoint_time": "2026-04-15T14:30:00Z",
    "completed_phases": ["preparation", "orchestration"],
    "completed_tasks": ["T1-GSD-1", "T1-nonGSD-1", "T2-GSD-1"],
    "running_tasks": ["T2-nonGSD-1"],
    "pending_tasks": [...],
    "state_snapshot": ".planning/checkpoints/CP-2026-04-15-14-30.json"
  }
}
```

恢复命令:
```bash
# 主控Agent启动时自动检测并恢复
gsd-experiment-supervisor --resume --checkpoint .planning/checkpoints/CP-2026-04-15-14-30.json
```

---

## 八、执行流程详细设计

### 8.1 阶段一：准备阶段

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 1: Preparation                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  任务列表:                                                       │
│  ├── P1-1: 环境配置检查                                         │
│  │   ├── 检查GSD环境可用性                                      │
│  │   ├── 检查非GSD环境可用性                                    │
│  │   └── 验证API连接                                            │
│  │                                                              │
│  ├── P1-2: 任务准备                                             │
│  │   ├── 创建实验目录结构                                       │
│  │   ├── 初始化状态文件                                         │
│  │   └── 准备输入资源                                           │
│  │                                                              │
│  └── P1-3: 评估工具准备                                         │
│      ├── 创建数据记录表格模板                                   │
│      ├── 配置计时工具                                           │
│      └── 准备评分标准文档                                       │
│                                                                 │
│  执行方式: 顺序执行                                              │
│  负责Agent: 主控Agent                                            │
│  输出: .planning/experiment-state.json (初始化)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 阶段二：编排阶段

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 2: Orchestration                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  任务列表:                                                       │
│  ├── P2-1: 解析实验设计文档                                     │
│  │   ├── 读取 zGSDExpierement.md                                │
│  │   ├── 提取任务定义                                           │
│  │   └── 提取评估指标                                           │
│  │                                                              │
│  ├── P2-2: 生成任务计划 (并行)                                  │
│  │   ├── 编排Agent-1: 生成 T1-T3 计划                           │
│  │   ├── 编排Agent-2: 生成 T4-T6 计划                           │
│  │   ├── 编排Agent-3: 生成 T7-T9 计划                           │
│  │   └── 并行度: 3                                              │
│  │                                                              │
│  └── P2-3: 创建任务队列                                         │
│      ├── 合并所有任务计划                                       │
│      ├── 生成任务队列文件                                       │
│      └── 初始化任务状态                                         │
│                                                                 │
│  执行方式: P2-1顺序 → P2-2并行 → P2-3顺序                       │
│  负责Agent: 主控Agent + 编排Agent池                              │
│  输出: .planning/experiments/*/PLAN.md, STEPS.md                 │
│        .planning/experiment-queue.json                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3 阶段三：执行阶段

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 3: Execution                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  任务列表: 54次实验 (9任务 × 3重复 × 2模式)                      │
│                                                                 │
│  执行策略: 波次并行执行                                          │
│                                                                 │
│  Wave 1 (并行度=4):                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│  │ executor-001   │ │ executor-002   │ │ executor-003   │ │ executor-004   │
│  │ T1-GSD-1       │ │ T1-nonGSD-1    │ │ T2-GSD-1       │ │ T2-nonGSD-1    │
│  └────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
│                                                                 │
│  Wave 2 (并行度=4):                                              │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│  │ executor-001   │ │ executor-002   │ │ executor-003   │ │ executor-004   │
│  │ T1-GSD-2       │ │ T1-nonGSD-2    │ │ T2-GSD-2       │ │ T2-nonGSD-2    │
│  └────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
│                                                                 │
│  ... (共14个Wave)                                               │
│                                                                 │
│  每次执行包含:                                                   │
│  ├── 读取任务计划                                               │
│  ├── 执行实验操作                                               │
│  ├── 记录过程数据                                               │
│  ├── 保存输出结果                                               │
│  └── 更新任务状态                                               │
│                                                                 │
│  异常处理:                                                       │
│  ├── 超时 → 重试(最多3次)                                       │
│  ├── 错误 → 触发调试Agent                                       │
│  └── 失败 → 标记并继续下一任务                                  │
│                                                                 │
│  输出: .planning/experiments/*/execution/*/LOG.md                │
│        .planning/experiments/*/execution/*/OUTPUT/               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.4 阶段四：验证阶段

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 4: Validation                          │
├─────────────────────────────────────────────────────────────────┤
│
│  任务列表:                                                       │
│  ├── V-1: 数据完整性检查                                        │
│  │   ├── 检查所有任务状态文件                                   │
│  │   ├── 验证必需字段完整性                                     │
│  │   └── 标记缺失数据                                           │
│  │                                                              │
│  ├── V-2: 指标评分汇总 (并行)                                   │
│  │   ├── 验证Agent-1: T1-T3 评分                                │
│  │   ├── 验证Agent-2: T4-T6 评分                                │
│  │   └── 验证Agent-3: T7-T9 评分                                │
│  │                                                              │
│  └── V-3: 异常数据标记                                          │
│      ├── 检测离群值                                             │
│      ├── 标记异常实验                                           │
│      └── 生成异常报告                                           │
│                                                                 │
│  执行方式: V-1顺序 → V-2并行 → V-3顺序                          │
│  负责Agent: 主控Agent + 验证Agent池                              │
│  输出: .planning/experiments/*/validation/*/REPORT.md            │
│        .planning/experiments/*/validation/*/SCORES.json          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.5 阶段五：分析阶段

```
┌─────────────────────────────────────────────────────────────────┐
│                    Phase 5: Analysis                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  任务列表:                                                       │
│  ├── A-1: 统计检验                                              │
│  │   ├── 执行t检验/Mann-Whitney U检验                           │
│  │   ├── 计算效应量                                             │
│  │   └── 生成显著性报告                                         │
│  │                                                              │
│  ├── A-2: 可视化生成                                            │
│  │   ├── 生成效率对比图                                         │
│  │   ├── 生成质量雷达图                                         │
│  │   ├── 生成场景-复杂度热力图                                  │
│  │   └── 生成相关性散点图                                       │
│  │                                                              │
│  └── A-3: 报告撰写                                              │
│      ├── 汇总对比分析                                           │
│      ├── 撰写优势边界分析                                       │
│      └── 生成最终报告                                           │
│                                                                 │
│  执行方式: A-1/A-2并行 → A-3顺序                                │
│  负责Agent: 主控Agent                                            │
│  输出: .planning/experiment-results/SUMMARY.json                 │
│        .planning/experiment-results/visualizations/              │
│        .planning/experiment-results/FINAL_REPORT.md              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 九、Agent启动脚本

### 9.1 主控Agent启动脚本

**文件**: `.planning/scripts/start-supervisor.md`

```markdown
# GSD实验主控Agent启动指令

## 上下文加载

1. 读取实验设计文档: zGSDExpierement.md
2. 读取执行方案: zGSDExecutionPlan.md
3. 检查状态文件: .planning/experiment-state.json

## 启动检查

- [ ] 检查目录结构是否存在
- [ ] 检查配置文件是否完整
- [ ] 验证Agent池可用性

## 执行流程

按照 zGSDExecutionPlan.md 中定义的阶段顺序执行:

1. Phase 1: Preparation
2. Phase 2: Orchestration  
3. Phase 3: Execution
4. Phase 4: Validation
5. Phase 5: Analysis

## 状态报告

每完成一个阶段，更新 experiment-state.json 并生成进度报告。
```

### 9.2 编排Agent任务模板

**文件**: `.planning/templates/orchestrator-task.md`

```markdown
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
```

### 9.3 执行Agent任务模板

**文件**: `.planning/templates/executor-task.md`

```markdown
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
```

### 9.4 验证Agent任务模板

**文件**: `.planning/templates/validator-task.md`

```markdown
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
```

---

## 十、目录结构初始化

### 10.1 完整目录结构

```
.planning/
├── experiment-state.json           # 全局状态
├── experiment-queue.json           # 任务队列
├── experiment-results/             # 结果汇总
│   ├── SUMMARY.json
│   ├── BY_TASK/
│   ├── BY_SCENARIO/
│   ├── BY_COMPLEXITY/
│   └── AGGREGATED/
├── experiments/                    # 实验数据
│   ├── T1-GSD-1/
│   │   ├── PLAN.md
│   │   ├── STEPS.md
│   │   ├── STATUS.json
│   │   ├── execution/
│   │   │   └── run-1/
│   │   │       ├── LOG.md
│   │   │       ├── METRICS.json
│   │   │       └── OUTPUT/
│   │   ├── validation/
│   │   │   └── run-1/
│   │   │       ├── REPORT.md
│   │   │       └── SCORES.json
│   │   └── debug/
│   │       └── {debug_id}/
│   │           ├── ANALYSIS.md
│   │           └── FIX.md
│   ├── T1-nonGSD-1/
│   └── ...
├── messages/                       # Agent通信
│   ├── supervisor/
│   │   ├── status-update.json
│   │   ├── completion.json
│   │   └── error-report.json
│   ├── executor-001/
│   │   └── assignment.json
│   └── ...
├── checkpoints/                    # 断点快照
│   └── CP-{timestamp}.json
├── templates/                      # 任务模板
│   ├── orchestrator-task.md
│   ├── executor-task.md
│   └── validator-task.md
└── scripts/                        # 启动脚本
    ├── start-supervisor.md
    └── init-directories.sh
```

### 10.2 初始化脚本

**文件**: `.planning/scripts/init-directories.sh`

```bash
#!/bin/bash

# GSD实验目录初始化脚本

BASE_DIR=".planning"

# 创建基础目录
mkdir -p "$BASE_DIR/experiment-results"/{BY_TASK,BY_SCENARIO,BY_COMPLEXITY,AGGREGATED}
mkdir -p "$BASE_DIR/experiments"
mkdir -p "$BASE_DIR/messages"/{supervisor}
mkdir -p "$BASE_DIR/checkpoints"
mkdir -p "$BASE_DIR/templates"
mkdir -p "$BASE_DIR/scripts"

# 初始化状态文件
cat > "$BASE_DIR/experiment-state.json" << 'EOF'
{
  "experiment_id": "EXP-2026-04-14-001",
  "status": "initialized",
  "started_at": null,
  "updated_at": null,
  "config": {
    "total_tasks": 9,
    "repeats": 3,
    "modes": ["GSD", "non-GSD"],
    "parallel_limit": 4
  },
  "progress": {
    "total_experiments": 54,
    "completed": 0,
    "running": 0,
    "pending": 54,
    "failed": 0
  },
  "current_phase": "preparation",
  "active_agents": [],
  "checkpoints": []
}
EOF

# 初始化任务队列
cat > "$BASE_DIR/experiment-queue.json" << 'EOF'
{
  "queue_id": "QUEUE-001",
  "created_at": null,
  "tasks": [],
  "completed_tasks": [],
  "failed_tasks": []
}
EOF

echo "GSD实验目录初始化完成"
```

---

## 十一、执行检查清单

### 11.1 启动前检查

```markdown
## 环境检查
- [ ] GSD环境已安装并可用
- [ ] 非GSD环境已配置
- [ ] API连接正常
- [ ] 磁盘空间充足 (>10GB)

## 文件检查
- [ ] zGSDExpierement.md 存在
- [ ] zGSDExecutionPlan.md 存在
- [ ] 目录结构已初始化

## 配置检查
- [ ] 并行度配置合理
- [ ] 资源限制已设置
- [ ] 超时参数已配置

## Agent检查
- [ ] 主控Agent可用
- [ ] 编排Agent池就绪
- [ ] 执行Agent池就绪
- [ ] 验证Agent池就绪
- [ ] 调试Agent可用
```

### 11.2 阶段完成检查

```markdown
## Phase 1: Preparation
- [ ] 环境配置完成
- [ ] 任务准备完成
- [ ] 评估工具准备完成

## Phase 2: Orchestration
- [ ] 所有PLAN.md已生成
- [ ] 所有STEPS.md已生成
- [ ] 任务队列已创建

## Phase 3: Execution
- [ ] 所有实验已执行
- [ ] 所有LOG.md已生成
- [ ] 所有输出已保存

## Phase 4: Validation
- [ ] 所有REPORT.md已生成
- [ ] 所有SCORES.json已生成
- [ ] 异常数据已标记

## Phase 5: Analysis
- [ ] 统计检验已完成
- [ ] 可视化已生成
- [ ] 最终报告已生成
```

---

## 十二、文档信息

| 项目 | 内容 |
|------|------|
| 文档版本 | v1.0 |
| 创建日期 | 2026-04-14 |
| 最后更新 | 2026-04-14 |
| 关联文档 | zGSDExpierement.md |
| 文档状态 | 待执行 |

---

*本执行方案设计为GSD实验的多Agent协作执行提供完整的技术规范与操作指南。*
