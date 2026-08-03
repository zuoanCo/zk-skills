---
name: image-prompt
description: 为主图、场景图、A+ 页面生成 AI 图片提示词，配合 image-gen Skill 出图。
---

# image-prompt · AI 图片生成

## 用途
- 生成电商主图提示词
- 生成场景图、生活方式图提示词
- 生成 A+ 页面配图提示词
- 保持视觉风格一致

## 触发场景
- 新品上架需要图片
- 老品图片 CTR 低
- A+ 页面需要配图
- 广告素材测试需要多版本图片

## 输入
- 产品信息
- 目标用户
- 使用场景
- 图片类型（主图/场景图/A+）
- 风格要求

## 输出
```markdown
## AI 图片生成方案

### 主图提示词
### 场景图提示词
### A+ 配图提示词
### 风格参考
### 尺寸要求
```

## 工作流
1. **确定图片目标**：主图、场景图、A+
2. **提取产品卖点**：功能、材质、使用方式
3. **设计场景**：用户、环境、情绪
4. **编写提示词**：主体、风格、光线、构图
5. **调用 image-gen**：批量生成
6. **筛选优化**：A/B 测试

## 调用关系
**被调用**：listing-writing、amazon-operation、creative-testing

**调用**：image-gen（外部 Skill）

## 依赖工具 / Memory
- Tool: image-gen Skill
- Memory: 高 CTR 图片风格、品牌视觉规范

## 边界与限制
- 不生成虚假或误导性图片
- 模特、宠物等需考虑版权
- 图片需符合平台规范

## 示例
输出：主图提示词 'A stainless steel cat water fountain on a clean white background, soft studio lighting, a fluffy cat drinking from it, professional product photography, 4K'
