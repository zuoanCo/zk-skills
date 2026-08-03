---
name: shopify-operation
description: 负责 Shopify 商品管理、活动策划、转化优化和独立站增长策略。
---

# shopify-operation · 独立站运营

## 用途
- 管理 Shopify 商品上架和页面
- 策划促销活动
- 优化转化率
- 分析独立站流量和销售

## 触发场景
- Shopify 新品上架
- 独立站转化率低
- 策划营销活动
- 分析独立站数据

## 输入
- 产品信息
- Shopify 后台数据
- 流量数据（Google Analytics）
- 广告数据
- 用户行为数据

## 输出
```markdown
## Shopify 运营方案

### 商品策略
### 页面优化建议
### 营销活动计划
### 转化优化建议
### 数据分析
```

## 工作流
1. **店铺诊断**：流量、转化、客单价
2. **商品优化**：标题、描述、图片、价格
3. **页面优化**：首页、类目页、详情页
4. **活动策划**：折扣、捆绑、邮件营销
5. **广告投放**：Google、Meta、TikTok
6. **数据复盘**：转化率、ROAS、LTV

## 调用关系
**被调用**：channel-operation-agent

**调用**：listing-writing、advertising-analysis、conversion-analysis

## 依赖工具 / Memory
- Tool: Shopify Admin、Google Analytics
- Memory: 独立站最佳实践、高转化页面

## 边界与限制
- 不直接修改 Shopify 后台
- 支付、退款等敏感操作需人工确认
- 品牌视觉需符合规范

## 示例
输出：建议首页增加信任徽章、产品页加入视频、设置弃购邮件挽回，预计转化率提升 15%
