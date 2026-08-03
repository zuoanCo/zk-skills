---
name: ebay-operation
description: 负责 eBay 店铺运营，包括 Listing 优化、定价、促销和卖家绩效维护。
---

# ebay-operation · eBay 运营

## 用途
- 优化 eBay Listing
- 管理 eBay 定价和促销
- 维护卖家等级
- 分析 eBay 销售和流量

## 触发场景
- eBay 新品上架
- 销量下滑
- 卖家绩效预警
- 平台政策变化

## 输入
- 产品信息
- eBay 后台数据
- 竞品数据
- 平台政策

## 输出
```markdown
## eBay 运营方案

### Listing 优化
### 定价策略
### 促销计划
### 卖家绩效维护
### 风险预警
```

## 工作流
1. **店铺诊断**：销售额、流量、转化率、卖家等级
2. **Listing 优化**：标题、Item Specifics、图片
3. **定价策略**：拍卖、一口价、Best Offer
4. **促销工具**：Markdown、Promoted Listings
5. **绩效维护**：物流时效、退货率、纠纷率
6. **输出方案**：可执行优化清单

## 调用关系
**被调用**：channel-operation-agent

**调用**：listing-writing、pricing-strategy、advertising-analysis

## 依赖工具 / Memory
- Tool: eBay Seller Hub
- Memory: eBay 政策、高转化 Listing 案例

## 边界与限制
- 不直接修改 eBay 后台
- 账户安全操作需人工处理
- 遵守 eBay 政策

## 示例
输出：建议标题加入品牌词 + 核心功能词，开通 Promoted Listings Standard，目标 ROAS 4.0
