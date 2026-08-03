---
name: seo-keyword
description: 关键词分析 Skill。输出核心词、长尾词、竞争词，分析搜索量、竞争度、相关性，为 Listing 和广告提供关键词策略。
---

# seo-keyword · 关键词分析

找到买家真正搜的词。

## 用途

- 挖掘核心关键词
- 发现长尾关键词
- 分析关键词搜索量和竞争度
- 识别广告高转化词
- 为 Listing 埋词和广告选词提供策略

## 触发场景

- 新品上架前做关键词研究
- Listing 优化需要关键词布局
- 广告投放前选词
- 竞品流量词反查

## 输入

- 产品名称 / 品类
- 种子关键词
- 目标市场
- 竞品 ASIN（可选）
- 平台（Amazon / Google / TikTok）

## 输出

```markdown
## 关键词分析报告：{产品}

### 核心词
| 关键词 | 搜索量 | 竞争度 | 相关性 | 建议用途 |

### 长尾词
| 关键词 | 搜索量 | 竞争度 | 转化潜力 | 建议用途 |

### 竞品流量词
### 否定词建议
### 关键词布局策略
```

## 工作流

1. **种子词扩展**：基于产品功能和场景扩展同义词、变体、长尾。
2. **数据获取**：搜索量、竞争度、CPC 估算。
3. **相关性评分**：与产品匹配度打分。
4. **分类标签**：
   - 核心词：高搜索、高竞争
   - 长尾词：低搜索、高转化
   - 品牌词：竞品 / 自有品牌
   - 否定词：不相关 / 低转化
5. **输出策略**：Listing 埋词 + 广告分组 + 否定词。

## 调用关系

**被调用**：amazon-operation、listing-writing、advertising-analysis

**调用**：competitor-analysis、market-research

## 依赖工具 / Memory

- Tool: 第三方关键词工具（Helium 10 / Jungle Scout / 卖家精灵等，如接入）
- Memory: 历史高转化词、行业词库

## 边界与限制

- 关键词数据为估算，需结合实际广告表现验证
- 不保证排名，只提供策略
- 平台算法变化需持续更新

## 示例

输入：美国亚马逊宠物饮水机
输出：核心词 pet water fountain、长尾词 automatic cat water fountain stainless steel、否定词 free / DIY / homemade
