---
name: amazon-operation
description: Amazon 运营 Skill。负责 Listing 优化、广告分析、关键词监控、排名跟踪等 Amazon 渠道运营工作。
---

# amazon-operation · Amazon 运营

在亚马逊上把产品卖好。

## 用途

- Listing 优化建议（标题、五点、A+、图片）
- 广告数据分析和优化建议
- 关键词排名跟踪
- BSR / 销量监控
- 平台政策合规检查
- 竞品动态跟踪

## 触发场景

- 新品上架前准备 Listing
- 老品销量下滑需要诊断
- 广告 ACOS 过高需要优化
- 关键词排名下降
- 需要制定 Amazon 增长策略

## 输入

- ASIN
- Listing 当前内容
- 广告报告（Search Term Report、Campaign Report）
- 销售数据
- 竞品 ASIN
- 关键词列表

## 输出

```markdown
## Amazon 运营诊断：{ASIN}

### Listing 健康度
- 标题、五点、描述、A+、图片评分
- 优化建议

### 关键词表现
| 关键词 | 排名 | 搜索量 | 建议 |

### 广告表现
- ACOS / TACOS
- 高 spend 低转化词
- 建议优化动作

### 竞品对比
### 行动计划
```

## 工作流

1. **Listing 诊断**：标题、五点、图片、A+、价格、评论。
2. **关键词分析**：流量词、转化词、排名、搜索量。
3. **广告诊断**：ACOS、TACOS、 spend 分布、否定词机会。
4. **竞品监控**：价格、促销、评论、关键词动作。
5. **输出优化建议**：可执行的 Listing 和广告优化清单。

## 调用关系

**被调用**：task-planning、channel-operation-agent

**调用**：listing-writing、seo-keyword、advertising-analysis、competitor-analysis、review-management

## 依赖工具 / Memory

- Tool: Amazon Seller Central、Amazon SP API（如接入）
- Memory: 历史广告优化效果、关键词排名曲线

## 边界与限制

- 只输出建议，不直接修改 Seller Central
- 不操控评论或进行平台违规操作
- 广告优化需人类确认预算调整

## 示例

输入：ASIN B08XXXX，ACOS 45%，销量下滑 20%
输出：标题埋词不足、主图点击率低于类目平均、建议加视频、否定 12 个高 spend 词、预算向 3 个高转化词倾斜
