---
name: ecommerce-api
description: 连接 Amazon SP API、Shopify API、TikTok API 等电商平台接口，实现数据拉取和基础操作。
---

# ecommerce-api · 电商 API

## 用途
- 连接电商平台 API
- 拉取订单、库存、广告数据
- 执行基础写操作（如更新库存）
- 为多平台同步提供数据基础

## 触发场景
- 需要同步平台数据
- 开发自动化流程
- 对接新平台
- 数据分析和报表

## 输入
- API 凭证
- 目标平台
- 操作类型
- 查询条件

## 输出
```markdown
## 电商 API 操作结果

### 平台
### 操作
### 记录数
### 状态
### 错误信息
### 下一步
```

## 工作流
1. **认证连接**：OAuth 或 API key
2. **读取数据**：订单、库存、产品、广告
3. **数据转换**：统一字段格式
4. **写回操作**：库存更新、价格更新（需确认）
5. **错误处理**：限流、重试、告警
6. **日志记录**：便于审计

## 调用关系
**被调用**：marketplace-sync、fulfillment-management、advertising-analysis

**调用**：odoo-integration、feishu-automation

## 依赖工具 / Memory
- Tool: 各平台 API SDK
- Memory: API 字段映射、限流规则

## 边界与限制
- API 凭证安全存储
- 写操作需人工确认或严格规则
- 遵守平台 API 政策

## 示例
输出：通过 Amazon SP API 拉取过去 30 天 1,200 条订单，同步至 Odoo Sales
