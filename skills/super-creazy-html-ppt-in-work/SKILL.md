---
name: super-creazy-html-ppt-in-work
description: 高端HTML幻灯片生成器；智能主题匹配；SVG图标与插画系统；玻璃态/新拟态/极简多风格；粒子背景与几何图案；图片配图与背景融合；8种布局×30+动画×10+主题；16:9演示优化
---

# 高端 HTML 幻灯片演示生成器

将用户提供的内容智能转换为专业级 HTML 幻灯片演示文稿。不是用脚本生成，而是由 AI 直接编写完整的单文件 HTML，确保每一页幻灯片的设计都与内容完美匹配。

> **重要参考文件**：`references/code-templates.md` 包含完整的 HTML 骨架、8种布局的 HTML 模板、40+ 个 SVG 图标代码、12 种主题的完整 CSS 变量、粒子背景 JS、页面切换动画 CSS 等可复用代码。编写幻灯片时必须对照此文件中的模板。

## 核心设计哲学

1. **内容决定设计** — 先理解内容属性（严肃/活泼/科技/自然/商务），再选择主题与风格
2. **内容为王** — 每页必须有充实的内容，文字量充足，不能空洞；页面要撑满视口
3. **克制而精致** — 动画不是为了炫技，而是引导视线、强调重点
4. **SVG 仅作图标** — SVG 严格用于小尺寸标识性图标（徽章图标、卡片图标、按钮图标），**绝不用于叙事性插画或占位图**。叙事靠文字和真实配图
5. **图片即叙事** — 除封面外，至少 50% 的幻灯片需要生成配图（背景图或内容配图），图片要大、要撑满
6. **16:9 优先** — 专为演示场景优化，支持全屏播放
7. **独立文件** — 单 HTML 文件包含所有 CSS/JS/SVG，无外部依赖（字体除外）

---

## 内容密度强制规范

> **这是最重要的规范。内容空洞是幻灯片的第一大忌。**

### 每页内容最低要求

| 布局类型 | 最低文字量 | 最低信息点 | 必须包含 |
|----------|-----------|-----------|----------|
| poster（封面） | 标题 ≥6 字 + 副标题 ≥12 字 | 标题+副标题+日期/标签 | 全屏背景大图 |
| hero-split（左右分栏） | 标题 ≥6 字 + 描述 ≥40 字 | 标题+描述+≥3 条要点 | 右侧配图 |
| grid-cards（卡片网格） | 每卡标题 ≥4 字 + 描述 ≥20 字 | ≥3 张卡片，每卡有图 | 每卡配图或大背景图 |
| stats-dashboard（数据） | 每项标签 ≥4 字 + 说明 ≥12 字 | ≥3 项数据 | 图表或配图 |
| timeline（时间线） | 每节点标题 ≥4 字 + 描述 ≥16 字 | ≥3 个时间节点 | 背景配图 |
| quote-spotlight（语录） | 引文 ≥15 字 + 作者信息 | 引言+作者+出处 | 氛围背景图 |
| comparison（对比） | 每列 ≥3 条对比要点 | ≥3 条对比维度 | 每列可配图 |
| gallery（画廊） | 每张图有标题 ≥4 字 | ≥4 张配图 | 大量配图 |

### 内容密度铁律

- **禁止**一句话就撑起一页幻灯片
- **禁止**卡片描述只有 3-5 个字（如"快速响应"就完了）
- 每个卡片/节点的描述要有实质性内容，至少一句话完整说明
- 描述文字要让观众获得新认知，而不是喊口号
- 页面内容区域（content-wrapper）应占据视口 **≥70%** 的面积

---

## 图片使用强制规范

> **SVG 不等于图片。绝大多数叙事场景必须使用真实配图。**

### SVG 与图片的严格分工

| 用途 | SVG | 生成图片 |
|------|:---:|:---:|
| 小尺寸图标（≤48px，徽章/按钮/卡片头部） | ✅ | ❌ |
| 叙事性配图（场景、产品、人物、氛围） | ❌ | ✅ |
| 占位插图（"右半部分放个图"） | ❌ | ✅ |
| 装饰性大图形（>80px） | ❌ | ✅ |
| 背景（封面/全页氛围） | ❌ | ✅ |
| 数据图表 | ❌ | ✅ |
| 卡片内的配图 | ❌ | ✅ |

### 配图生成策略

编写幻灯片时，必须在动手写 HTML 之前先规划好配图列表：

```
每页配图决策：
- poster 封面页     → 必须生成 1 张全屏背景图
- hero-split 分栏页  → 必须生成 1 张右侧配图
- grid-cards 卡片页  → 若有 3 张卡片，生成 3 张对应配图；或生成 1 张大背景图
- stats 数据页      → 可配 1 张背景图或无图（几何图案背景）
- timeline 时间线页  → 必须生成 1 张氛围背景图
- quote 语录页       → 必须生成 1 张氛围背景图
- comparison 对比页  → 可配 2 张对应配图
- gallery 画廊页     → 生成 ≥4 张配图
```

使用 `mcp__gpt-image__generate_image` 工具逐一生成配图后再编写 HTML。

### 图片展示规则

- **大图撑满**：内容配图应占据所在容器的全部空间，图片 `width: 100%; height: 100%; object-fit: cover;`
- **无框无边**：图片不需要 border，不需要圆角包裹（或仅用极小圆角 4-8px）
- **不要玻璃态包裹图片**：图片本身是视觉重点，不要套 glass-card 样式
- **图片容器不设 max-width 小值**：配图容器宽度应撑满（如 `flex: 1` 而非 `max-width: 400px`）
- **封面图必须全屏**：position: absolute; inset: 0; 覆盖整个视口
- **图片上的文字必须有遮罩**：`background: linear-gradient(...)` 半透明遮罩确保可读

---

## 第一步：内容分析与主题匹配

在编写任何代码之前，先分析用户提供的内容：

### 内容属性判断

```
内容类型 → 主题方向
─────────────────────────
科技/AI/数据    → cyber, midnight
自然/环保/农业  → forest, earth
商务/金融/企业  → elegant, slate
创意/设计/艺术  → aurora, prism
医疗/健康/生命  → ocean, calm
教育/人文/历史  → warm, classic
产品发布/营销   → aurora, sunset
```

### 自动决策流程

1. 扫描用户输入的关键词
2. 判断内容情感倾向（激动人心/严肃专业/温暖亲切）
3. 选择合适的主题色彩体系
4. 决定设计风格（玻璃态/极简/新拟态/经典）
5. 为每页内容选择最佳布局

---

## 第二步：主题系统

### 内置 12 种主题

| 主题 | 主色 | 辅色 | 强调色 | 背景 | 风格 |
|------|------|------|--------|------|------|
| midnight | #6366f1 | #8b5cf6 | #a78bfa | #0a0a0f | 深色科技 |
| aurora | #0ea5e9 | #06b6d4 | #22d3ee | #0c1929 | 极光蓝 |
| elegant | #18181b | #27272a | #52525b | #fafafa | 浅色商务 |
| sunset | #f97316 | #ef4444 | #fbbf24 | #1a0a0a | 暖色活力 |
| forest | #22c55e | #10b981 | #34d399 | #0a1a0f | 自然绿 |
| ocean | #3b82f6 | #0ea5e9 | #38bdf8 | #0c1222 | 海洋蓝 |
| rose | #e11d48 | #f43f5e | #fda4af | #1a0a10 | 玫瑰粉 |
| cyber | #00ff88 | #00e5ff | #76ff03 | #0a0a0a | 赛博朋克 |
| earth | #92400e | #b45309 | #d97706 | #1a1008 | 大地棕 |
| prism | #a855f7 | #ec4899 | #f97316 | #0f0a1a | 多彩创意 |
| calm | #0891b2 | #06b6d4 | #67e8f9 | #0a1820 | 宁静青 |
| slate | #334155 | #475569 | #94a3b8 | #0f172a | 石板灰 |

### 每种主题提供

- 12 个 CSS 变量完整定义
- 玻璃态（glassmorphism）参数
- 渐变预设（3-5 组）
- 适合的字体组合建议
- 背景图案/纹理建议

> **代码模板**：`references/code-templates.md` → "主题完整 CSS 变量" 章节包含全部 12 种主题的 `:root { }` 变量块，直接复制使用。

---

## 第三步：设计风格系统

### A. 玻璃态（Glassmorphism）— 默认推荐

```css
.glass-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
```

### B. 新拟态（Neumorphism）— 浅色主题适用

```css
.neumorphic {
  background: #f0f0f3;
  border-radius: 24px;
  box-shadow: 8px 8px 16px #d1d1d4, -8px -8px 16px #ffffff;
}
```

### C. 极简线条（Minimalist）— 商务场景

```css
.minimal-card {
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 2rem;
}
```

### D. 投影片（Projector）— 经典演示

```css
.projector-slide {
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  /* 大标题 + 内容区的经典布局 */
}
```

---

## 第四步：布局类型（8 种）

> **代码模板**：`references/code-templates.md` → "布局模板" 章节包含全部 8 种布局的完整 HTML 代码（poster、hero-split、grid-cards、stats-dashboard、timeline、quote-spotlight、comparison、gallery），直接复制并替换内容即可。

### 1. poster — 全屏海报封面
- 超大标题（clamp 3rem-6rem）
- 可选：徽章(badge)、CTA按钮
- 可选：背景大图/渐变
- 副标题、日期、演讲者信息

### 2. hero-split — 左右分栏
- 左侧：标题 + 描述 + CTA（40-50%）
- 右侧：大图/SVG插画/数据可视化（50-60%）
- 适合：产品介绍、概念说明

### 3. grid-cards — 卡片网格
- 2×2 / 2×3 / 3×3 网格
- 每张卡片：SVG图标 + 标题 + 描述
- 悬停微交互（上浮+阴影+边框光晕）
- 适合：功能展示、服务介绍

### 4. stats-dashboard — 数据仪表盘
- 大数字（clamp 2.5rem-5rem）
- 趋势箭头、对比标签
- 可选迷你柱状图/进度环
- 适合：数据报告、成绩展示

### 5. timeline — 时间线
- 横向或纵向时间轴
- 节点：年份/里程碑图标
- 连接线带渐变动画
- 适合：发展历程、项目规划

### 6. quote-spotlight — 语录聚焦
- 巨大引号 SVG 装饰
- 引文居中大字
- 作者信息 + 头像占位
- 背景可配氛围图

### 7. comparison — 对比展示
- 左右/上下对比
- Before/After、方案A vs 方案B
- 表格或卡片形式
- 差异高亮标注

### 8. gallery — 图文画廊
- 图片网格或轮播
- 每张图有标题覆盖层
- 支持点击放大
- 适合：作品集、产品展示

---

## 第五步：SVG 图标（仅限标识性图标）

> **代码模板**：`references/code-templates.md` → "SVG 图标模板" 章节包含全部 40+ 个图标的完整 `<svg>` 代码。

### 严格使用边界

SVG 图标 **只能**出现在以下位置，尺寸 **不得超过 48px**：

| 允许位置 | 示例 | 最大尺寸 |
|----------|------|----------|
| 页面顶部标签/badge | 徽章旁的小图标 | 18-20px |
| 卡片头部标识 | 功能卡片顶部圆形图标 | 24-36px |
| 按钮内 | CTA 按钮箭头 | 18-20px |
| 列表要点前导 | 要点左侧标记 | 18-20px |
| 导航箭头 | 翻页按钮 | 24px |
| 数据指标标识 | 数据卡片标签旁 | 24px |

### 禁止的 SVG 用法

- ❌ **禁止**用 SVG 作为卡片/内容区的"配图"（如给"赛龙舟"卡片放一个龙舟 SVG 大图）
- ❌ **禁止**用 SVG 填充 hero-split 布局的"右侧图片区"
- ❌ **禁止**用 SVG 作为页面主体视觉元素（>80px）
- ❌ **禁止**用多个 SVG 组成"插画"来替代配图

### 卡片配图正确做法

当 grid-cards 布局的每张卡片需要视觉元素时：

```
正确：为每张卡片生成一张对应的配图（使用 generate_image）
      → 图片放在卡片顶部，占卡片 50-60% 面积
      → 图片下方是图标（24px SVG）+ 标题 + 描述

错误：在卡片里放一个 64px 的 SVG 大图标充当"配图"
      → 这会让卡片看起来像低保真线框图
```

### 内置图标集（40+，仅限 ≤48px 标识用途）

```
通用：arrow-right, arrow-left, arrow-down, arrow-up, check, x, plus, minus
导航：chevron-right, chevron-left, chevron-up, chevron-down, home, menu
商业：briefcase, building, chart-bar, chart-line, trending-up, trending-down
科技：cpu, code, database, server, cloud, wifi, bluetooth, zap, shield
媒体：play, pause, music, camera, image, film, video
通信：mail, message-circle, phone, send, share, bell
文档：file-text, folder, book, bookmark, edit, copy, clipboard
人物：user, users, smile, heart, star, award, crown
自然：sun, moon, leaf, flower, mountain, globe, compass
```

---

## 第六步：背景系统（多样性强制要求）

> **绝对不能所有页面用同一个背景！每页背景必须有差异。**

### 每页背景差异化方案

为 6 页幻灯片设计背景的典型方案：

| 页码 | 背景类型 | 说明 |
|------|----------|------|
| 封面 | 全屏生成图片 + 半透明遮罩 | 视觉冲击力最强 |
| 内容页1 | 生成图片背景 + 模糊 + 强遮罩 | 文字主导但图片烘托氛围 |
| 内容页2 | 几何图案 + 光斑 + 主题色渐变 | 纯 CSS，突出卡片内容 |
| 内容页3 | 不同生成图片背景 + 玻璃态卡片 | 与前页图片不同，分隔内容 |
| 内容页4 | 主题色渐变 + 粒子/网格 + 光斑变色 | CSS 背景，与前页区分 |
| 结束页 | 与封面呼应的生成图片背景 | 首尾呼应 |

### 背景差异化铁律

- **绝对禁止**所有页面用同一张背景图
- **绝对禁止**所有页面用同一个纯色渐变
- **绝对禁止**光斑色彩和位置不变贯穿所有页面
- 每页背景的色调、明暗、纹理至少有 30% 的差异
- 如果连续两页都是图片背景，图片主题应明显不同
- 光斑的大小、颜色、位置应每页改变

---

## 第七步：动画系统

> **代码模板**：`references/code-templates.md` → "页面切换动画 CSS" 章节包含完整的关键帧定义和过渡 CSS；"粒子背景 JS" 包含 Canvas 粒子系统。<br>
> **HTML 骨架中的动画引擎**：`references/code-templates.md` → "完整 HTML 骨架" 中的 `<script>` 部分包含完整的幻灯片切换 JS 引擎（goTo、updateNav、键盘/触摸/滚轮事件）。

### 页面切换动画（精选 20 种）

| 动画 | 效果描述 | 适用场景 |
|------|----------|----------|
| fade | 淡入淡出 0.5s | 通用 |
| slide | 水平滑动 0.5s | 流程推进 |
| slideUp | 垂直上滑 0.5s | 层级递进 |
| zoom | 缩放 0.6s | 重点强调 |
| zoomBlur | 缩放+模糊 0.7s | 场景转换 |
| flip | 3D翻转 0.6s | 视角转换 |
| flip3d | 全3D翻转 0.7s | 重大转折 |
| rotateIn | 旋转入场 0.6s | 创意内容 |
| elastic | 弹性缩放 0.7s | 活力内容 |
| bounce | 弹跳入场 0.6s | 轻快内容 |
| blur | 模糊消散 0.6s | 氛围转换 |
| glitch | 故障艺术 0.5s | 科技/赛博 |
| curtain | 幕布拉开 0.8s | 开场/揭幕 |
| wipe | 擦拭效果 0.6s | 清洁/刷新 |
| cube | 立方体旋转 0.7s | 3D叙事 |
| door | 开门效果 0.7s | 进入新篇章 |
| newspaper | 报纸展开 0.7s | 新闻/资讯 |
| swing | 摇摆入场 0.6s | 轻松活泼 |
| fold | 折叠过渡 0.6s | 层次变化 |
| morph | 形态过渡 0.8s | 概念演变 |

### 内容入场动画（精选 16 种）

| 动画 | 效果 | 延迟策略 |
|------|------|----------|
| fadeIn | 淡入 opacity 0→1 | 子元素 0.1s 递增 |
| slideUp | 下→上 40px + 淡入 | 子元素 0.12s 递增 |
| slideDown | 上→下 40px + 淡入 | 子元素 0.12s 递增 |
| slideLeft | 右→左 40px + 淡入 | 子元素 0.12s 递增 |
| slideRight | 左→右 40px + 淡入 | 子元素 0.12s 递增 |
| scaleUp | scale 0.85→1 + 淡入 | 子元素 0.15s 递增 |
| zoomIn | scale 0.3→1 弹性 | 子元素 0.1s 递增 |
| rotateIn | rotate -15deg + 淡入 | 子元素 0.12s 递增 |
| flipX | rotateY 90deg→0 | 子元素 0.12s 递增 |
| flipY | rotateX 90deg→0 | 子元素 0.12s 递增 |
| bounce | Y位移+回弹曲线 | 子元素 0.15s 递增 |
| blurIn | blur 20px→0 + 淡入 | 子元素 0.15s 递增 |
| elastic | scaleX弹性变形 | 子元素 0.1s 递增 |
| morph | clip-path 展开 | 子元素 0.12s 递增 |
| staggerFade | 逐个淡入+位移 | 内置间隔 0.1s |
| drawLine | SVG 描边动画 | 单元素 0.8-1.5s |

### 微交互

- 按钮悬停：scale(1.03) + 阴影扩散 + 0.2s
- 卡片悬停：translateY(-4px) + 边框光晕 + 0.3s
- 图标悬停：轻微旋转或脉冲
- 数据数字：count-up 动画（如果有意义）
- 进度条/环：入场时从 0 动画到目标值

---

## 第八步：排版系统

### 字体层级

```css
--font-display: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
--font-body: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

/* 字号层级（16:9 视口基准） */
--text-xs:   clamp(0.625rem, 0.8vw, 0.75rem);   /* 辅助文字 */
--text-sm:   clamp(0.75rem,  1vw,   0.875rem);   /* 正文小 */
--text-base: clamp(0.875rem, 1.2vw, 1rem);       /* 正文 */
--text-lg:   clamp(1rem,     1.5vw, 1.25rem);    /* 正文大 */
--text-xl:   clamp(1.25rem,  2vw,   1.5rem);     /* 小标题 */
--text-2xl:  clamp(1.5rem,   2.5vw, 2rem);       /* 标题 */
--text-3xl:  clamp(2rem,     4vw,   3rem);       /* 大标题 */
--text-4xl:  clamp(3rem,     6vw,   5rem);       /* 超大标题 */
--text-5xl:  clamp(4rem,     8vw,   7rem);       /* 巨幅标题 */
```

### 间距系统

```
--space-xs: 0.5rem
--space-sm: 1rem
--space-md: 1.5rem
--space-lg: 2.5rem
--space-xl: 4rem
--space-2xl: 6rem
```

---

## 第九步：导航与控制

### 必备交互

- **键盘**: ← → 切换页面，Space 下一页，Home/End 首末页
- **鼠标**: 底部左右箭头按钮（半透明，悬停高亮）
- **触摸**: 左右滑动支持
- **指示器**: 底部进度条 + 页码显示（如 "3 / 12"）
- **缩略图导航**: 按 T 键可打开/关闭缩略图网格

### 可选增强

- 按 F 进入全屏
- 按 B 黑屏（演讲中途暂停）
- 按数字键直接跳转页面
- 自动播放模式（按 A 切换）

---

## 第十步：HTML 文件结构规范

> **代码模板**：`references/code-templates.md` → "完整 HTML 骨架" 章节是可直接复制的基础模板，包含完整的 CSS 变量、背景层、玻璃态样式、排版系统、SVG 图标样式、导航控制、粒子背景、完整 JS 引擎。从此骨架开始构建，替换主题变量和幻灯片内容即可。

### 必须遵循的结构（简写版）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>根据内容命名</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        /* ===== 1. CSS 变量（主题） ===== */
        /* ===== 2. 全局重置与基础样式 ===== */
        /* ===== 3. 背景层样式 ===== */
        /* ===== 4. 幻灯片容器 ===== */
        /* ===== 5. 布局样式（8种） ===== */
        /* ===== 6. 卡片/组件样式 ===== */
        /* ===== 7. SVG 图标样式 ===== */
        /* ===== 8. 动画关键帧定义 ===== */
        /* ===== 9. 导航控制样式 ===== */
        /* ===== 10. 响应式微调 ===== */
    </style>
</head>
<body>
    <!-- ===== 背景层 ===== -->
    <div class="bg-layer">
        <!-- 渐变 / 图案 / 粒子 / 图片 -->
    </div>

    <!-- ===== 主演示容器 ===== -->
    <main class="presentation">
        <!-- 幻灯片页们 -->
        <section class="slide active" data-index="0" data-transition="fade">
            <!-- 内容 -->
        </section>
        <!-- ...更多幻灯片... -->
    </main>

    <!-- ===== 导航控制 ===== -->
    <nav class="nav-controls">
        <!-- 箭头、进度条、页码 -->
    </nav>

    <script>
        // ===== 1. 幻灯片切换引擎 =====
        // ===== 2. 键盘/鼠标/触摸事件 =====
        // ===== 3. 入场动画触发 =====
        // ===== 4. 自动播放（可选） =====
    </script>
</body>
</html>
```

---

## 第十一步：质量检查清单

生成 HTML 后，逐项检查：

### 内容质量
- [ ] 每页文字量充足，没有"一句话撑一页"的情况
- [ ] 卡片描述文字 ≥20 字，是完整句子而非喊口号
- [ ] 信息有深度，观众能获得新认知
- [ ] 内容区域占视口 ≥70%

### 图片质量
- [ ] 除封面外，≥50% 的页面有生成配图
- [ ] SVG 仅用作 ≤48px 的小图标，没有大号 SVG "插画"
- [ ] 配图无边框、无玻璃态包裹、无大圆角
- [ ] 配图容器撑满可用空间，没有 `max-width` 过小的问题
- [ ] 图片上的文字有遮罩层保证可读
- [ ] 封面背景图全屏覆盖

### 背景质量
- [ ] 每页背景各不相同，有 ≥30% 的差异
- [ ] 没有连续多页使用相同的纯色渐变
- [ ] 光斑位置/颜色/大小每页有变化

### 技术质量
- [ ] 无任何 emoji 字符
- [ ] 字体层级清晰，标题与正文对比分明
- [ ] 动画时长合理（≤0.8s）
- [ ] 键盘导航完整可用
- [ ] 幻灯片数量 ≥3 页
- [ ] 文件独立运行（字体 CDN 除外）

---

## 使用示例

### 用户只需提供内容

```
用户：帮我做一个关于"2025年AI趋势报告"的幻灯片
用户：做一个产品路线图的演示
用户：帮我做一份碳中和项目汇报的PPT
```

### AI 执行流程

1. **分析内容** → 判断主题、风格、情感
2. **确定结构** → 每页选什么布局、什么动画
3. **生成配图**（如需要）→ 使用图像生成工具
4. **编写 HTML** → 完整单文件，包含所有 CSS/JS
5. **输出路径** → `/workspace/<slug>.html`
6. **告知 URL** → 给出完整访问链接

---

## 禁止事项

- ❌ 不要使用 emoji 作为图标
- ❌ **不要用 SVG 充当叙事配图**（SVG 只能做 ≤48px 的小图标）
- ❌ **不要让内容空虚**——每页必须有充实文字，卡片描述不能只有3个字
- ❌ **不要所有页面用同一个背景**——每页背景必须有差异
- ❌ **不要给配图加边框或玻璃态包裹**——图片要自由撑满
- ❌ 不要使用外链图片（除了生成的本地图片）
- ❌ 不要使用超过 3 种字体
- ❌ 不要使用纯黑色 #000 或纯白色 #fff
- ❌ 不要让动画超过 0.8 秒
- ❌ 不要使用 alert() 或粗劣的交互
- ❌ 不要生成多文件（必须是单 HTML 文件）
