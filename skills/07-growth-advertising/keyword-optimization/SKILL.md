---
name: keyword-optimization
description: 持续优化广告关键词，包括拓词、否定词、出价调整、匹配方式优化，提升广告效率。
---

# keyword-optimization · 关键词优化

## 用途
- 扩展高转化关键词
- 添加否定词减少浪费
- 优化关键词出价
- 调整匹配方式

## 触发场景
- 广告 ACOS 过高
- Search Term Report 更新
- 需要拓词
- 发现高 spend 低转化词

## 输入
- Search Term Report
- 广告表现数据
- 关键词排名
- 竞品关键词

## 输出
```markdown
## 关键词优化方案

### 新增关键词
### 否定词建议
### 出价调整
### 匹配方式调整
### 预期效果
```

## 工作流
1. **数据清洗**：整理 Search Term Report
2. **识别高转化词**：高销售、低 ACOS
3. **识别浪费词**：高 spend、低转化
4. **拓词**：从竞品、长尾、相关搜索扩展
5. **优化出价**：升降出价、调整匹配
6. **输出方案**：新增、否定、调价清单

## 调用关系
**被调用**：advertising-analysis、campaign-management

**调用**：seo-keyword、competitor-analysis

## 依赖工具 / Memory
- Tool: 广告平台报告
- Memory: 历史关键词表现、否定词库

## 边界与限制
- 只输出优化建议，不直接修改广告
- 否定词需避免误伤
- 大词调整需谨慎

## 示例
输出：新增 8 个长尾词，否定 12 个宽泛词，3 个核心词提价 15%，预计 ACOS 降 5pp
