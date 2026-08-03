# AI 跨境电商 Skill 总目录

本仓库按 **AI 原生跨境电商公司** 组织架构设计 Skill 体系：

- **Agent = 岗位**
- **Skill = 岗位技能模块**
- **Tool = 外部能力**（Odoo、飞书、电商平台、浏览器、API）
- **Memory = 岗位经验**
- **Workflow = SOP 流程**

不设计"大而全电商 Agent"，而是拆成专业 Skill，由多个 Subagent 协作完成复杂任务。

## 设计原则

1. **专业化拆分**：每个 Skill 聚焦一个岗位能力
2. **可组合调用**：通过 task-planning 编排多 Agent 协作
3. **明确边界**：每个 Skill 说明输入、输出、依赖、边界
4. **安全第一**：API key、敏感操作绝不自动执行
5. **先建骨架再扩展**：第一阶段聚焦 15 个核心 Skill，跑通闭环后再扩展

---

## 第一阶段 · 核心 15 Skill（已创建）

这 15 个 Skill 足够跑通：**选品 → 采购 → 上架 → 销售 → 库存 → 客服 → 利润分析** 完整 AI 电商闭环。

| 编号 | Skill | 路径 | 负责岗位 |
|------|-------|------|---------|
| 1 | [task-planning](./skills/00-core/task-planning) | `00-core/task-planning` | 总调度 |
| 2 | [market-research](./skills/01-market-intelligence/market-research) | `01-market-intelligence/market-research` | 市场研究 |
| 3 | [competitor-analysis](./skills/01-market-intelligence/competitor-analysis) | `01-market-intelligence/competitor-analysis` | 市场研究 |
| 4 | [product-selection](./skills/02-product/product-selection) | `02-product/product-selection` | 产品 |
| 5 | [supplier-search](./skills/03-sourcing/supplier-search) | `03-sourcing/supplier-search` | 采购 |
| 6 | [quotation-analysis](./skills/03-sourcing/quotation-analysis) | `03-sourcing/quotation-analysis` | 采购 |
| 7 | [inventory-analysis](./skills/04-supply-chain/inventory-analysis) | `04-supply-chain/inventory-analysis` | 供应链 |
| 8 | [demand-forecast](./skills/04-supply-chain/demand-forecast) | `04-supply-chain/demand-forecast` | 供应链 |
| 9 | [amazon-operation](./skills/05-channel-operation/amazon-operation) | `05-channel-operation/amazon-operation` | 渠道运营 |
| 10 | [listing-writing](./skills/06-listing-content/listing-writing) | `06-listing-content/listing-writing` | 内容 |
| 11 | [seo-keyword](./skills/06-listing-content/seo-keyword) | `06-listing-content/seo-keyword` | 内容 |
| 12 | [advertising-analysis](./skills/07-growth-advertising/advertising-analysis) | `07-growth-advertising/advertising-analysis` | 增长广告 |
| 13 | [customer-support](./skills/08-customer-service/customer-support) | `08-customer-service/customer-support` | 客服 |
| 14 | [profitability-analysis](./skills/09-finance/profitability-analysis) | `09-finance/profitability-analysis` | 财务 |
| 15 | [odoo-integration](./skills/13-automation/odoo-integration) | `13-automation/odoo-integration` | 自动化 |

---

## 完整 Skill 目录

```
skills/
├── 00-core/
│   ├── task-planning           # 任务规划 ✅
│   ├── decision-analysis       # 决策分析 ✅
│   ├── report-generation       # 报告生成 ✅
│   └── knowledge-management    # 知识管理 ✅
│
├── 01-market-intelligence/
│   ├── market-research         # 市场调研 ✅
│   ├── competitor-analysis     # 竞品分析 ✅
│   ├── customer-insight        # 用户洞察
│   └── trend-monitoring        # 趋势监控
│
├── 02-product/
│   ├── product-selection       # 选品 ✅
│   ├── product-positioning     # 产品定位 ✅
│   ├── sku-management          # SKU 管理
│   └── pricing-strategy        # 定价策略
│
├── 03-sourcing/
│   ├── supplier-search         # 供应商搜索 ✅
│   ├── supplier-evaluation     # 供应商评估
│   ├── quotation-analysis      # 报价分析 ✅
│   ├── negotiation             # 供应商谈判
│   └── purchase-management     # 采购管理
│
├── 04-supply-chain/
│   ├── inventory-analysis      # 库存分析 ✅
│   ├── demand-forecast         # 销量预测 ✅
│   ├── replenishment           # 补货策略
│   ├── logistics-optimization  # 物流优化
│   └── fulfillment-management  # 履约管理
│
├── 05-channel-operation/
│   ├── amazon-operation        # Amazon 运营 ✅
│   ├── shopify-operation       # 独立站运营
│   ├── tiktok-shop-operation   # TikTok Shop 运营
│   ├── ebay-operation          # eBay 运营
│   ├── walmart-operation       # 沃尔玛运营
│   └── marketplace-sync        # 多平台同步
│
├── 06-listing-content/
│   ├── listing-writing         # Listing 文案 ✅
│   ├── seo-keyword             # 关键词分析 ✅
│   ├── image-prompt            # AI 图片生成
│   ├── video-script            # 短视频脚本
│   └── localization            # 本地化
│
├── 07-growth-advertising/
│   ├── advertising-analysis    # 广告分析 ✅
│   ├── campaign-management     # 广告计划
│   ├── keyword-optimization    # 关键词优化
│   ├── creative-testing        # 素材测试
│   └── conversion-analysis     # 转化分析
│
├── 08-customer-service/
│   ├── customer-support        # 客服回复 ✅
│   ├── complaint-analysis      # 投诉分析
│   ├── refund-management       # 退款流程
│   └── review-management       # 评价管理
│
├── 09-finance/
│   ├── cost-analysis           # 成本分析
│   ├── profitability-analysis  # 利润分析 ✅
│   ├── cashflow-management     # 现金流预测
│   ├── accounting-assistant    # 财务辅助
│   └── tax-analysis            # 税务分析
│
├── 10-data-analysis/
│   ├── business-dashboard      # 经营看板
│   ├── data-cleaning           # 数据清洗
│   ├── data-analysis           # 数据分析
│   └── anomaly-detection       # 异常检测
│
├── 11-compliance/
│   ├── compliance-check        # 产品合规
│   ├── trademark-check         # 商标检查
│   └── policy-monitoring       # 平台规则监控
│
├── 12-management/
│   ├── meeting-summary         # 会议总结
│   ├── task-followup           # 任务跟踪
│   ├── SOP-generation          # 流程生成
│   └── performance-review      # 绩效分析
│
├── 13-automation/
│   ├── odoo-integration        # Odoo 连接 ✅
│   ├── ecommerce-api           # 电商 API
│   ├── workflow-automation     # 自动流程
│   └── feishu-automation       # 飞书自动化
│
└── 14-learning-memory/
    ├── memory-manager          # 经验管理
    ├── knowledge-curator       # 知识整理
    └── skill-improvement       # 自我优化
```

---

## 核心闭环流程

```
人类输入 / 老板需求
    ↓
task-planning 拆解任务
    ↓
market-research + competitor-analysis → 找到机会
    ↓
product-selection 评分决策
    ↓
supplier-search + quotation-analysis → 确定供应链
    ↓
listing-writing + seo-keyword → 生成上架内容
    ↓
amazon-operation + advertising-analysis → 运营与推广
    ↓
customer-support → 处理客户问题
    ↓
inventory-analysis + demand-forecast → 库存与补货
    ↓
profitability-analysis → 利润复盘
    ↓
odoo-integration → 数据同步与凭证
    ↓
report-generation + knowledge-management → 沉淀与汇报
```

---

## 示例与脚本

每个核心 Skill 都配有 `references/examples.md`，包含真实场景下的输入输出示例，帮助 Agent 理解期望格式。

此外，`scripts/` 目录提供可直接运行的 Python 辅助脚本：

| 脚本 | 用途 | 对应 Skill |
|------|------|-----------|
| [inventory_analyzer.py](./scripts/ai-ecommerce/inventory_analyzer.py) | 库存健康度分析 | inventory-analysis |
| [demand_forecast.py](./scripts/ai-ecommerce/demand_forecast.py) | 销量预测 | demand-forecast |
| [ppc_analyzer.py](./scripts/ai-ecommerce/ppc_analyzer.py) | Amazon PPC 分析 | advertising-analysis |
| [profit_calculator.py](./scripts/ai-ecommerce/profit_calculator.py) | SKU 利润计算 | profitability-analysis |
| [odoo_client.py](./scripts/ai-ecommerce/odoo_client.py) | Odoo API 连接 | odoo-integration |
| [quotation_compare.py](./scripts/ai-ecommerce/quotation_compare.py) | 供应商报价比较 | quotation-analysis |
| [product_scorer.py](./scripts/ai-ecommerce/product_scorer.py) | 选品评分 | product-selection |
| [keyword_research.py](./scripts/ai-ecommerce/keyword_research.py) | 关键词扩展 | seo-keyword |

更多用法见 [scripts/README.md](./scripts/ai-ecommerce/README.md)。

---

## 使用方式

### Claude Code

```bash
# 整个目录作为 skill 集合使用
ln -s "$(pwd)" ~/.claude/skills/ai-ecommerce

# 或单独软链某个 skill
ln -s "$(pwd)/01-market-intelligence/market-research" ~/.claude/skills/market-research
```

### Skill 入口

每个 Skill 的入口是 `SKILL.md`，必须包含 YAML frontmatter：

```yaml
---
name: skill-name
description: 一句话描述 Skill 的用途和触发场景
---
```

---

## 扩展路线图

| 阶段 | 目标 | Skill 数量 | 状态 |
| --- | --- | --- | --- |
| 第一阶段 | 跑通选品→采购→上架→销售→库存→客服→利润闭环 | 15 | ✅ |
| 第二阶段 | 补齐内容、广告、客服、财务深度能力 | 30 | ✅ |
| 第三阶段 | 加入合规、管理、自动化、学习记忆 | 45 | ✅ |
| 第四阶段 | 全量 65 Skill，形成完整 AI 电商公司 | 65 | ✅ |

当前已完成 **全部 65 个 Skill** 的骨架和核心文档，后续重点是：

1. 根据真实业务场景持续细化每个 Skill
2. 补充更多实战案例和脚本
3. 建立 Memory 体系和 SOP Workflow
4. 对接真实数据源（Odoo、Amazon SP API、飞书等）

---

## 维护约定

- 新增 Skill：放在对应 category 目录下，自包含
- 引用文件统一放 `references/`
- frontmatter 至少含 `name` + `description`
- 敏感信息（API key、密码）绝不写入 Skill 文件
- 写操作（创建采购单、调整广告、退款）只生成草稿或建议，需人类确认
- 定期复盘 Skill 效果，由 skill-improvement 驱动迭代
