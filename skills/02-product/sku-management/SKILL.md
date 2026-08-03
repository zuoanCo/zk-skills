---
name: sku-management
description: 负责 SKU 规划、规格设计、包装组合，连接 Odoo Product，确保产品数据一致性和可扩展性。
---

# sku-management · SKU 管理

## 用途
- 规划 SKU 结构和变体
- 设计规格、颜色、尺寸等属性
- 管理包装组合和套装
- 同步 Odoo Product 数据

## 触发场景
- 新品开发需要规划 SKU
- 多平台销售需要统一 SKU
- 产品变体过多需要优化
- 库存混乱需要梳理

## 输入
- 产品基础信息
- 市场需求和竞品变体
- 供应链能力
- 平台属性要求

## 输出
```markdown
## SKU 规划方案

### SKU 编码规则
### 主 SKU 与变体
### 规格矩阵
### 包装组合
### 多平台映射
### Odoo 同步计划
```

## 工作流
1. **确定 SKU 层级**：单品 / 变体 / 套装
2. **设计编码规则**：类目-材质-容量-颜色
3. **规划变体矩阵**：避免过度 SKU
4. **设计包装组合**：单件 / 多件 / 滤芯套装
5. **同步 Odoo**：创建或更新 product.template
6. **维护映射表**：Amazon / Shopify / TikTok SKU 对应

## 调用关系
**被调用**：product-selection、marketplace-sync

**调用**：odoo-integration、product-positioning

## 依赖工具 / Memory
- Tool: Odoo Product API
- Memory: SKU 编码规范、历史变体表现

## 边界与限制
- 不直接修改 Odoo 生产数据，只生成草稿
- SKU 数量需平衡覆盖度和库存风险
- 变体命名需符合平台规则

## 示例
输出：WP-001-S（不锈钢 2.5L 标准版）、WP-001-S-6F（含半年滤芯套装），并生成 Odoo product.template 草稿
