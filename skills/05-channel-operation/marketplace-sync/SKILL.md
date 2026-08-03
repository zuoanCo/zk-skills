---
name: marketplace-sync
description: 负责 Amazon、Shopify、TikTok、eBay、Walmart 与 Odoo 之间的数据同步，确保库存、价格、订单一致。
---

# marketplace-sync · 多平台同步

## 用途
- 同步多平台库存
- 同步价格和促销
- 同步订单到 Odoo
- 处理平台间冲突

## 触发场景
- 新品多平台上架
- 库存变动需要同步
- 价格调整需要多平台更新
- 订单需要回传 Odoo

## 输入
- 各平台 API 数据
- Odoo 数据
- 同步规则
- 冲突处理策略

## 输出
```markdown
## 多平台同步报告

### 同步状态
### 库存差异
### 价格差异
### 订单同步
### 异常处理
```

## 工作流
1. **建立映射**：SKU、仓库、价格、订单状态
2. **库存同步**：以 Odoo 为准，定时推送各平台
3. **价格同步**：按平台策略差异化定价
4. **订单同步**：拉取订单到 Odoo Sales
5. **异常处理**：超卖、价格冲突、SKU 缺失
6. **监控告警**：同步失败通知

## 调用关系
**被调用**：workflow-automation、inventory-analysis

**调用**：odoo-integration、ecommerce-api、feishu-automation

## 依赖工具 / Memory
- Tool: 各平台 API、Odoo API
- Memory: SKU 映射表、同步规则

## 边界与限制
- 不自动修改敏感数据
- 同步前需测试
- 重大价格调整需人工确认

## 示例
输出：检测到 Amazon 库存 320 与 Shopify 库存 300 不一致，建议以 Odoo 可用库存 275 为准统一更新
