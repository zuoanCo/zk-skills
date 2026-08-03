# 任务规划示例

## 示例 1：选品任务规划

### 输入

> 老板：找一个适合美国市场的宠物产品，预算 5 万美金，3 周内要结果。

### 输出

```yaml
任务:
  目标: 在美国宠物市场找到 1-3 个高潜力产品，完成可行性评估和启动方案
  约束:
    - 预算: 50,000 USD
    - 时间: 3 周
  子任务:
    - 编号: 1
      名称: 美国宠物市场趋势扫描
      负责 Agent: market-agent
      调用 Skill: market-research
      输入:
        市场: 美国
        品类: 宠物用品
        数据源: [Google Trends, Amazon Best Seller, TikTok]
      输出: 宠物品类 Top 10 趋势清单
      验收标准: 提供搜索量趋势、市场规模估算、增长率
      依赖: []

    - 编号: 2
      名称: 竞品深度分析
      负责 Agent: market-agent
      调用 Skill: competitor-analysis
      输入:
        品类: 宠物智能饮水/喂食
        竞品数量: 5-10
      输出: 竞品 ASIN 分析报告
      验收标准: 包含价格、评分、差评关键词、卖点
      依赖: [1]

    - 编号: 3
      名称: 选品评分
      负责 Agent: product-agent
      调用 Skill: product-selection
      输入:
        候选产品: 来自子任务 1
        竞品数据: 来自子任务 2
      输出: 选品评分表（Top 3）
      验收标准: 综合得分 ≥ 70
      依赖: [1, 2]

    - 编号: 4
      名称: 供应链初筛
      负责 Agent: sourcing-agent
      调用 Skill: supplier-search
      输入:
        产品: Top 3 选品
        首单 MOQ: ≤1000
        认证: FDA / CE / FCC
      输出: 每款产品 2-3 家候选供应商
      验收标准: 供应商有认证、交期 ≤30 天
      依赖: [3]

    - 编号: 5
      名称: 利润测算
      负责 Agent: finance-agent
      调用 Skill: profitability-analysis
      输入:
        产品: Top 3 选品
        成本: 来自子任务 4 报价
        售价: 来自子任务 2 竞品价格
      输出: SKU 级利润预测
      验收标准: 毛利率 ≥ 30%
      依赖: [2, 4]

    - 编号: 6
      名称: 决策建议报告
      负责 Agent: ceo-agent
      调用 Skill: decision-analysis
      输入:
        选品评分: 来自子任务 3
        利润预测: 来自子任务 5
      输出: 最终推荐产品 + 启动方案
      验收标准: 包含 SWOT、风险、下一步行动
      依赖: [3, 5]

  执行策略: 混合
  整体验收标准: 3 周内输出可落地的产品推荐和采购启动方案
```

## 示例 2：Listing 优化任务规划

### 输入

> ASIN B08XXXXXX 最近销量下滑 30%，帮我诊断并优化。

### 输出

```yaml
任务:
  目标: 诊断 ASIN B08XXXXXX 销量下滑原因并输出优化方案
  子任务:
    - 编号: 1
      名称: Listing 健康度诊断
      负责 Agent: amazon-agent
      调用 Skill: amazon-operation
      输出: Listing 评分和优化点

    - 编号: 2
      名称: 竞品 Listing 对比
      负责 Agent: amazon-agent
      调用 Skill: competitor-analysis
      输出: 竞品标题、五点、图片、价格对比
      依赖: [1]

    - 编号: 3
      名称: 关键词排名分析
      负责 Agent: amazon-agent
      调用 Skill: seo-keyword
      输出: 关键词排名变化、流量词流失
      依赖: [1]

    - 编号: 4
      名称: 广告诊断
      负责 Agent: growth-agent
      调用 Skill: advertising-analysis
      输出: ACOS、TACOS、高 spend 低转化词
      依赖: [1]

    - 编号: 5
      名称: 生成优化后 Listing
      负责 Agent: content-agent
      调用 Skill: listing-writing
      输出: 新标题、五点、描述
      依赖: [2, 3]

  执行策略: 串行 → 并行优化
  整体验收标准: 输出可直接上架的 Listing 优化方案和广告调整建议
```
