---
name: knowledge-management
description: 知识管理 Skill。负责保存岗位经验、提取规律、更新知识库，让 Agent 能力随执行持续进化。
---

# knowledge-management · 知识管理

把一次性的任务执行，变成可复用的组织知识。

## 用途

- 保存任务执行中的关键经验
- 提取成功 / 失败模式
- 更新知识库和 SOP
- 为后续 Agent 提供上下文
- 沉淀供应商、产品、市场等领域知识

## 触发场景

- 任务完成后复盘
- 发现新的市场规律或最佳实践
- 遇到失败案例需要记录
- 知识体系需要更新

## 输入

- 任务结果
- 执行过程日志
- 成功 / 失败标记
- 相关上下文

## 输出

- 知识条目（Markdown / YAML）
- 更新后的知识库索引
- 推荐的 SOP 改进点

## 工作流

1. **收集案例**：从任务日志中提取关键事件。
2. **提取规律**：归纳成功因素、失败原因、常见陷阱。
3. **结构化存储**：按领域、场景、类型分类。
4. **更新索引**：维护可检索的知识目录。
5. **反哺 Skill**：将新知识写入 Memory 或 references。
6. **推荐 SOP**：识别可固化的流程。

## 知识条目格式

```markdown
---
type: 经验 | 案例 | 规则 | 模板
domain: market | product | sourcing | logistics | customer
author: agent-name
created: 2026-08-03
---

## 场景
## 现象
## 原因
## 行动
## 结果
## 可复用建议
```

## 调用关系

**被调用**：任意 Agent 任务完成后、skill-improvement

**调用**：memory-manager、SOP-generation

## 依赖工具 / Memory

- Memory: 全量岗位经验库
- Tool: 飞书知识库 / 本地知识库

## 边界与限制

- 不保存敏感信息或未经确认的数据
- 知识条目需要定期清理和验证
- 不替代人类对重要知识的最终判断

## 示例

输入：某次广告投放失败，CPC 暴涨 3 倍
输出：知识条目 "高价竞品词陷阱"，建议优化 keyword-optimization 的否定词策略
