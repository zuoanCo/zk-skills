---
name: listing-writing
description: Listing 文案 Skill。生成电商商品详情页内容，包括标题、五点描述、SEO 描述、A+ 文案，适配 Amazon / Shopify / TikTok 等平台。
---

# listing-writing · Listing 文案

让产品页自己会卖货。

## 用途

- 生成平台适配的商品标题
- 撰写五点描述（Bullet Points）
- 生成 SEO 长描述 / 产品故事
- 输出 A+ 页面文案
- 支持多平台（Amazon / Shopify / TikTok Shop）

## 触发场景

- 新品上架需要 Listing 文案
- 老品 Listing 转化率低需要重写
- 多平台同步需要本地化文案
- A/B 测试需要多版文案

## 输入

- 产品基础信息（名称、规格、功能、材质）
- 目标用户画像
- 差异化卖点
- 关键词列表
- 平台要求（Amazon / Shopify / TikTok）
- 竞品文案参考
- 品牌调性

## 输出

```markdown
## {产品} Listing 文案

### 标题
### 五点描述
1. ...
2. ...

### SEO 描述
### A+ 模块文案
### 关键词布局
### 平台适配说明
```

## 工作流

1. **理解产品**：功能、规格、用户、场景。
2. **研究竞品**：提炼类目文案套路。
3. **埋入关键词**：核心词 + 长尾词自然分布。
4. **撰写文案**：
   - 标题：核心词 + 卖点 + 规格，符合平台长度
   - 五点：每点一个卖点，前 3 点放核心差异
   - 描述：讲故事 + 解决顾虑 + 使用场景
   - A+：模块化，图文配合
5. **本地化润色**：避免直译，符合当地表达习惯。
6. **输出多版本**：主版本 + 测试版本。

## 调用关系

**被调用**：amazon-operation、shopify-operation、localization

**调用**：seo-keyword、product-positioning、image-prompt

## 依赖工具 / Memory

- Memory: 品牌话术库、高转化文案模板、平台政策
- Tool: 翻译 / 本地化工具

## 边界与限制

- 不使用违禁词、夸大宣传、侵权词汇
- 文案需人类审校后上架
- 平台政策变化需同步更新

## 示例

输入：宠物智能饮水机，目标美国，核心词 pet water fountain
输出：200 字符标题 + 5 点卖点 + SEO 描述 + A+ 模块大纲
