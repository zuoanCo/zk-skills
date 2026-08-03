---
name: walmart-operation
description: 负责 Walmart Marketplace 店铺运营，包括 Listing、广告、定价和绩效维护。
---

# walmart-operation · 沃尔玛运营

## 用途
- 管理 Walmart Listing
- 优化 Walmart 广告
- 制定定价策略
- 维护卖家绩效

## 触发场景
- Walmart 新品上架
- 广告 ACOS 优化
- 价格竞争力下降
- 绩效预警

## 输入
- 产品信息
- Walmart Seller Center 数据
- 竞品价格
- 广告报告

## 输出
```markdown
## Walmart 运营方案

### Listing 优化
### 广告优化
### 定价建议
### 绩效维护
### 增长机会
```

## 工作流
1. **店铺诊断**：销售额、Buy Box 占有率、退货率
2. **Listing 优化**：标题、描述、属性、图片
3. **广告优化**：Sponsored Products 关键词和出价
4. **定价策略**：Repricer 规则
5. **库存管理**：防止断货影响绩效
6. **输出方案**：优化清单

## 调用关系
**被调用**：channel-operation-agent

**调用**：listing-writing、seo-keyword、advertising-analysis

## 依赖工具 / Memory
- Tool: Walmart Seller Center
- Memory: Walmart 政策、竞品数据

## 边界与限制
- 不直接修改 Seller Center
- 价格调整需考虑利润
- 遵守 Walmart 绩效标准

## 示例
输出：建议优化 Item Specs 完整度至 95%，开启自动广告获取搜索词，设置有竞争力的 Repricer 规则
