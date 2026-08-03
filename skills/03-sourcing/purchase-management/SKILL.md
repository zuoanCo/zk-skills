---
name: purchase-management
description: 连接 Odoo Purchase，创建采购草稿、跟踪采购进度、管理供应商交期，确保采购流程可控。
---

# purchase-management · 采购管理

## 用途
- 在 Odoo 中创建采购草稿
- 跟踪采购订单状态
- 监控供应商交期
- 预警采购异常

## 触发场景
- 补货决策确认后
- 需要创建采购单
- 交期延迟需要跟进
- 采购对账

## 输入
- 采购需求（SKU、数量、目标交期）
- 供应商信息
- 报价单
- Odoo Purchase 配置

## 输出
```markdown
## 采购管理报告

### 采购草稿
### PO 跟踪
### 交期状态
### 异常预警
### 对账建议
```

## 工作流
1. **接收采购需求**：来自 replenishment 或人工
2. **选择供应商**：基于 evaluation 结果
3. **创建采购草稿**：在 Odoo Purchase 生成 PO
4. **人工确认**：采购人员审核后发送
5. **跟踪进度**：交期、生产、质检、出货
6. **异常处理**：延迟、质量问题升级

## 调用关系
**被调用**：replenishment、inventory-analysis

**调用**：odoo-integration、supplier-evaluation

## 依赖工具 / Memory
- Tool: Odoo Purchase API
- Memory: 采购历史、供应商交期记录

## 边界与限制
- 只创建草稿状态 PO，不自动确认
- 付款、合同签署需人工处理
- 不越权修改已确认订单

## 示例
输出：为 WP-001 创建 PO 草稿，数量 500，供应商工厂 B，目标交期 25 天
