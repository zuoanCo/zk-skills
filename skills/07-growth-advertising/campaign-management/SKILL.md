---
name: campaign-management
description: 制定、执行和优化广告投放计划，管理预算、出价、受众和素材组合。
---

# campaign-management · 广告计划

## 用途
- 制定广告投放计划
- 管理广告预算分配
- 优化出价策略
- 协调多平台广告投放

## 触发场景
- 新品上线需要广告计划
- 大促需要预算规划
- 广告表现需要优化
- 需要测试新渠道

## 输入
- 广告目标（销售、曝光、转化）
- 预算
- 目标受众
- 产品信息
- 历史广告数据

## 输出
```markdown
## 广告计划

### 目标与 KPI
### 预算分配
### Campaign 结构
### 出价策略
### 素材计划
### 测试计划
### 优化节奏
```

## 工作流
1. **明确目标**：销售、品牌、拉新
2. **预算分配**：按平台、产品、漏斗阶段
3. **Campaign 结构**：品牌、品类、竞品、再营销
4. **出价策略**：自动、手动、目标 ACOS/ROAS
5. **素材计划**：图片、视频、文案版本
6. **上线与监控**：每日检查、每周优化
7. **复盘迭代**：数据复盘、策略调整

## 调用关系
**被调用**：amazon-operation、shopify-operation、tiktok-shop-operation

**调用**：advertising-analysis、creative-testing、seo-keyword

## 依赖工具 / Memory
- Tool: 广告平台 API
- Memory: 历史广告计划、最佳实践

## 边界与限制
- 只输出计划建议，不直接操作广告账户
- 预算调整需人工确认
- 不承诺具体 ROAS

## 示例
输出：新品首月预算 $3000，70% 放 Amazon PPC（核心词 + 长尾词），30% 放 TikTok Spark Ads，目标 ACOS 30%
