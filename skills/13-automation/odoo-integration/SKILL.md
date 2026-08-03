---
name: odoo-integration
description: Odoo 连接 Skill。连接 Odoo 的 Product、Sales、Purchase、Inventory、Accounting 模块，实现数据读取、凭证草稿创建和流程同步。
---

# odoo-integration · Odoo 连接

让 AI 电商系统和 Odoo ERP 数据互通。

## 用途

- 读取 Odoo Product 产品数据
- 读取 Sales 订单数据
- 读取 Purchase 采购数据
- 读取 Inventory 库存数据
- 读取 Accounting 财务数据
- 创建采购草稿、凭证草稿
- 同步电商平台订单到 Odoo

## 触发场景

- 库存分析需要 Odoo Inventory 数据
- 利润分析需要 Odoo Sales / Accounting 数据
- 采购流程需要在 Odoo 创建草稿
- 订单履约需要同步到 Odoo
- 财务对账需要 Odoo 账目

## 输入

- Odoo 连接配置（URL、DB、用户名、API key）
- 目标模型（product.template、sale.order、purchase.order、stock.quant、account.move 等）
- 操作类型（读取 / 创建 / 更新）
- 查询条件或数据载荷

## 输出

```markdown
## Odoo 操作结果

### 操作类型
### 影响模型
### 记录数
### 关键字段
### 状态
### 错误信息（如有）
```

## 支持模块

| 模块 | 能力 |
|------|------|
| Product | 读取产品信息、变体、价格 |
| Sales | 读取订单、客户、发票 |
| Purchase | 读取 / 创建采购草稿、询价单 |
| Inventory | 读取库存、库位、在途、调拨 |
| Accounting | 读取账目、创建凭证草稿 |

## 工作流

1. **验证连接**：检查 Odoo 服务可用性和权限。
2. **读取数据**：按条件查询目标模型。
3. **数据转换**：将 Odoo 数据转换为 Skill 所需格式。
4. **业务处理**：库存分析、利润计算、采购建议等。
5. **写回草稿**：需要人类确认后，创建采购单 / 凭证草稿。
6. **错误处理**：记录异常，重试或人工介入。

## 调用关系

**被调用**：inventory-analysis、profitability-analysis、purchase-management、accounting-assistant、workflow-automation

**调用**：ecommerce-api（同步订单）、feishu-automation（通知）

## 依赖工具 / Memory

- Tool: Odoo XML-RPC / JSON-RPC API
- Memory: Odoo 字段映射、同步规则、错误处理记录

## 安全与边界

- API key 绝不写入 Skill 文件，使用环境变量
- 只创建"草稿"状态记录，不自动确认
- 写操作需日志记录，便于审计
- 不删除 Odoo 数据

## 示例

输入：读取过去 30 天销售订单
输出：100 条订单记录，总金额 $X，按 SKU 汇总

输入：创建采购草稿
输出：在 Odoo Purchase 生成草稿 PO #P00045，等待采购确认
