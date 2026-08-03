#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成剩余 46 个 AI 跨境电商 Skill 的 SKILL.md 文件。

用法：
    python scripts/generate_remaining_skills.py
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SKILL_TEMPLATE = """---
name: {name}
description: {description}
---

# {name} · {title}

## 用途
{purpose}

## 触发场景
{triggers}

## 输入
{inputs}

## 输出
{outputs}

## 工作流
{workflow}

## 调用关系
{relations}

## 依赖工具 / Memory
{dependencies}

## 边界与限制
{boundaries}

## 示例
{example}
"""

SKILLS = [
    # 01-market-intelligence
    {
        "path": "01-market-intelligence/customer-insight",
        "name": "customer-insight",
        "title": "用户洞察",
        "description": "分析评论、社媒和社区内容，提取用户痛点、购买原因、拒绝原因和情绪关键词，为产品定位和 Listing 优化提供依据。",
        "purpose": "- 从评论、社媒、社区中提炼用户需求\n- 识别用户痛点、购买动机、拒绝原因\n- 提取情绪关键词和口碑趋势\n- 为产品定位、Listing 文案、客服话术提供洞察",
        "triggers": "- 新品开发前需要了解用户\n- Listing 转化率低，需要优化卖点\n- 差评增多，需要分析根因\n- 品牌升级或产品迭代前",
        "inputs": "- 评论数据（Amazon、独立站、社媒）\n- 社媒讨论（Reddit、TikTok、Instagram）\n- 客服对话记录\n- 问卷或调研数据",
        "outputs": "```markdown\n## 用户洞察报告\n\n### 用户画像\n### 核心痛点\n### 购买原因\n### 拒绝原因\n### 情绪关键词\n### 未被满足的需求\n### 产品改进建议\n```",
        "workflow": "1. **数据采集**：收集评论、社媒、客服记录\n2. **数据清洗**：去重、去噪、分类\n3. **主题聚类**：痛点、卖点、使用场景\n4. **情绪分析**：正面、负面、中性\n5. **提炼洞察**：形成可行动结论\n6. **输出报告**：结构化呈现",
        "relations": "**被调用**：product-positioning、listing-writing、customer-support\n\n**调用**：market-research、data-analysis",
        "dependencies": "- Tool: 评论抓取工具、社媒监听工具\n- Memory: 用户画像库、历史洞察",
        "boundaries": "- 只分析公开可获取数据\n- 不窥探用户隐私\n- 洞察需结合定量数据验证",
        "example": "输入：1000 条 Amazon 评论\n输出：痛点 Top 5（噪音 22%、漏水 18%、滤芯贵 15%），改进建议：强调静音、优化密封、推出滤芯订阅"
    },
    {
        "path": "01-market-intelligence/trend-monitoring",
        "name": "trend-monitoring",
        "title": "趋势监控",
        "description": "每天扫描 TikTok、Google、YouTube、Pinterest 等平台，发现爆品趋势和新兴需求，抢占市场先机。",
        "purpose": "- 持续监控多平台热点\n- 发现潜在爆品和新兴需求\n- 预警趋势变化\n- 为选品和内容创作提供灵感",
        "triggers": "- 每日趋势扫描\n- 季度选品规划\n- 内容团队寻找选题\n- 发现异常销量波动时",
        "inputs": "- 监控关键词列表\n- 目标平台\n- 时间窗口\n- 历史趋势基线",
        "outputs": "```markdown\n## 趋势监控日报\n\n### 今日热点\n### 增长最快关键词\n### 新兴品类\n### 相关视频 / 内容\n### 机会评估\n### 风险提示\n```",
        "workflow": "1. **设置监控词**：品类词、场景词、竞品词\n2. **多平台扫描**：TikTok、Google Trends、YouTube、Pinterest\n3. **热度计算**：播放量、搜索量、互动增长率\n4. **趋势分类**：爆品、潜力、衰退、异常\n5. **输出预警**：高优先级趋势推送相关人员",
        "relations": "**被调用**：market-research、product-selection\n\n**调用**：market-research、data-analysis",
        "dependencies": "- Tool: 社媒 API、Google Trends、爬虫\n- Memory: 历史趋势库、爆款案例",
        "boundaries": "- 趋势不等于销量，需结合市场数据验证\n- 不追昙花一现的伪需求\n- 监控频率和范围受工具限制",
        "example": "输出：TikTok #quietcatfountain 标签近 7 天播放量增长 340%，建议关注静音饮水机趋势"
    },
    # 02-product
    {
        "path": "02-product/sku-management",
        "name": "sku-management",
        "title": "SKU 管理",
        "description": "负责 SKU 规划、规格设计、包装组合，连接 Odoo Product，确保产品数据一致性和可扩展性。",
        "purpose": "- 规划 SKU 结构和变体\n- 设计规格、颜色、尺寸等属性\n- 管理包装组合和套装\n- 同步 Odoo Product 数据",
        "triggers": "- 新品开发需要规划 SKU\n- 多平台销售需要统一 SKU\n- 产品变体过多需要优化\n- 库存混乱需要梳理",
        "inputs": "- 产品基础信息\n- 市场需求和竞品变体\n- 供应链能力\n- 平台属性要求",
        "outputs": "```markdown\n## SKU 规划方案\n\n### SKU 编码规则\n### 主 SKU 与变体\n### 规格矩阵\n### 包装组合\n### 多平台映射\n### Odoo 同步计划\n```",
        "workflow": "1. **确定 SKU 层级**：单品 / 变体 / 套装\n2. **设计编码规则**：类目-材质-容量-颜色\n3. **规划变体矩阵**：避免过度 SKU\n4. **设计包装组合**：单件 / 多件 / 滤芯套装\n5. **同步 Odoo**：创建或更新 product.template\n6. **维护映射表**：Amazon / Shopify / TikTok SKU 对应",
        "relations": "**被调用**：product-selection、marketplace-sync\n\n**调用**：odoo-integration、product-positioning",
        "dependencies": "- Tool: Odoo Product API\n- Memory: SKU 编码规范、历史变体表现",
        "boundaries": "- 不直接修改 Odoo 生产数据，只生成草稿\n- SKU 数量需平衡覆盖度和库存风险\n- 变体命名需符合平台规则",
        "example": "输出：WP-001-S（不锈钢 2.5L 标准版）、WP-001-S-6F（含半年滤芯套装），并生成 Odoo product.template 草稿"
    },
    {
        "path": "02-product/pricing-strategy",
        "name": "pricing-strategy",
        "title": "定价策略",
        "description": "基于成本、竞争价格和心理价格，制定产品定价策略，平衡利润、竞争力和转化率。",
        "purpose": "- 分析成本结构\n- 研究竞品价格带\n- 应用心理定价策略\n- 制定多平台价格策略",
        "triggers": "- 新品上架定价\n- 竞品降价需要应对\n- 利润下滑需要调价\n- 大促折扣策略制定",
        "inputs": "- 全成本数据\n- 竞品价格\n- 目标利润率\n- 品牌定位\n- 平台费用",
        "outputs": "```markdown\n## 定价策略方案\n\n### 成本结构\n### 竞品价格带\n### 建议售价\n### 心理定价点\n### 促销底价\n### 多平台价格建议\n```",
        "workflow": "1. **成本核算**：采购、物流、平台、广告、税费\n2. **竞品价格扫描**：高、中、低价格带\n3. **确定价格锚点**：避开红海、匹配定位\n4. **心理定价**：$39.99 vs $40\n5. **测试与迭代**：A/B 测试价格敏感度\n6. **输出策略**：日常价、促销价、底线价",
        "relations": "**被调用**：product-selection、amazon-operation\n\n**调用**：profitability-analysis、competitor-analysis、cost-analysis",
        "dependencies": "- Tool: 价格监控工具\n- Memory: 历史价格测试、促销效果",
        "boundaries": "- 不自动修改平台售价\n- 定价需考虑品牌长期定位\n- 低价竞争需谨慎",
        "example": "输出：建议定价 $39.99（竞品中位 $35-$45，心理价位 $39-$49），促销底价 $34.99"
    },
    # 03-sourcing
    {
        "path": "03-sourcing/supplier-evaluation",
        "name": "supplier-evaluation",
        "title": "供应商评估",
        "description": "从价格、质量、响应速度、生产能力、风险等维度评估供应商，输出评分和合作建议。",
        "purpose": "- 建立供应商评估体系\n- 对候选供应商量化打分\n- 识别供应商风险\n- 输出合作等级和建议",
        "triggers": "- 新供应商入围评估\n- 年度供应商考核\n- 出现质量问题后复评\n- 需要开发备选供应商",
        "inputs": "- 供应商基本信息\n- 报价和历史成交\n- 样品质量报告\n- 验厂报告\n- 客户反馈",
        "outputs": "```markdown\n## 供应商评估报告\n\n### 评分表\n| 维度 | 权重 | 得分 | 说明 |\n\n### 综合评级\n### 风险分析\n### 合作建议\n```",
        "workflow": "1. **信息收集**：资质、产能、认证、财务\n2. **多维度评分**：价格、质量、响应、产能、风险\n3. **现场/视频验厂**：生产能力、品控\n4. **样品测试**：质量、功能、包装\n5. **综合评级**：A/B/C/D\n6. **输出建议**：主力 / 备选 / 淘汰",
        "relations": "**被调用**：supplier-search、quotation-analysis\n\n**调用**：compliance-check、knowledge-management",
        "dependencies": "- Tool: 验厂清单、样品测试表\n- Memory: 供应商档案、历史评分",
        "boundaries": "- 评估基于可验证信息\n- 不替代实地考察（重要供应商）\n- 评估结果需定期更新",
        "example": "输出：工厂 B 综合评分 86（A 级），建议作为主力供应商；工厂 C 质量风险高，列为备选"
    },
    {
        "path": "03-sourcing/negotiation",
        "name": "negotiation",
        "title": "供应商谈判",
        "description": "生成询价话术、降价策略、合同条款，辅助采购人员与供应商谈判，争取更优价格和条件。",
        "purpose": "- 生成询价和议价话术\n- 制定降价策略和让步方案\n- 起草合同关键条款\n- 模拟谈判场景",
        "triggers": "- 收到报价后需要议价\n- 年度合同谈判\n- 要求更优付款条件\n- 处理交期或质量问题",
        "inputs": "- 供应商报价\n- 目标价格\n- 历史合作情况\n- 市场行情\n- 谈判底线",
        "outputs": "```markdown\n## 谈判方案\n\n### 目标与底线\n### 议价话术\n### 让步策略\n### 合同条款建议\n### 风险点提示\n```",
        "workflow": "1. **分析报价**：识别水分和合理性\n2. **设定目标价和底线价**\n3. **准备话术**：开场、压价、收尾\n4. **设计让步**：阶梯式让步，每次让步换条件\n5. **合同条款**：付款、交期、质量、售后\n6. **模拟演练**：预判供应商反应",
        "relations": "**被调用**：supplier-search、quotation-analysis\n\n**调用**：supplier-evaluation、knowledge-management",
        "dependencies": "- Memory: 历史谈判案例、行业成本基准\n- Tool: 报价分析表",
        "boundaries": "- 只生成建议，不直接发送给供应商\n- 重大合同条款需法务确认\n- 不采取欺诈或胁迫手段",
        "example": "输出：目标降价 8%，话术强调量大和长期合作，让步方案为接受 5% 降幅换 30 天账期"
    },
    {
        "path": "03-sourcing/purchase-management",
        "name": "purchase-management",
        "title": "采购管理",
        "description": "连接 Odoo Purchase，创建采购草稿、跟踪采购进度、管理供应商交期，确保采购流程可控。",
        "purpose": "- 在 Odoo 中创建采购草稿\n- 跟踪采购订单状态\n- 监控供应商交期\n- 预警采购异常",
        "triggers": "- 补货决策确认后\n- 需要创建采购单\n- 交期延迟需要跟进\n- 采购对账",
        "inputs": "- 采购需求（SKU、数量、目标交期）\n- 供应商信息\n- 报价单\n- Odoo Purchase 配置",
        "outputs": "```markdown\n## 采购管理报告\n\n### 采购草稿\n### PO 跟踪\n### 交期状态\n### 异常预警\n### 对账建议\n```",
        "workflow": "1. **接收采购需求**：来自 replenishment 或人工\n2. **选择供应商**：基于 evaluation 结果\n3. **创建采购草稿**：在 Odoo Purchase 生成 PO\n4. **人工确认**：采购人员审核后发送\n5. **跟踪进度**：交期、生产、质检、出货\n6. **异常处理**：延迟、质量问题升级",
        "relations": "**被调用**：replenishment、inventory-analysis\n\n**调用**：odoo-integration、supplier-evaluation",
        "dependencies": "- Tool: Odoo Purchase API\n- Memory: 采购历史、供应商交期记录",
        "boundaries": "- 只创建草稿状态 PO，不自动确认\n- 付款、合同签署需人工处理\n- 不越权修改已确认订单",
        "example": "输出：为 WP-001 创建 PO 草稿，数量 500，供应商工厂 B，目标交期 25 天"
    },
    # 04-supply-chain
    {
        "path": "04-supply-chain/replenishment",
        "name": "replenishment",
        "title": "补货策略",
        "description": "基于安全库存、采购周期、销量预测自动计算补货数量，连接采购和库存管理。",
        "purpose": "- 自动计算安全库存\n- 根据预测生成补货建议\n- 平衡缺货风险和库存积压\n- 输出可执行的补货计划",
        "triggers": "- 每周补货会议\n- 库存预警\n- 大促备货\n- 新品首单后补货",
        "inputs": "- 当前库存\n- 在途库存\n- 销量预测\n- 采购周期\n- 安全库存目标\n- 仓库分布",
        "outputs": "```markdown\n## 补货建议\n\n### 需要补货的 SKU\n| SKU | 建议补货量 | 目标仓库 | 期望到仓时间 |\n\n### 补货总量\n### 资金占用预估\n### 风险说明\n```",
        "workflow": "1. **计算日均销量**：基于 demand-forecast\n2. **设定安全库存**：通常 14-30 天销量\n3. **计算补货点**：安全库存 + 采购周期 × 日均销量\n4. **计算补货量**：目标库存 - 现有库存 - 在途库存\n5. **输出建议**：按优先级排序\n6. **生成采购草稿**：连接 purchase-management",
        "relations": "**被调用**：inventory-analysis、demand-forecast\n\n**调用**：purchase-management、odoo-integration",
        "dependencies": "- Tool: Odoo Inventory、预测模型\n- Memory: 采购周期、安全库存策略",
        "boundaries": "- 只输出建议，不自动下单\n- 季节性、促销期需人工调整\n- 新供应商首单需额外缓冲",
        "example": "输出：WP-001 建议补货 600 台，目标美西仓，预计资金占用 $5,220"
    },
    {
        "path": "04-supply-chain/logistics-optimization",
        "name": "logistics-optimization",
        "title": "物流优化",
        "description": "分析海运、空运、铁路、海外仓等物流方案，优化运输成本、时效和库存分布。",
        "purpose": "- 比较不同物流方式成本与时效\n- 优化头程和尾程物流\n- 规划海外仓布局\n- 降低物流成本",
        "triggers": "- 新品出货前选择物流\n- 物流成本上涨\n- 旺季备货需要加急\n- 评估新仓库布局",
        "inputs": "- 货物信息（重量、体积、货值）\n- 起运地和目的地\n- 时效要求\n- 预算约束\n- 各物流商报价",
        "outputs": "```markdown\n## 物流优化方案\n\n### 方案对比\n| 方式 | 时效 | 成本 | 适用场景 |\n\n### 推荐方案\n### 海外仓建议\n### 成本优化空间\n```",
        "workflow": "1. **收集报价**：海运、空运、铁路、快递\n2. **计算总成本**：运费 + 关税 + 保险 + 仓储\n3. **评估时效**：满足不同 SKU 需求\n4. **风险分析**：延误、查验、损耗\n5. **输出方案**：常规 / 加急 / 经济\n6. **海外仓规划**：库存分布建议",
        "relations": "**被调用**：quotation-analysis、replenishment\n\n**调用**：cost-analysis、data-analysis",
        "dependencies": "- Tool: 物流商 API、运费计算器\n- Memory: 历史物流时效、查验率",
        "boundaries": "- 不直接预订物流\n- 报价以物流商最新确认为准\n- 危险品需特殊处理",
        "example": "输出：2000 台饮水机推荐美森快船（18 天，$1.1/件），比空运节省 60%"
    },
    {
        "path": "04-supply-chain/fulfillment-management",
        "name": "fulfillment-management",
        "title": "履约管理",
        "description": "管理订单从仓库到物流再到签收的履约全流程，跟踪异常订单，提升客户体验。",
        "purpose": "- 跟踪订单履约状态\n- 识别异常订单（延迟、丢件、退货）\n- 协调仓库和物流\n- 提升签收率和客户满意度",
        "triggers": "- 每日履约监控\n- 客户投诉物流问题\n- 异常订单预警\n- 物流商考核",
        "inputs": "- 订单数据\n- 仓库出库数据\n- 物流追踪号\n- 签收状态\n- 退货数据",
        "outputs": "```markdown\n## 履约监控报告\n\n### 今日订单概况\n### 在途订单\n### 异常订单\n### 签收率\n### 物流商表现\n### 建议动作\n```",
        "workflow": "1. **拉取订单**：从 Odoo / 电商平台\n2. **跟踪物流状态**：根据追踪号同步\n3. **识别异常**：超时未更新、丢件、退回\n4. **预警升级**：通知客服或仓库\n5. **物流商考核**：时效、签收率、异常率\n6. **输出报告**：每日履约看板",
        "relations": "**被调用**：customer-support、workflow-automation\n\n**调用**：odoo-integration、ecommerce-api",
        "dependencies": "- Tool: 物流追踪 API、电商平台 API\n- Memory: 物流商表现、异常处理案例",
        "boundaries": "- 不直接联系物流商或客户\n- 只输出异常预警和处理建议\n- 涉及赔偿需人工处理",
        "example": "输出：今日 5 单物流 5 天未更新，建议联系物流商；USPS 签收率 96%，FedEx 98%"
    },
    # 05-channel-operation
    {
        "path": "05-channel-operation/shopify-operation",
        "name": "shopify-operation",
        "title": "独立站运营",
        "description": "负责 Shopify 商品管理、活动策划、转化优化和独立站增长策略。",
        "purpose": "- 管理 Shopify 商品上架和页面\n- 策划促销活动\n- 优化转化率\n- 分析独立站流量和销售",
        "triggers": "- Shopify 新品上架\n- 独立站转化率低\n- 策划营销活动\n- 分析独立站数据",
        "inputs": "- 产品信息\n- Shopify 后台数据\n- 流量数据（Google Analytics）\n- 广告数据\n- 用户行为数据",
        "outputs": "```markdown\n## Shopify 运营方案\n\n### 商品策略\n### 页面优化建议\n### 营销活动计划\n### 转化优化建议\n### 数据分析\n```",
        "workflow": "1. **店铺诊断**：流量、转化、客单价\n2. **商品优化**：标题、描述、图片、价格\n3. **页面优化**：首页、类目页、详情页\n4. **活动策划**：折扣、捆绑、邮件营销\n5. **广告投放**：Google、Meta、TikTok\n6. **数据复盘**：转化率、ROAS、LTV",
        "relations": "**被调用**：channel-operation-agent\n\n**调用**：listing-writing、advertising-analysis、conversion-analysis",
        "dependencies": "- Tool: Shopify Admin、Google Analytics\n- Memory: 独立站最佳实践、高转化页面",
        "boundaries": "- 不直接修改 Shopify 后台\n- 支付、退款等敏感操作需人工确认\n- 品牌视觉需符合规范",
        "example": "输出：建议首页增加信任徽章、产品页加入视频、设置弃购邮件挽回，预计转化率提升 15%"
    },
    {
        "path": "05-channel-operation/tiktok-shop-operation",
        "name": "tiktok-shop-operation",
        "title": "TikTok Shop 运营",
        "description": "负责 TikTok Shop 的达人合作、短视频内容、直播运营和店铺增长。",
        "purpose": "- 策划 TikTok 短视频内容\n- 管理达人合作\n- 优化直播运营\n- 分析 TikTok Shop 销售数据",
        "triggers": "- TikTok Shop 新品上架\n- 寻找合作达人\n- 短视频数据下滑\n- 直播策划",
        "inputs": "- 产品信息\n- TikTok Shop 数据\n- 达人数据\n- 短视频表现\n- 竞品内容",
        "outputs": "```markdown\n## TikTok Shop 运营方案\n\n### 内容策略\n### 达人合作计划\n### 直播计划\n### 投放策略\n### 数据复盘\n```",
        "workflow": "1. **店铺诊断**：GMV、转化率、内容表现\n2. **内容策划**：选题、脚本、拍摄计划\n3. **达人筛选**：粉丝画像、互动率、报价\n4. **直播运营**：排期、脚本、选品\n5. **广告投放**：Spark Ads、直播加热\n6. **数据复盘**：GMV、ROAS、内容 ROI",
        "relations": "**被调用**：channel-operation-agent\n\n**调用**：video-script、creative-testing、advertising-analysis",
        "dependencies": "- Tool: TikTok Shop Seller Center、达人平台\n- Memory: 爆款内容模板、达人库",
        "boundaries": "- 不直接发布内容或联系达人\n- 达人合作合同需人工确认\n- 内容需符合平台社区规范",
        "example": "输出：推荐 10 位宠物类达人，平均互动率 5%+，建议寄样 3 位做短视频测评"
    },
    {
        "path": "05-channel-operation/ebay-operation",
        "name": "ebay-operation",
        "title": "eBay 运营",
        "description": "负责 eBay 店铺运营，包括 Listing 优化、定价、促销和卖家绩效维护。",
        "purpose": "- 优化 eBay Listing\n- 管理 eBay 定价和促销\n- 维护卖家等级\n- 分析 eBay 销售和流量",
        "triggers": "- eBay 新品上架\n- 销量下滑\n- 卖家绩效预警\n- 平台政策变化",
        "inputs": "- 产品信息\n- eBay 后台数据\n- 竞品数据\n- 平台政策",
        "outputs": "```markdown\n## eBay 运营方案\n\n### Listing 优化\n### 定价策略\n### 促销计划\n### 卖家绩效维护\n### 风险预警\n```",
        "workflow": "1. **店铺诊断**：销售额、流量、转化率、卖家等级\n2. **Listing 优化**：标题、Item Specifics、图片\n3. **定价策略**：拍卖、一口价、Best Offer\n4. **促销工具**：Markdown、Promoted Listings\n5. **绩效维护**：物流时效、退货率、纠纷率\n6. **输出方案**：可执行优化清单",
        "relations": "**被调用**：channel-operation-agent\n\n**调用**：listing-writing、pricing-strategy、advertising-analysis",
        "dependencies": "- Tool: eBay Seller Hub\n- Memory: eBay 政策、高转化 Listing 案例",
        "boundaries": "- 不直接修改 eBay 后台\n- 账户安全操作需人工处理\n- 遵守 eBay 政策",
        "example": "输出：建议标题加入品牌词 + 核心功能词，开通 Promoted Listings Standard，目标 ROAS 4.0"
    },
    {
        "path": "05-channel-operation/walmart-operation",
        "name": "walmart-operation",
        "title": "沃尔玛运营",
        "description": "负责 Walmart Marketplace 店铺运营，包括 Listing、广告、定价和绩效维护。",
        "purpose": "- 管理 Walmart Listing\n- 优化 Walmart 广告\n- 制定定价策略\n- 维护卖家绩效",
        "triggers": "- Walmart 新品上架\n- 广告 ACOS 优化\n- 价格竞争力下降\n- 绩效预警",
        "inputs": "- 产品信息\n- Walmart Seller Center 数据\n- 竞品价格\n- 广告报告",
        "outputs": "```markdown\n## Walmart 运营方案\n\n### Listing 优化\n### 广告优化\n### 定价建议\n### 绩效维护\n### 增长机会\n```",
        "workflow": "1. **店铺诊断**：销售额、Buy Box 占有率、退货率\n2. **Listing 优化**：标题、描述、属性、图片\n3. **广告优化**：Sponsored Products 关键词和出价\n4. **定价策略**：Repricer 规则\n5. **库存管理**：防止断货影响绩效\n6. **输出方案**：优化清单",
        "relations": "**被调用**：channel-operation-agent\n\n**调用**：listing-writing、seo-keyword、advertising-analysis",
        "dependencies": "- Tool: Walmart Seller Center\n- Memory: Walmart 政策、竞品数据",
        "boundaries": "- 不直接修改 Seller Center\n- 价格调整需考虑利润\n- 遵守 Walmart 绩效标准",
        "example": "输出：建议优化 Item Specs 完整度至 95%，开启自动广告获取搜索词，设置有竞争力的 Repricer 规则"
    },
    {
        "path": "05-channel-operation/marketplace-sync",
        "name": "marketplace-sync",
        "title": "多平台同步",
        "description": "负责 Amazon、Shopify、TikTok、eBay、Walmart 与 Odoo 之间的数据同步，确保库存、价格、订单一致。",
        "purpose": "- 同步多平台库存\n- 同步价格和促销\n- 同步订单到 Odoo\n- 处理平台间冲突",
        "triggers": "- 新品多平台上架\n- 库存变动需要同步\n- 价格调整需要多平台更新\n- 订单需要回传 Odoo",
        "inputs": "- 各平台 API 数据\n- Odoo 数据\n- 同步规则\n- 冲突处理策略",
        "outputs": "```markdown\n## 多平台同步报告\n\n### 同步状态\n### 库存差异\n### 价格差异\n### 订单同步\n### 异常处理\n```",
        "workflow": "1. **建立映射**：SKU、仓库、价格、订单状态\n2. **库存同步**：以 Odoo 为准，定时推送各平台\n3. **价格同步**：按平台策略差异化定价\n4. **订单同步**：拉取订单到 Odoo Sales\n5. **异常处理**：超卖、价格冲突、SKU 缺失\n6. **监控告警**：同步失败通知",
        "relations": "**被调用**：workflow-automation、inventory-analysis\n\n**调用**：odoo-integration、ecommerce-api、feishu-automation",
        "dependencies": "- Tool: 各平台 API、Odoo API\n- Memory: SKU 映射表、同步规则",
        "boundaries": "- 不自动修改敏感数据\n- 同步前需测试\n- 重大价格调整需人工确认",
        "example": "输出：检测到 Amazon 库存 320 与 Shopify 库存 300 不一致，建议以 Odoo 可用库存 275 为准统一更新"
    },
    # 06-listing-content
    {
        "path": "06-listing-content/image-prompt",
        "name": "image-prompt",
        "title": "AI 图片生成",
        "description": "为主图、场景图、A+ 页面生成 AI 图片提示词，配合 image-gen Skill 出图。",
        "purpose": "- 生成电商主图提示词\n- 生成场景图、生活方式图提示词\n- 生成 A+ 页面配图提示词\n- 保持视觉风格一致",
        "triggers": "- 新品上架需要图片\n- 老品图片 CTR 低\n- A+ 页面需要配图\n- 广告素材测试需要多版本图片",
        "inputs": "- 产品信息\n- 目标用户\n- 使用场景\n- 图片类型（主图/场景图/A+）\n- 风格要求",
        "outputs": "```markdown\n## AI 图片生成方案\n\n### 主图提示词\n### 场景图提示词\n### A+ 配图提示词\n### 风格参考\n### 尺寸要求\n```",
        "workflow": "1. **确定图片目标**：主图、场景图、A+\n2. **提取产品卖点**：功能、材质、使用方式\n3. **设计场景**：用户、环境、情绪\n4. **编写提示词**：主体、风格、光线、构图\n5. **调用 image-gen**：批量生成\n6. **筛选优化**：A/B 测试",
        "relations": "**被调用**：listing-writing、amazon-operation、creative-testing\n\n**调用**：image-gen（外部 Skill）",
        "dependencies": "- Tool: image-gen Skill\n- Memory: 高 CTR 图片风格、品牌视觉规范",
        "boundaries": "- 不生成虚假或误导性图片\n- 模特、宠物等需考虑版权\n- 图片需符合平台规范",
        "example": "输出：主图提示词 'A stainless steel cat water fountain on a clean white background, soft studio lighting, a fluffy cat drinking from it, professional product photography, 4K'"
    },
    {
        "path": "06-listing-content/video-script",
        "name": "video-script",
        "title": "短视频脚本",
        "description": "为 TikTok、Amazon、独立站生成短视频脚本，包括开场、卖点展示、行动号召。",
        "purpose": "- 生成 TikTok 短视频脚本\n- 生成 Amazon 主图视频脚本\n- 生成广告视频脚本\n- 提高内容转化率",
        "triggers": "- 需要拍摄 TikTok 视频\n- 新品需要主图视频\n- 广告投放需要视频素材\n- 短视频表现差需要重写",
        "inputs": "- 产品信息\n- 目标平台\n- 目标用户\n- 核心卖点\n- 视频时长\n- 风格要求",
        "outputs": "```markdown\n## 短视频脚本\n\n### 视频信息\n### 镜头 1：开场（0-3s）\n### 镜头 2：痛点（3-8s）\n### 镜头 3：产品介绍（8-20s）\n### 镜头 4：使用场景（20-30s）\n### 镜头 5：CTA（30-35s）\n### 字幕 / 音乐建议\n```",
        "workflow": "1. **确定目标**：品牌曝光、转化、教育\n2. **研究爆款**：分析同类高赞视频\n3. **设计钩子**：前 3 秒抓住注意力\n4. **展示卖点**：功能 → 收益 → 情绪\n5. **设计 CTA**：购买、关注、评论\n6. **输出分镜**：画面、台词、时长、音乐",
        "relations": "**被调用**：tiktok-shop-operation、amazon-operation、creative-testing\n\n**调用**：customer-insight、competitor-analysis",
        "dependencies": "- Tool: 视频分析工具\n- Memory: 爆款脚本模板、品牌话术库",
        "boundaries": "- 不夸大产品功能\n- 遵守平台内容规范\n- 音乐、字体需注意版权",
        "example": "输出：15 秒 TikTok 脚本，前 3 秒猫咪拒绝喝旧水，中间展示饮水机水流，结尾主人微笑 + 'Link in bio'"
    },
    {
        "path": "06-listing-content/localization",
        "name": "localization",
        "title": "本地化",
        "description": "不只是语言翻译，而是文化适配。将 Listing、广告、客服内容适配到目标市场的语言习惯和文化背景。",
        "purpose": "- 翻译并本地化 Listing 文案\n- 适配不同市场的文化表达\n- 避免直译和语言错误\n- 提升本地用户信任感",
        "triggers": "- 产品进入新市场\n- 多平台多语言上架\n- 广告文案需要本地化\n- 客服模板需要多语言版本",
        "inputs": "- 原始文案\n- 源语言\n- 目标市场\n- 目标平台\n- 品牌调性",
        "outputs": "```markdown\n## 本地化方案\n\n### 翻译文本\n### 文化适配说明\n### 禁用词 / 敏感词检查\n### 本地市场表达建议\n```",
        "workflow": "1. **直译**：准确传达原意\n2. **文化适配**：俚语、节日、度量衡、消费习惯\n3. **平台适配**：Amazon、Shopify、TikTok 表达差异\n4. **本地审校**：检查语法、语气、文化禁忌\n5. **A/B 测试**：不同版本对比\n6. **输出最终文案**",
        "relations": "**被调用**：listing-writing、customer-support、advertising-analysis\n\n**调用**：market-research",
        "dependencies": "- Tool: 翻译工具、本地审校\n- Memory: 本地化术语库、文化禁忌",
        "boundaries": "- 不编造本地化信息\n- 宗教、政治、文化敏感内容需人工复核\n- 法律声明需本地法务确认",
        "example": "输出：美国版 'faucet' 在英国用 'tap'；德国市场需强调环保和认证；日本市场语气需更礼貌"
    },
    # 07-growth-advertising
    {
        "path": "07-growth-advertising/campaign-management",
        "name": "campaign-management",
        "title": "广告计划",
        "description": "制定、执行和优化广告投放计划，管理预算、出价、受众和素材组合。",
        "purpose": "- 制定广告投放计划\n- 管理广告预算分配\n- 优化出价策略\n- 协调多平台广告投放",
        "triggers": "- 新品上线需要广告计划\n- 大促需要预算规划\n- 广告表现需要优化\n- 需要测试新渠道",
        "inputs": "- 广告目标（销售、曝光、转化）\n- 预算\n- 目标受众\n- 产品信息\n- 历史广告数据",
        "outputs": "```markdown\n## 广告计划\n\n### 目标与 KPI\n### 预算分配\n### Campaign 结构\n### 出价策略\n### 素材计划\n### 测试计划\n### 优化节奏\n```",
        "workflow": "1. **明确目标**：销售、品牌、拉新\n2. **预算分配**：按平台、产品、漏斗阶段\n3. **Campaign 结构**：品牌、品类、竞品、再营销\n4. **出价策略**：自动、手动、目标 ACOS/ROAS\n5. **素材计划**：图片、视频、文案版本\n6. **上线与监控**：每日检查、每周优化\n7. **复盘迭代**：数据复盘、策略调整",
        "relations": "**被调用**：amazon-operation、shopify-operation、tiktok-shop-operation\n\n**调用**：advertising-analysis、creative-testing、seo-keyword",
        "dependencies": "- Tool: 广告平台 API\n- Memory: 历史广告计划、最佳实践",
        "boundaries": "- 只输出计划建议，不直接操作广告账户\n- 预算调整需人工确认\n- 不承诺具体 ROAS",
        "example": "输出：新品首月预算 $3000，70% 放 Amazon PPC（核心词 + 长尾词），30% 放 TikTok Spark Ads，目标 ACOS 30%"
    },
    {
        "path": "07-growth-advertising/keyword-optimization",
        "name": "keyword-optimization",
        "title": "关键词优化",
        "description": "持续优化广告关键词，包括拓词、否定词、出价调整、匹配方式优化，提升广告效率。",
        "purpose": "- 扩展高转化关键词\n- 添加否定词减少浪费\n- 优化关键词出价\n- 调整匹配方式",
        "triggers": "- 广告 ACOS 过高\n- Search Term Report 更新\n- 需要拓词\n- 发现高 spend 低转化词",
        "inputs": "- Search Term Report\n- 广告表现数据\n- 关键词排名\n- 竞品关键词",
        "outputs": "```markdown\n## 关键词优化方案\n\n### 新增关键词\n### 否定词建议\n### 出价调整\n### 匹配方式调整\n### 预期效果\n```",
        "workflow": "1. **数据清洗**：整理 Search Term Report\n2. **识别高转化词**：高销售、低 ACOS\n3. **识别浪费词**：高 spend、低转化\n4. **拓词**：从竞品、长尾、相关搜索扩展\n5. **优化出价**：升降出价、调整匹配\n6. **输出方案**：新增、否定、调价清单",
        "relations": "**被调用**：advertising-analysis、campaign-management\n\n**调用**：seo-keyword、competitor-analysis",
        "dependencies": "- Tool: 广告平台报告\n- Memory: 历史关键词表现、否定词库",
        "boundaries": "- 只输出优化建议，不直接修改广告\n- 否定词需避免误伤\n- 大词调整需谨慎",
        "example": "输出：新增 8 个长尾词，否定 12 个宽泛词，3 个核心词提价 15%，预计 ACOS 降 5pp"
    },
    {
        "path": "07-growth-advertising/creative-testing",
        "name": "creative-testing",
        "title": "素材测试",
        "description": "测试不同图片、视频、文案素材的转化效果，找出最佳创意组合。",
        "purpose": "- 设计素材 A/B 测试\n- 分析 CTR、CVR、ROAS 差异\n- 识别最佳创意方向\n- 沉淀高转化素材模板",
        "triggers": "- 广告 CTR 低\n- 需要新素材方向\n- 大促前测试创意\n- 素材疲劳需要更新",
        "inputs": "- 现有素材数据\n- 竞品素材\n- 测试预算\n- 目标受众\n- 产品卖点",
        "outputs": "```markdown\n## 素材测试方案\n\n### 测试假设\n### 素材版本\n### 测试预算与周期\n### 分组策略\n### 胜出标准\n### 测试结果分析\n```",
        "workflow": "1. **提出假设**：某类图片/视频更吸引目标用户\n2. **设计版本**：主图、场景、人物、文案\n3. **分配预算**：控制变量，确保统计显著\n4. **运行测试**：通常 7-14 天\n5. **分析结果**：CTR、CVR、ROAS、CPA\n6. **沉淀模板**：获胜素材扩展为系列",
        "relations": "**被调用**：campaign-management、amazon-operation\n\n**调用**：image-prompt、video-script、conversion-analysis",
        "dependencies": "- Tool: 广告平台 A/B 测试功能\n- Memory: 历史测试结果、高转化素材模板",
        "boundaries": "- 测试需有足够样本量\n- 不基于短期数据做决策\n- 创意需符合品牌规范",
        "example": "输出：测试 3 组主图，'猫咪喝水场景图' CTR 1.8% 胜出（vs 白底图 0.9%），建议扩展为视频素材"
    },
    {
        "path": "07-growth-advertising/conversion-analysis",
        "name": "conversion-analysis",
        "title": "转化分析",
        "description": "分析 CTR、CVR、CPA、ROAS 等转化指标，找出漏斗泄漏点，提升整体转化效率。",
        "purpose": "- 分析广告到购买的转化漏斗\n- 识别 CTR、CVR 异常\n- 诊断落地页问题\n- 输出转化优化建议",
        "triggers": "- 广告流量高但销量低\n- CTR 或 CVR 异常\n- 需要优化落地页\n- 大促复盘",
        "inputs": "- 广告数据\n- 网站/店铺数据\n- 用户行为数据\n- 销售数据",
        "outputs": "```markdown\n## 转化分析报告\n\n### 漏斗分析\n### 关键指标\n### 泄漏点识别\n### 优化建议\n### 预期提升\n```",
        "workflow": "1. **建立漏斗**：曝光 → 点击 → 加购 → 结算 → 购买\n2. **计算指标**：CTR、CVR、CPA、ROAS、AOV\n3. **对比基准**：行业、历史、竞品\n4. **识别泄漏点**：哪个环节流失最多\n5. **根因分析**：素材、价格、页面、流程\n6. **输出建议**：针对性优化",
        "relations": "**被调用**：advertising-analysis、amazon-operation、shopify-operation\n\n**调用**：data-analysis、creative-testing",
        "dependencies": "- Tool: GA4、广告平台、热图工具\n- Memory: 行业转化率基准",
        "boundaries": "- 归因分析存在局限性\n- 不承诺具体提升幅度\n- 需结合多数据源判断",
        "example": "输出：点击到加购转化率 5%（健康），但加购到结算仅 20%（偏低），建议优化结算页运费显示"
    },
    # 08-customer-service
    {
        "path": "08-customer-service/complaint-analysis",
        "name": "complaint-analysis",
        "title": "投诉分析",
        "description": "分析客户投诉，提取产品问题、服务问题和流程问题，推动产品改进和服务优化。",
        "purpose": "- 分类和量化客户投诉\n- 提取产品问题根因\n- 识别高频服务问题\n- 推动产品和流程改进",
        "triggers": "- 投诉量上升\n- 需要产品改进依据\n- 月度客服复盘\n- 差评批量分析",
        "inputs": "- 客户投诉记录\n- 客服对话\n- 退货原因\n- 差评内容",
        "outputs": "```markdown\n## 投诉分析报告\n\n### 投诉总量与趋势\n### 投诉分类\n### 高频问题 Top 10\n### 产品问题根因\n### 改进建议\n### 责任部门分配\n```",
        "workflow": "1. **收集投诉**：客服记录、评论、退货\n2. **分类标注**：产品、物流、服务、价格\n3. **提取关键词**：漏水、噪音、包装破损\n4. **量化趋势**：本周 vs 上周 vs 上月\n5. **根因分析**：设计、生产、物流、包装\n6. **输出改进建议**：责任部门 + 行动项",
        "relations": "**被调用**：customer-support、review-management\n\n**调用**：data-analysis、product-selection",
        "dependencies": "- Tool: 客服系统、评论数据\n- Memory: 历史投诉库、改进措施效果",
        "boundaries": "- 保护客户隐私\n- 不用于追责个人\n- 需结合生产数据验证",
        "example": "输出：本月投诉 Top 3 为漏水 35%、噪音 22%、包装破损 15%，建议改进密封圈和包装方案"
    },
    {
        "path": "08-customer-service/refund-management",
        "name": "refund-management",
        "title": "退款流程",
        "description": "生成退款建议和处理话术，辅助客服人员处理退款、退货、重发等售后问题，不自动执行退款。",
        "purpose": "- 评估退款合理性\n- 生成退款建议\n- 提供客服话术\n- 记录退款原因和金额",
        "triggers": "- 客户要求退款\n- 退货申请需要审核\n- 需要判断重发或退款\n- 退款纠纷处理",
        "inputs": "- 客户请求\n- 订单信息\n- 退货原因\n- 产品问题证据\n- 退款政策",
        "outputs": "```markdown\n## 退款处理建议\n\n### 退款合理性评估\n### 建议方案\n### 客服话术\n### 需升级事项\n### 记录与统计\n```",
        "workflow": "1. **核实订单**：金额、时间、物流状态\n2. **评估原因**：产品质量、物流损坏、不喜欢\n3. **匹配政策**：是否在规定期限内\n4. **生成方案**：全额退、部分退、换货、重发\n5. **输出话术**：专业、共情、明确\n6. **标记升级**：大额、欺诈、法律风险",
        "relations": "**被调用**：customer-support\n\n**调用**：complaint-analysis、odoo-integration",
        "dependencies": "- Tool: 订单系统、退款政策\n- Memory: 历史退款案例、欺诈模式",
        "boundaries": "- 只生成建议，不自动退款\n- 所有退款需人工确认\n- 不处理疑似欺诈（需升级）",
        "example": "输出：客户因产品质量问题要求退款，建议全额退款并承担退货运费，话术已生成，需客服主管确认"
    },
    {
        "path": "08-customer-service/review-management",
        "name": "review-management",
        "title": "评价管理",
        "description": "分析五星好评和差评原因，生成回复话术，监控评价变化，维护品牌形象。",
        "purpose": "- 分析评价情感和原因\n- 生成差评回复话术\n- 提取好评关键词\n- 监控评分变化",
        "triggers": "- 新增差评需要回复\n- 月度评价复盘\n- 评分下降\n- 需要收集好评素材",
        "inputs": "- 产品评价数据\n- 星级分布\n- 评价内容\n- 竞品评价",
        "outputs": "```markdown\n## 评价分析报告\n\n### 评分概览\n### 好评关键词\n### 差评关键词\n### 差评回复话术\n### 改进建议\n```",
        "workflow": "1. **收集评价**：Amazon、独立站、社媒\n2. **情感分类**：好评、中评、差评\n3. **关键词提取**：点赞点、吐槽点\n4. **生成回复**：差评共情 + 解决，好评感谢\n5. **监控趋势**：评分、评论数、星级分布\n6. **输出建议**：产品改进、客服优化",
        "relations": "**被调用**：amazon-operation、customer-support\n\n**调用**：complaint-analysis、customer-insight",
        "dependencies": "- Tool: 评价抓取工具\n- Memory: 优秀回复模板、差评根因库",
        "boundaries": "- 不删除或修改真实评价\n- 不诱导虚假好评\n- 回复需符合平台政策",
        "example": "输出：差评集中在滤芯难买，建议上架滤芯套装并优化 Listing 说明，同时生成官方回复话术"
    },
    # 09-finance
    {
        "path": "09-finance/cost-analysis",
        "name": "cost-analysis",
        "title": "成本分析",
        "description": "全面拆解采购、物流、平台费、广告、税费等成本，识别降本机会。",
        "purpose": "- 拆解全链路成本\n- 识别成本异常\n- 分析降本空间\n- 为定价和利润分析提供基础",
        "triggers": "- 利润下滑需要分析成本\n- 供应商报价对比\n- 物流费用上涨\n- 年度成本预算",
        "inputs": "- 采购成本\n- 物流账单\n- 平台费用\n- 广告 spend\n- 税费\n- 其他运营费用",
        "outputs": "```markdown\n## 成本分析报告\n\n### 总成本结构\n### 各 SKU 成本分布\n### 异常成本项\n### 降本建议\n### 敏感性分析\n```",
        "workflow": "1. **归集成本**：按类目、SKU、时间归集\n2. **分类统计**：采购、物流、平台、广告、税费\n3. **对比分析**：环比、同比、预算对比\n4. **识别异常**：超预算、单价异常、损耗\n5. **输出建议**：议价、换物流、优化包装\n6. **敏感性分析**：成本变动对利润影响",
        "relations": "**被调用**：profitability-analysis、quotation-analysis\n\n**调用**：odoo-integration、data-analysis",
        "dependencies": "- Tool: Odoo Accounting、账单数据\n- Memory: 历史成本基准、供应商价格库",
        "boundaries": "- 成本数据需准确归集\n- 间接费用分摊需约定规则\n- 降本建议需考虑质量风险",
        "example": "输出：物流成本占比从 12% 升至 16%，建议换海运联盟，预计节省 8% 头程费用"
    },
    {
        "path": "09-finance/cashflow-management",
        "name": "cashflow-management",
        "title": "现金流预测",
        "description": "基于销售预测、采购计划、费用支出预测未来现金流，预警资金缺口。",
        "purpose": "- 预测未来现金流\n- 预警资金缺口\n- 优化付款节奏\n- 支持采购和库存决策",
        "triggers": "- 月度财务规划\n- 大促备货前\n- 现金流紧张\n- 需要融资或贷款",
        "inputs": "- 销售预测\n- 采购计划\n- 费用预算\n- 应收账款\n- 应付账款\n- 现金余额",
        "outputs": "```markdown\n## 现金流预测报告\n\n### 当前现金余额\n### 未来 13 周现金流\n### 资金缺口预警\n### 建议行动\n### 敏感性分析\n```",
        "workflow": "1. **收集数据**：收入、支出、应收应付\n2. **建立模型**：按周预测现金流入流出\n3. **情景分析**：乐观、中性、悲观\n4. **识别缺口**：资金低于安全线的时间点\n5. **输出建议**：延迟付款、加快回款、减少库存\n6. **滚动更新**：每周更新预测",
        "relations": "**被调用**：CEO Agent、task-planning\n\n**调用**：demand-forecast、purchase-management、cost-analysis",
        "dependencies": "- Tool: 财务数据、Odoo Accounting\n- Memory: 历史现金流、回款周期",
        "boundaries": "- 预测基于假设，存在不确定性\n- 不替代财务专业判断\n- 重大资金决策需 CFO 确认",
        "example": "输出：9 月因大促备货将出现 $45,000 资金缺口，建议 8 月压缩非必要支出或申请短期授信"
    },
    {
        "path": "09-finance/accounting-assistant",
        "name": "accounting-assistant",
        "title": "财务辅助",
        "description": "连接 Odoo Accounting，创建凭证草稿、分析账目、辅助对账和报表生成。",
        "purpose": "- 创建会计凭证草稿\n- 分析账目异常\n- 辅助对账\n- 生成财务报表初稿",
        "triggers": "- 需要创建凭证\n- 月度对账\n- 账目异常需要分析\n- 需要快速报表",
        "inputs": "- 交易数据\n- 凭证信息\n- 对账单\n- Odoo Accounting 配置",
        "outputs": "```markdown\n## 财务辅助报告\n\n### 凭证草稿\n### 账目分析\n### 对账差异\n### 建议调整\n### 报表初稿\n```",
        "workflow": "1. **接收数据**：发票、银行流水、平台账单\n2. **分类匹配**：收入、成本、费用\n3. **创建草稿**：在 Odoo 生成凭证草稿\n4. **异常识别**：对账差异、重复记录\n5. **输出分析**：科目余额、趋势\n6. **人工确认**：会计审核后过账",
        "relations": "**被调用**：profitability-analysis、cost-analysis\n\n**调用**：odoo-integration、data-cleaning",
        "dependencies": "- Tool: Odoo Accounting API\n- Memory: 会计科目映射、对账规则",
        "boundaries": "- 只创建草稿，不过账\n- 税务、审计问题需专业会计\n- 不处理现金收支",
        "example": "输出：根据 7 月 Amazon 结算单生成 12 张凭证草稿，涉及收入、佣金、FBA 费用等科目"
    },
    {
        "path": "09-finance/tax-analysis",
        "name": "tax-analysis",
        "title": "税务分析",
        "description": "分析 VAT、GST、销售税等税务合规要求，计算税费影响，辅助税务决策。",
        "purpose": "- 分析目标市场税务要求\n- 计算销售税 / VAT / GST\n- 识别税务风险\n- 辅助税务合规",
        "triggers": "- 进入新市场\n- 税务合规审查\n- 利润分析需要扣税\n- 平台税务政策变化",
        "inputs": "- 目标市场\n- 销售额\n- 产品类别\n- 仓储地点\n- 公司注册地",
        "outputs": "```markdown\n## 税务分析报告\\n\\n### 适用税种\\n### 税率\\n### 税务义务\\n### 税费计算\\n### 合规建议\\n### 风险提示\\n```",
        "workflow": "1. **识别税种**：销售税、VAT、GST、进口税\n2. **确定税率**：按国家和州/省\n3. **判断纳税义务**：经济联结（nexus）\n4. **计算税费影响**：对利润的影响\n5. **合规建议**：注册、申报、代扣\n6. **风险提示**：逾期、漏报、误算",
        "relations": "**被调用**：profitability-analysis、market-research\n\n**调用**：compliance-check、accounting-assistant",
        "dependencies": "- Tool: 税务数据库、平台税务报告\n- Memory: 各国税务规则、申报日历",
        "boundaries": "- 不替代专业税务顾问\n- 税务规则变化快，需定期更新\n- 重大税务决策需确认当地法规",
        "example": "输出：美国销售需关注各州经济联结，预计销售税占收入 6-10%，建议注册 Avalara 或 TaxJar 自动计算"
    },
    # 10-data-analysis
    {
        "path": "10-data-analysis/business-dashboard",
        "name": "business-dashboard",
        "title": "经营看板",
        "description": "构建 GMV、利润、库存、广告等核心指标的经营看板，支持管理层决策。",
        "purpose": "- 整合多数据源\n- 构建核心指标看板\n- 支持实时监控\n- 发现业务异常和机会",
        "triggers": "- 管理层需要业务概览\n- 每日经营晨会\n- 需要构建 BI 看板\n- 指标体系梳理",
        "inputs": "- 销售数据\n- 广告数据\n- 库存数据\n- 财务数据\n- 用户数据",
        "outputs": "```markdown\n## 经营看板方案\n\n### 核心 KPI\n### 指标定义\n### 数据源\n### 刷新频率\n### 可视化设计\n### 告警规则\n```",
        "workflow": "1. **确定指标**：GMV、利润、库存周转、ROAS\n2. **梳理数据源**：Odoo、Amazon、Shopify、广告平台\n3. **设计看板**：汇总、趋势、对比、明细\n4. **数据建模**：ETL、维度、指标计算\n5. **可视化实现**：图表、筛选、下钻\n6. **告警配置**：异常阈值、推送渠道",
        "relations": "**被调用**：CEO Agent、report-generation\n\n**调用**：data-analysis、odoo-integration、ecommerce-api",
        "dependencies": "- Tool: BI 工具（Metabase/Superset/Tableau）、Python\n- Memory: 指标定义、历史基线",
        "boundaries": "- 看板数据质量取决于数据源\n- 不替代深度分析\n- 实时性受 ETL 频率限制",
        "example": "输出：设计 4 个看板（销售、广告、库存、财务），32 个核心指标，每日 8 点自动推送飞书"
    },
    {
        "path": "10-data-analysis/data-cleaning",
        "name": "data-cleaning",
        "title": "数据清洗",
        "description": "清洗电商平台、广告平台、Odoo 等来源的脏数据，为分析提供高质量数据基础。",
        "purpose": "- 处理缺失值、异常值\n- 统一数据格式\n- 去重和合并\n- 建立数据质量规则",
        "triggers": "- 数据分析前\n- 发现数据异常\n- 建立数据管道\n- 对接新数据源",
        "inputs": "- 原始数据\n- 数据字典\n- 清洗规则\n- 质量要求",
        "outputs": "```markdown\n## 数据清洗报告\n\n### 数据概况\n### 质量问题\n### 清洗规则\n### 清洗后数据\n### 质量评分\n```",
        "workflow": "1. **数据探查**：分布、缺失、异常\n2. **制定规则**：填充、删除、转换、校验\n3. **执行清洗**：去重、格式统一、异常处理\n4. **质量验证**：完整性、一致性、准确性\n5. **输出报告**：问题清单和清洗结果\n6. **建立监控**：持续数据质量检查",
        "relations": "**被调用**：data-analysis、business-dashboard、demand-forecast\n\n**调用**：odoo-integration、ecommerce-api",
        "dependencies": "- Tool: Python pandas / SQL\n- Memory: 数据字典、清洗规则库",
        "boundaries": "- 不删除原始数据\n- 清洗规则需记录\n- 对业务有影响的处理需确认",
        "example": "输出：清洗 50,000 条订单，修复 1,200 个缺失 SKU，删除 45 条重复记录，标记 230 个异常金额"
    },
    {
        "path": "10-data-analysis/data-analysis",
        "name": "data-analysis",
        "title": "数据分析",
        "description": "使用 SQL、Python、BI 工具对业务数据进行深度分析，回答复杂业务问题。",
        "purpose": "- 回答复杂业务问题\n- 进行多维度分析\n- 发现数据规律和异常\n- 输出可行动洞察",
        "triggers": "- 业务问题需要数据支撑\n- 需要深度分析\n- 建立分析模型\n- 数据驱动决策",
        "inputs": "- 清洗后的数据\n- 分析目标\n- 假设和问题\n- 工具偏好",
        "outputs": "```markdown\n## 数据分析报告\n\n### 分析目标\n### 数据说明\n### 分析方法\n### 关键发现\n### 业务建议\n### 附录：代码 / 查询\n```",
        "workflow": "1. **明确问题**：业务问题转化为数据问题\n2. **提取数据**：SQL、API、文件\n3. **探索分析**：描述统计、可视化\n4. **建模分析**：回归、聚类、时序\n5. **验证假设**：A/B 测试、显著性\n6. **输出洞察**：结论和建议",
        "relations": "**被调用**：所有需要数据分析的 Skill\n\n**调用**：data-cleaning、business-dashboard",
        "dependencies": "- Tool: SQL、Python、Jupyter、BI 工具\n- Memory: 分析模板、常用查询",
        "boundaries": "- 分析结果受数据质量限制\n- 相关性不等于因果性\n- 复杂模型需验证假设",
        "example": "输出：分析发现广告 Spend 与销量存在 3 天滞后，建议调整预算分配节奏，周末前置投放"
    },
    {
        "path": "10-data-analysis/anomaly-detection",
        "name": "anomaly-detection",
        "title": "异常检测",
        "description": "自动发现销量、广告、库存等指标的异常波动，及时预警业务风险。",
        "purpose": "- 监控关键指标异常\n- 及时发现销量、广告、库存异常\n- 减少人工监控成本\n- 支持快速响应",
        "triggers": "- 每日自动监控\n- 关键指标波动\n- 建立告警体系\n- 复盘异常事件",
        "inputs": "- 历史指标数据\n- 监控指标列表\n- 异常阈值\n- 时间窗口",
        "outputs": "```markdown\n## 异常检测报告\n\n### 异常指标\n### 异常时间\n### 异常程度\n### 可能原因\n### 建议动作\n### 相关影响\n```",
        "workflow": "1. **定义指标**：销量、广告、库存、利润\n2. **建立基线**：历史均值、标准差、趋势\n3. **选择算法**：统计阈值、同比环比、时序模型\n4. **检测异常**：超出阈值或偏离趋势\n5. **根因提示**：关联指标分析\n6. **推送告警**：飞书 / 邮件通知",
        "relations": "**被调用**：business-dashboard、workflow-automation\n\n**调用**：data-analysis、feishu-automation",
        "dependencies": "- Tool: Python、时序模型\n- Memory: 历史异常案例、阈值配置",
        "boundaries": "- 异常可能是正常波动，需人工判断\n- 阈值需根据业务调整\n- 不自动采取业务动作",
        "example": "输出：WP-001 今日销量较 7 日均值下降 65%，同时广告 spend 正常，疑似库存断货或差评影响"
    },
    # 11-compliance
    {
        "path": "11-compliance/compliance-check",
        "name": "compliance-check",
        "title": "产品合规",
        "description": "检查产品是否符合 FDA、CE、FCC、RoHS 等目标市场合规要求，降低合规风险。",
        "purpose": "- 识别目标市场合规要求\n- 检查认证是否齐全\n- 评估产品合规风险\n- 输出合规检查清单",
        "triggers": "- 选品阶段\n- 进入新市场\n- 产品变更\n- 平台合规审查",
        "inputs": "- 产品信息\n- 目标市场\n- 现有认证\n- 供应商资料",
        "outputs": "```markdown\n## 合规检查报告\n\n### 适用法规\n### 所需认证\n### 现有认证状态\n### 缺失项\n### 风险等级\n### 行动计划\n```",
        "workflow": "1. **确定市场**：美国、欧盟、英国等\n2. **识别法规**：FDA、CE、FCC、RoHS、CPC 等\n3. **核对认证**：检查证书、测试报告\n4. **评估风险**：高 / 中 / 低\n5. **输出清单**：缺失项、负责人、时间\n6. **跟踪闭环**：认证补齐确认",
        "relations": "**被调用**：product-selection、supplier-search\n\n**调用**：policy-monitoring、supplier-evaluation",
        "dependencies": "- Tool: 合规数据库、认证文件\n- Memory: 各国合规要求、历史问题",
        "boundaries": "- 不替代专业合规顾问\n- 法规变化需持续更新\n- 最终合规责任在人类",
        "example": "输出：美国销售宠物饮水机需 FCC（带电）和 FDA 食品接触材料检测，欧盟需 CE 和 RoHS，当前缺失 FDA 报告"
    },
    {
        "path": "11-compliance/trademark-check",
        "name": "trademark-check",
        "title": "商标检查",
        "description": "检查品牌名、产品名、关键词是否侵犯他人商标，降低侵权风险。",
        "purpose": "- 检查品牌名可注册性\n- 识别潜在商标侵权\n- 监控竞品商标动态\n- 保护自有品牌",
        "triggers": "- 新品命名\n- 品牌注册前\n- 收到侵权投诉\n- 关键词广告投放前",
        "inputs": "- 品牌名 / 产品名\n- 目标市场\n- 产品类别\n- 待检查关键词",
        "outputs": "```markdown\n## 商标检查报告\n\n### 检查对象\n### 检索结果\n### 冲突风险\n### 建议行动\n### 注册建议\n```",
        "workflow": "1. **商标局检索**：USPTO、EUIPO、中国商标网等\n2. **分类匹配**：核对产品类别\n3. **相似度判断**：文字、发音、含义\n4. **评估风险**：高 / 中 / 低\n5. **输出建议**：改名、注册、监控\n6. **持续监控**：新申请商标预警",
        "relations": "**被调用**：product-positioning、amazon-operation\n\n**调用**：policy-monitoring",
        "dependencies": "- Tool: 商标局数据库、检索工具\n- Memory: 自有商标、黑名单",
        "boundaries": "- 不替代律师意见\n- 检索结果有滞后性\n- 最终注册需专业机构",
        "example": "输出：品牌名 'FlowPaw' 在美国无相同商标，建议尽快注册；关键词 'Catit' 为竞品商标，需加入否定词"
    },
    {
        "path": "11-compliance/policy-monitoring",
        "name": "policy-monitoring",
        "title": "平台规则监控",
        "description": "监控 Amazon、Shopify、TikTok 等平台的规则变化，预警可能影响业务的政策调整。",
        "purpose": "- 监控平台政策变化\n- 预警合规风险\n- 及时调整运营策略\n- 避免因违规导致处罚",
        "triggers": "- 每日/每周政策扫描\n- 收到平台通知\n- 店铺绩效异常\n- 新规则上线",
        "inputs": "- 监控平台列表\n- 业务涉及的政策领域\n- 历史违规记录",
        "outputs": "```markdown\n## 平台规则监控报告\n\n### 新规则摘要\n### 影响评估\n### 涉及业务\n### 建议行动\n### 截止时间\n```",
        "workflow": "1. **设置监控范围**：类目、广告、物流、售后\n2. **采集政策更新**：平台公告、卖家中心\n3. **解读影响**：对当前业务的影响程度\n4. **评估风险**：高 / 中 / 低\n5. **输出建议**：调整 Listing、广告、流程\n6. **跟踪闭环**：确认已落实",
        "relations": "**被调用**：amazon-operation、shopify-operation、tiktok-shop-operation\n\n**调用**：compliance-check、feishu-automation",
        "dependencies": "- Tool: 平台公告、卖家中心\n- Memory: 历史政策变化、处罚案例",
        "boundaries": "- 政策解读不替代官方说明\n- 重大规则变化需法务/运营确认\n- 监控范围受限于公开信息",
        "example": "输出：Amazon 更新宠物用品 FDA 合规要求，90 天内需补充检测报告，涉及 3 个 SKU"
    },
    # 12-management
    {
        "path": "12-management/meeting-summary",
        "name": "meeting-summary",
        "title": "会议总结",
        "description": "将会议录音或纪要转换为结构化总结，提取决策、行动项和责任人。",
        "purpose": "- 整理会议纪要\n- 提取关键决策\n- 明确行动项和责任人\n- 生成可追踪的会议产出",
        "triggers": "- 会议结束后\n- 需要同步会议结论\n- 跟踪行动项\n- 复盘会议决策",
        "inputs": "- 会议录音/文字稿\n- 参会人\n- 会议主题\n- 往期行动项",
        "outputs": "```markdown\n## 会议纪要\n\n### 会议信息\n### 与会人员\n### 核心议题\n### 关键决策\n### 行动项\n| 事项 | 负责人 | 截止时间 |\n\n### 待解决问题\n```",
        "workflow": "1. **转录录音**：语音转文字\n2. **分段整理**：按议题划分\n3. **提取决策**：明确结论\n4. **识别行动项**：任务、负责人、时间\n5. **输出纪要**：结构化、简洁\n6. **同步飞书**：推送相关人员",
        "relations": "**被调用**：CEO Agent、task-followup\n\n**调用**：feishu-automation、report-generation",
        "dependencies": "- Tool: 语音识别、飞书文档\n- Memory: 历史会议纪要、决策库",
        "boundaries": "- 不曲解会议内容\n- 敏感决策需发言人确认\n- 行动项需责任人认可",
        "example": "输出：10 分钟会议录音整理为 1 页纪要，3 项决策，5 个行动项，自动同步飞书任务"
    },
    {
        "path": "12-management/task-followup",
        "name": "task-followup",
        "title": "任务跟踪",
        "description": "连接飞书任务/项目，跟踪任务进度，提醒逾期，汇总任务状态。",
        "purpose": "- 跟踪任务执行情况\n- 提醒逾期任务\n- 汇总项目进度\n- 推动任务闭环",
        "triggers": "- 每日任务检查\n- 项目进度会议\n- 任务逾期预警\n- 需要生成进度报告",
        "inputs": "- 任务列表\n- 负责人\n- 截止时间\n- 当前进度\n- 飞书任务数据",
        "outputs": "```markdown\n## 任务跟踪报告\n\n### 总体进度\n### 逾期任务\n### 本周到期\n### 已完成\n### 阻塞项\n### 建议行动\n```",
        "workflow": "1. **拉取任务**：从飞书或任务系统\n2. **分类状态**：未开始 / 进行中 / 已完成 / 逾期\n3. **识别阻塞**：任务依赖、资源问题\n4. **提醒预警**：逾期前 1-3 天提醒\n5. **输出报告**：进度、风险、建议\n6. **推动闭环**：跟进逾期任务",
        "relations": "**被调用**：CEO Agent、task-planning\n\n**调用**：feishu-automation、meeting-summary",
        "dependencies": "- Tool: 飞书任务 API\n- Memory: 历史任务完成情况",
        "boundaries": "- 不替负责人完成任务\n- 提醒需适度，避免骚扰\n- 进度以负责人更新为准",
        "example": "输出：本周 12 个任务中 2 个逾期，3 个今日到期，已自动发送提醒给负责人"
    },
    {
        "path": "12-management/SOP-generation",
        "name": "SOP-generation",
        "title": "流程生成",
        "description": "把岗位经验和最佳实践沉淀为标准操作流程（SOP），提升执行一致性和培训效率。",
        "purpose": "- 将经验沉淀为 SOP\n- 规范操作流程\n- 降低对个人的依赖\n- 支持新人培训",
        "triggers": "- 完成重要任务后复盘\n- 发现流程混乱\n- 新人入职培训\n- 需要标准化操作",
        "inputs": "- 任务执行记录\n- 成功经验\n- 失败案例\n- 相关 Skill 文档",
        "outputs": "```markdown\n## SOP：{流程名称}\n\n### 目的\n### 适用范围\n### 角色与职责\n### 流程步骤\n### 验收标准\n### 常见问题\n### 相关模板\n```",
        "workflow": "1. **收集素材**：执行记录、案例、文档\n2. **梳理流程**：按时间线或决策点\n3. **定义角色**：谁做什么\n4. **明确标准**：输入、输出、验收\n5. **输出 SOP**：Markdown 格式\n6. **评审发布**：相关岗位确认\n7. **持续更新**：根据执行反馈优化",
        "relations": "**被调用**：knowledge-management、skill-improvement\n\n**调用**：knowledge-management、report-generation",
        "dependencies": "- Tool: 飞书文档、知识库\n- Memory: 最佳实践、失败案例",
        "boundaries": "- SOP 是指导不是枷锁\n- 需定期评审更新\n- 不替代人工判断",
        "example": "输出：《Amazon PPC 新品上架 SOP》，包含 12 步操作流程、验收标准和常见错误"
    },
    {
        "path": "12-management/performance-review",
        "name": "performance-review",
        "title": "绩效分析",
        "description": "分析团队和 Agent 的绩效指标，生成绩效报告和改进建议。",
        "purpose": "- 量化团队和 Agent 产出\n- 识别绩效瓶颈\n- 支持绩效评估\n- 输出改进计划",
        "triggers": "- 月度/季度绩效评估\n- 团队复盘\n- Agent 效果评估\n- 需要优化资源配置",
        "inputs": "- 任务完成数据\n- KPI 定义\n- 目标值\n- 历史绩效",
        "outputs": "```markdown\n## 绩效分析报告\n\n### KPI 完成情况\n### 同比/环比\n### 亮点与不足\n### 瓶颈分析\n### 改进建议\n### 下阶段目标\n```",
        "workflow": "1. **确定 KPI**：与目标对齐\n2. **收集数据**：任务、产出、质量、时效\n3. **计算达成率**：实际 vs 目标\n4. **多维分析**：人、Skill、项目\n5. **识别问题**：低效率、高错误、瓶颈\n6. **输出建议**：培训、流程优化、资源调整",
        "relations": "**被调用**：CEO Agent、task-followup\n\n**调用**：data-analysis、report-generation",
        "dependencies": "- Tool: 任务系统、数据分析工具\n- Memory: KPI 定义、历史绩效",
        "boundaries": "- 绩效分析需公平透明\n- 不用于惩罚，用于改进\n- 指标需与目标强相关",
        "example": "输出：market-agent 本月完成 8 份调研报告，平均交付时间 2.5 天，准确率 92%，建议优化数据清洗流程"
    },
    # 13-automation
    {
        "path": "13-automation/ecommerce-api",
        "name": "ecommerce-api",
        "title": "电商 API",
        "description": "连接 Amazon SP API、Shopify API、TikTok API 等电商平台接口，实现数据拉取和基础操作。",
        "purpose": "- 连接电商平台 API\n- 拉取订单、库存、广告数据\n- 执行基础写操作（如更新库存）\n- 为多平台同步提供数据基础",
        "triggers": "- 需要同步平台数据\n- 开发自动化流程\n- 对接新平台\n- 数据分析和报表",
        "inputs": "- API 凭证\n- 目标平台\n- 操作类型\n- 查询条件",
        "outputs": "```markdown\n## 电商 API 操作结果\n\n### 平台\n### 操作\n### 记录数\n### 状态\n### 错误信息\n### 下一步\n```",
        "workflow": "1. **认证连接**：OAuth 或 API key\n2. **读取数据**：订单、库存、产品、广告\n3. **数据转换**：统一字段格式\n4. **写回操作**：库存更新、价格更新（需确认）\n5. **错误处理**：限流、重试、告警\n6. **日志记录**：便于审计",
        "relations": "**被调用**：marketplace-sync、fulfillment-management、advertising-analysis\n\n**调用**：odoo-integration、feishu-automation",
        "dependencies": "- Tool: 各平台 API SDK\n- Memory: API 字段映射、限流规则",
        "boundaries": "- API 凭证安全存储\n- 写操作需人工确认或严格规则\n- 遵守平台 API 政策",
        "example": "输出：通过 Amazon SP API 拉取过去 30 天 1,200 条订单，同步至 Odoo Sales"
    },
    {
        "path": "13-automation/workflow-automation",
        "name": "workflow-automation",
        "title": "自动流程",
        "description": "编排跨 Skill、跨系统的自动化工作流，例如订单进入 → Odoo → 库存 → 物流 → 客服。",
        "purpose": "- 串联多个 Skill 和系统\n- 实现业务流程自动化\n- 减少重复人工操作\n- 提高响应速度",
        "triggers": "- 需要自动化某条业务流程\n- 多个系统需要协同\n- 人工操作重复且规则明确\n- 需要实时响应",
        "inputs": "- 流程定义\n- 触发条件\n- 涉及系统\n- 异常处理规则",
        "outputs": "```markdown\n## 自动化流程方案\n\n### 流程图\n### 触发条件\n### 执行步骤\n### 异常处理\n### 监控告警\n```",
        "workflow": "1. **梳理流程**：订单履约、补货、客服等\n2. **定义触发**：定时、事件、阈值\n3. **编排步骤**：调用各 Skill / API\n4. **设置分支**：正常 / 异常 / 人工介入\n5. **测试验证**：沙盒环境跑通\n6. **上线监控**：日志、告警、复盘",
        "relations": "**被调用**：CEO Agent、all operational Skills\n\n**调用**：odoo-integration、ecommerce-api、feishu-automation",
        "dependencies": "- Tool: 工作流引擎 / 脚本\n- Memory: 流程模板、异常案例",
        "boundaries": "- 关键决策点保留人工确认\n- 不处理高价值或高风险自动写操作\n- 流程变更需测试",
        "example": "输出：订单履约自动化流程 - 订单进入 → 同步 Odoo → 扣减库存 → 推送到仓库 → 获取追踪号 → 通知客服跟进"
    },
    {
        "path": "13-automation/feishu-automation",
        "name": "feishu-automation",
        "title": "飞书自动化",
        "description": "连接飞书，实现创建审批、写入表格、推送消息、同步任务等自动化操作。",
        "purpose": "- 发送通知和告警\n- 创建审批流\n- 写入飞书表格\n- 同步任务和会议纪要",
        "triggers": "- 需要推送业务通知\n- 自动化审批\n- 数据同步到飞书\n- 任务提醒",
        "inputs": "- 飞书配置\n- 消息内容\n- 接收人\n- 表格/文档 ID",
        "outputs": "```markdown\n## 飞书自动化结果\n\n### 操作类型\n### 目标对象\n### 状态\n### 错误信息\n```",
        "workflow": "1. **配置连接**：飞书 app_id、app_secret\n2. **选择操作**：消息、审批、表格、文档\n3. **组装数据**：按 API 格式\n4. **执行操作**：调用飞书 API\n5. **处理异常**：重试、告警\n6. **记录日志**：便于审计",
        "relations": "**被调用**：workflow-automation、report-generation、task-followup\n\n**调用**：无",
        "dependencies": "- Tool: 飞书开放平台 API\n- Memory: 飞书配置、常用群聊/文档",
        "boundaries": "- 不发送垃圾消息\n- 敏感审批需人工复核\n- API 调用需控制频率",
        "example": "输出：每日 8:30 自动推送经营看板到飞书群，包含 GMV、利润、库存、广告 4 个核心指标"
    },
    # 14-learning-memory
    {
        "path": "14-learning-memory/memory-manager",
        "name": "memory-manager",
        "title": "经验管理",
        "description": "管理 Agent 的执行经验，包括保存、检索、更新和归档，让 Agent 能力持续提升。",
        "purpose": "- 保存 Agent 执行经验\n- 支持经验检索和复用\n- 管理记忆生命周期\n- 为 Skill 改进提供数据",
        "triggers": "- 任务完成后\n- 需要查找历史经验\n- 记忆过多需要清理\n- Skill 改进时",
        "inputs": "- 任务结果\n- 执行日志\n- 成功/失败标记\n- 经验内容",
        "outputs": "```markdown\n## 记忆管理报告\n\n### 新增记忆\n### 更新记忆\n### 检索结果\n### 记忆质量评估\n```",
        "workflow": "1. **提取经验**：从任务中提炼有价值信息\n2. **结构化存储**：标签、领域、类型\n3. **索引管理**：便于检索\n4. **定期清理**：删除过时记忆\n5. **检索复用**：新任务匹配历史经验\n6. **反馈更新**：根据效果更新记忆",
        "relations": "**被调用**：knowledge-management、skill-improvement\n\n**调用**：knowledge-curator",
        "dependencies": "- Tool: 记忆存储（文件/向量库）\n- Memory: 记忆索引",
        "boundaries": "- 不保存敏感信息\n- 记忆需标注置信度\n- 定期验证记忆有效性",
        "example": "输出：将 'TikTok 宠物饮水机场景视频 CTR 高' 保存为记忆，供后续 content-agent 调用"
    },
    {
        "path": "14-learning-memory/knowledge-curator",
        "name": "knowledge-curator",
        "title": "知识整理",
        "description": "整理和分类知识库内容，建立知识图谱，提升知识的可发现性和可用性。",
        "purpose": "- 整理碎片化知识\n- 建立知识结构\n- 维护知识库索引\n- 提升知识检索效率",
        "triggers": "- 知识库内容增多\n- 需要更新知识架构\n- 检索效率低\n- 需要建立知识体系",
        "inputs": "- 知识条目\n- 分类体系\n- 用户需求\n- 使用数据",
        "outputs": "```markdown\n## 知识整理报告\n\n### 知识分类\n### 索引更新\n### 关联关系\n### 缺失知识\n### 推荐补充\n```",
        "workflow": "1. **收集知识**：经验、SOP、案例、模板\n2. **分类打标签**：领域、类型、场景\n3. **建立关联**：相似、因果、依赖\n4. **更新索引**：目录、关键词\n5. **清理冗余**：合并重复、删除过时\n6. **输出地图**：知识图谱或目录",
        "relations": "**被调用**：knowledge-management、memory-manager\n\n**调用**：无",
        "dependencies": "- Tool: 知识库、向量检索\n- Memory: 知识分类体系",
        "boundaries": "- 不删除未经确认的知识\n- 分类需符合业务逻辑\n- 保持知识更新",
        "example": "输出：整理出 5 大知识领域、32 个子类，建立经验-SOP-模板三级结构"
    },
    {
        "path": "14-learning-memory/skill-improvement",
        "name": "skill-improvement",
        "title": "自我优化",
        "description": "分析任务失败原因和 Skill 使用效果，提出 Skill 改进方案，驱动 Agent 能力进化。",
        "purpose": "- 分析 Skill 执行失败原因\n- 评估 Skill 效果\n- 提出改进建议\n- 推动 Skill 迭代",
        "triggers": "- 任务频繁失败\n- Skill 效果不佳\n- 定期 Skill 复盘\n- 用户反馈 Skill 问题",
        "inputs": "- Skill 执行日志\n- 任务结果\n- 用户反馈\n- 成功率数据",
        "outputs": "```markdown\n## Skill 改进报告\n\n### Skill 名称\n### 问题描述\n### 失败原因分析\n### 改进建议\n### 优先级\n### 验证方案\n```",
        "workflow": "1. **收集反馈**：失败案例、用户反馈、效果数据\n2. **根因分析**：提示词、边界、依赖、数据\n3. **提出改进**：修改 Skill、增加示例、优化流程\n4. **优先级排序**：影响范围、成本、收益\n5. **验证测试**：小范围测试改进效果\n6. **发布更新**：更新 SKILL.md 和相关文件",
        "relations": "**被调用**：knowledge-management、CEO Agent\n\n**调用**：memory-manager、knowledge-curator",
        "dependencies": "- Tool: 日志分析、版本控制\n- Memory: Skill 历史版本、改进记录",
        "boundaries": "- 不擅自修改生产环境 Skill\n- 改进需测试验证\n- 重大变更需人工确认",
        "example": "输出：advertising-analysis 对 Amazon SB 广告支持不足，建议新增 Sponsored Brands 报告解析模块"
    }
]


def main():
    for skill in SKILLS:
        dir_path = BASE_DIR / skill["path"]
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "SKILL.md"
        content = SKILL_TEMPLATE.format(**skill)
        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_path}")


if __name__ == "__main__":
    main()
