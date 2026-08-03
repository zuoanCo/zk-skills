---
name: skill-improvement
description: 分析任务失败原因和 Skill 使用效果，提出 Skill 改进方案，驱动 Agent 能力进化。
---

# skill-improvement · 自我优化

## 用途
- 分析 Skill 执行失败原因
- 评估 Skill 效果
- 提出改进建议
- 推动 Skill 迭代

## 触发场景
- 任务频繁失败
- Skill 效果不佳
- 定期 Skill 复盘
- 用户反馈 Skill 问题

## 输入
- Skill 执行日志
- 任务结果
- 用户反馈
- 成功率数据

## 输出
```markdown
## Skill 改进报告

### Skill 名称
### 问题描述
### 失败原因分析
### 改进建议
### 优先级
### 验证方案
```

## 工作流
1. **收集反馈**：失败案例、用户反馈、效果数据
2. **根因分析**：提示词、边界、依赖、数据
3. **提出改进**：修改 Skill、增加示例、优化流程
4. **优先级排序**：影响范围、成本、收益
5. **验证测试**：小范围测试改进效果
6. **发布更新**：更新 SKILL.md 和相关文件

## 调用关系
**被调用**：knowledge-management、CEO Agent

**调用**：memory-manager、knowledge-curator

## 依赖工具 / Memory
- Tool: 日志分析、版本控制
- Memory: Skill 历史版本、改进记录

## 边界与限制
- 不擅自修改生产环境 Skill
- 改进需测试验证
- 重大变更需人工确认

## 示例
输出：advertising-analysis 对 Amazon SB 广告支持不足，建议新增 Sponsored Brands 报告解析模块
