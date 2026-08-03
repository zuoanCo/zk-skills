---
name: advertising-analysis
description: 广告分析 Skill。分析 Amazon PPC、Google Ads、Meta、TikTok 等平台的广告数据，输出 ACOS、ROAS、CTR、CVR 等指标的诊断和优化建议。
---

# advertising-analysis · 广告分析

让每一分广告费都花得更值。

## 用途

- 分析广告投放效果
- 诊断 ACOS / ROAS / CTR / CVR 异常
- 识别高 spend 低转化词 / 素材
- 输出预算和出价优化建议
- 支持 Amazon PPC、Google Ads、Meta、TikTok

## 触发场景

- 每周 / 每月广告复盘
- ACOS 飙升或 ROAS 下降
- 新品广告投放后需要诊断
- 大促前后广告策略调整

## 输入

- 广告平台报告
- 销售数据
- 广告目标（ACOS 目标 / ROAS 目标）
- 预算约束
- 关键词 / 素材列表

## 输出

```markdown
## 广告分析报告：{平台}

### 核心指标
- Spend
- Sales
- ACOS / ROAS
- CTR
- CVR
- CPC / CPM

### 分 Campaign 表现
| Campaign | Spend | Sales | ACOS | ROAS | 建议 |

### 关键词 / 受众诊断
### 素材表现
### 优化建议
```

## 分析维度

- **ACOS / TACOS**：广告花费占销售额比例
- **ROAS**：广告回报
- **CTR**：素材吸引力
- **CVR**：落地页 / 选品匹配度
- **CPC**：竞争程度
- **Search Term**：高 spend、高转化、高点击无转化

## 工作流

1. **数据清洗**：统一字段、处理异常值。
2. **核心指标计算**：ACOS、ROAS、CTR、CVR。
3. **分层分析**：Campaign / Ad Group / Keyword / 素材。
4. **异常识别**：高 spend 低转化、ACOS 超标、CTR 暴跌。
5. **输出建议**：预算迁移、出价调整、否定词、素材优化。

## 调用关系

**被调用**：task-planning、amazon-operation、campaign-management

**调用**：seo-keyword、conversion-analysis、creative-testing

## 依赖工具 / Memory

- Tool: 广告平台 API 或报告导出
- Memory: 历史广告优化效果、行业基准

## 边界与限制

- 只输出建议，不直接修改广告账户
- 重大预算调整需人类确认
- 归因窗口和平台差异需标注

## 示例

输入：Amazon PPC 30 天报告，ACOS 45%
输出：3 个 Campaign ACOS 超标，12 个词需否定，2 个高转化词建议加预算，预计可降至 28%
