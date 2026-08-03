---
name: task-planning
description: 任务规划 Skill。把老板或人类输入转化为可执行目标、子任务、执行 Agent、验收标准，并自动编排多 Agent 协作流程。所有 Agent 都应继承此能力。
---

# task-planning · 任务规划

把模糊的人类输入或高层目标，拆解为清晰的 AI 可执行计划。是 AI 电商公司的"总调度台"。

## 用途

- 将自然语言需求转换为结构化任务清单
- 为每个子任务匹配最合适的 Agent / Skill
- 定义验收标准（输出格式、成功指标、截止时间）
- 在必要时启动并行 Subagent 协作
- 生成可追踪的执行计划，供 task-followup 监控

## 触发场景

- 老板说"找一个适合美国市场的宠物产品"
- 用户要求"帮我做一份 Q4 增长方案"
- 复杂任务需要多个专业 Agent 协作
- 子任务边界不清，需要先规划再执行

## 输入

- 原始需求（自然语言）
- 目标市场、预算、时间约束（可选）
- 可用 Agent / Skill 列表
- 历史任务 / Memory（可选）

## 输出

```yaml
任务:
  目标: "string"
  子任务:
    - 编号: 1
      名称: "string"
      描述: "string"
      负责 Agent: "string"
      调用 Skill: "string"
      输入: {}
      输出: {}
      验收标准: "string"
      依赖: [0]
  执行策略: "并行|串行|混合"
  整体验收标准: "string"
```

## 工作流

1. **意图识别**：提取目标、约束、优先级。
2. **任务拆解**：按 MECE 原则拆成 3-7 个可执行子任务。
3. **Agent 匹配**：根据子任务类型匹配 market-agent、product-agent、sourcing-agent、finance-agent 等。
4. **依赖排序**：确定哪些子任务可并行，哪些有先后依赖。
5. **生成计划**：输出结构化任务清单，包含验收标准。
6. **调度执行**：按策略启动 Subagent 或等待人类确认。

## 调用关系

**被调用**：CEO Agent、人类用户、任意复杂任务入口

**调用**：
- market-research
- competitor-analysis
- product-selection
- supplier-search
- profitability-analysis
- 其他专业 Agent / Skill

## 依赖工具 / Memory

- Memory: 历史任务计划、失败案例、最佳实践
- Tool: 飞书任务 / 日历（可选，用于同步任务）

## 边界与限制

- 只做规划，不直接执行市场搜索或采购谈判
- 复杂计划需人类确认后再调度
- 不对不可量化的目标做硬性承诺

## 示例

输入：
> 找一个适合美国市场的宠物产品

输出：
```yaml
任务:
  目标: 在美国市场找到 1-3 个高潜力宠物产品，完成可行性评估
  子任务:
    - 编号: 1
      名称: 市场趋势扫描
      负责 Agent: market-agent
      调用 Skill: market-research
      输出: 宠物品类趋势 Top 10
      验收标准: 提供 Google Trends / Amazon Best Seller / TikTok 三方数据
    - 编号: 2
      名称: 竞品分析
      负责 Agent: market-agent
      调用 Skill: competitor-analysis
      依赖: [1]
      输出: 3-5 个核心竞品 ASIN 分析报告
    - 编号: 3
      名称: 选品评分
      负责 Agent: product-agent
      调用 Skill: product-selection
      依赖: [1, 2]
      输出: 选品评分表
    - 编号: 4
      名称: 供应链初筛
      负责 Agent: sourcing-agent
      调用 Skill: supplier-search
      依赖: [3]
      输出: 2-3 家候选供应商
    - 编号: 5
      名称: 利润测算
      负责 Agent: finance-agent
      调用 Skill: profitability-analysis
      依赖: [2, 4]
      输出: SKU 级利润预测
  执行策略: 混合
  整体验收标准: 72 小时内输出可落地的选品决策建议
```
