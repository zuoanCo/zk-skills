---
name: business-dashboard
description: 构建 GMV、利润、库存、广告等核心指标的经营看板，支持管理层决策。
---

# business-dashboard · 经营看板

## 用途
- 整合多数据源
- 构建核心指标看板
- 支持实时监控
- 发现业务异常和机会

## 触发场景
- 管理层需要业务概览
- 每日经营晨会
- 需要构建 BI 看板
- 指标体系梳理

## 输入
- 销售数据
- 广告数据
- 库存数据
- 财务数据
- 用户数据

## 输出
```markdown
## 经营看板方案

### 核心 KPI
### 指标定义
### 数据源
### 刷新频率
### 可视化设计
### 告警规则
```

## 工作流
1. **确定指标**：GMV、利润、库存周转、ROAS
2. **梳理数据源**：Odoo、Amazon、Shopify、广告平台
3. **设计看板**：汇总、趋势、对比、明细
4. **数据建模**：ETL、维度、指标计算
5. **可视化实现**：图表、筛选、下钻
6. **告警配置**：异常阈值、推送渠道

## 调用关系
**被调用**：CEO Agent、report-generation

**调用**：data-analysis、odoo-integration、ecommerce-api

## 依赖工具 / Memory
- Tool: BI 工具（Metabase/Superset/Tableau）、Python
- Memory: 指标定义、历史基线

## 边界与限制
- 看板数据质量取决于数据源
- 不替代深度分析
- 实时性受 ETL 频率限制

## 示例
输出：设计 4 个看板（销售、广告、库存、财务），32 个核心指标，每日 8 点自动推送飞书
