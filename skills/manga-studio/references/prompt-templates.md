# Prompt 模板参考

按五段流水线组织。每个模板都有变量占位符 `{...}`,用实际值替换。

---

## T1. 世界观(Worldview)

```text
你是一位富有创意的世界观构建者和漫画编剧。

**角色**:
{characters: each `- **name**: description`}

**剧情前提**:
{premise}

**任务**:
- 创造一个独特、有画面感的背景设定
- 描述这个世界的关键规则、核心冲突或谜团
- 解释这些角色如何融入或与这个世界相关联
- 200-400 字,一整段文字(不要列表)
- 语调应该为漫画艺术家提供创意和灵感
- 使用 {language} 写作

**输出**:仅返回那一段文字,不要任何解释或包装。
```

---

## T2. 角色表(Character Sheet)

```text
Professional manga character reference sheet for "{character.name}".

**Character description**:
{character.description}

**Style**: {style_keywords from style-presets.md}

**CRITICAL — Output specification**:
- A single image, 6 panels arranged in 2 rows × 3 columns
- Row 1 (head shots): side view / front-neutral-expression / front-smiling
- Row 2 (full body): front / side / back
- White or neutral background
- Consistent lighting and proportions across all 6 panels
- Bold black outlines (for color mode) or ink line art (for monochrome)

**DO NOT INCLUDE**:
- Any text, labels, character names, or panel numbers anywhere on the image
- Any props, weapons, or scenery
- Any speech bubbles or dialogue
- Any logos or watermarks

**Output**: only the 6-panel character reference image. Nothing else.
```

如果用户提供了 `referenceImages`:
```text
Professional manga character reference sheet for "{character.name}".

**Reference images provided** (use as appearance reference only):
- Apply the same art style as the references
- Maintain key visual traits (hair, face, age) from the references
- The character may differ in clothing/pose from the references; follow the description below

**Character description**:
{character.description}

[... same critical output spec as above ...]
```

---

## T3. 故事板(Storyboard)

```text
你是一位专业的单页漫画编剧。

**世界观**:
{worldview, may be empty}

**角色档案**:
{characters: each `- **name**: description`}

**前情(多页模式)**:
{previousPages: for each, `**[前页 {n}]** 摘要: ... | 脚本: ... | 图像: [已附加]`, else empty}

**本页前提**:
{premise}

**任务**:
基于以上所有背景,为本页漫画生成详细 storyboard。
- 拆分成 2-4 个分镜(panels)
- 每个分镜必填:
  - `panel`: 1-based 整数编号
  - `description`: 视觉描述(谁在哪、做什么、镜头角度、构图、表情、环境)
  - `dialogue` (可选): 对话,格式 "角色名:台词" 或 "旁白:..."
- 角色名要跟角色档案里的一致
- 所有对话使用 {language}
- 不要包含任何超出 schema 的字段

**输出 JSON schema** (严格):
```json
{
  "summary": "一句话剧情摘要",
  "panels": [
    {
      "panel": 1,
      "description": "...",
      "dialogue": "可选,字符串"
    }
  ]
}
```

只返回 JSON,不要任何解释。
```

---

## T4. 布局草图(Layout Proposal)

```text
Professional manga storyboard layout artist. Create a ROUGH GRAYSCALE SKETCH.

**Story to visualize**:
{summary}

{p逐 panel 列出,格式:
"Panel {n} ({relativeSize}): {description}"}

**Aspect ratio**: {aspectRatio.value}, filling the entire canvas with NO margins or padding.

**Composition instructions**:
- Use dynamic, professional comic panel layout
- Vary panel sizes — bigger panel for key moments, smaller for reactions/transitions
- Use diagonal cuts, overlapping panels, insets, or panel-bleeds for impact
- DO NOT use simple 2x2 equal grids unless the story truly requires it

**CRITICAL — visual sketch only, NOT final art**:
- Rough, simple lines and basic shapes only
- Grayscale or pencil-sketch style, no color
- Place characters in panels using the provided character sheets as appearance reference
- Empty speech bubble shapes are OK in the layout — but **BUBBLES MUST BE EMPTY** (no text inside)
- **No text, no labels, no numbers, no dialogue anywhere on the image**
- No final art quality — this is a layout guide only

**Character reference sheets provided**: {列出每个出场的角色 sheet 路径}
{若多页,加:
**Previous page layout (for visual continuity)**:
{prevPage.layoutImage 路径}
维持相同的画风与构图节奏。}
```

---

## T5. 成稿(Final Page)

```text
Professional manga artist. Create the final manga page.

**Provided assets**:
1. **Panel layout image** (compositional guide) — use it as the primary composition reference
2. **Character reference sheets** (one per character) — use them for character appearance
{若多页,加:
3. **Previous page image** — for visual continuity}
{若多页,改 3 为 3,4 为 4}

**Style**: {style_keywords}
**Color mode**: {color / monochrome}

**Scene script** (panel by panel, with EXACT dialogue):
{逐 panel 列出:
"Panel {n}:
  Visual: {description}
  Dialogue: {dialogue if present, else "(no dialogue)"}
  Size: {relativeSize}"
}

**CRITICAL instructions**:
1. **Composition**: Follow the panel layout faithfully. Larger panels = more detail and dynamic composition. Do not invent new panels not in the layout.
2. **Characters**: Strictly per reference sheets. Only the characters specified for each panel. No extras, no missing characters.
3. **Dialogue** (USE EXACTLY AS WRITTEN — do not paraphrase, translate, or modify):
{逐 panel 重复 dialogue,标注 "Panel {n}: {dialogue}"}
4. **Speech bubbles**: Place dialogue text inside the speech bubble shapes from the layout. If a panel has dialogue but the layout has no bubble, create an appropriate bubble. **All text must have bold, clear, thick black outlines.**
5. **Visual continuity** {若多页,加 ": Maintain character outfits, locations, lighting, and mood from the previous page."} {否则为空}
6. **Consistency**: All panels in this page must have the same line weight, color palette, and rendering style.

**Output**: A single manga page image. No commentary, no text outside the panels.
```

---

## 通用技巧

### 怎么让角色稳定

1. **每个角色固定 6 视角网格**,后续所有出图都附这个网格
2. **同一 prompt 里同时指定**:参考图路径 + 文本描述(description)
3. **如果是真人/明星/版权角色**:在 description 里写"a fictional character inspired by..." 避免被 image-gen 服务拒绝

### 怎么让构图一致

1. **布局草图是真理**:成稿 prompt 里说"严格遵循布局"+"不要发明新 panel"
2. **多页时把上页 finalImage 当 reference**:image-gen 模型对参考图敏感,能学到整体色调
3. **风格关键词每次都重复**:style 描述不能省,LLM 不会"记住"

### 怎么让对话正确

1. **成稿 prompt 里强调"USE EXACTLY AS WRITTEN"** 至少 2 遍
2. **dialogue 跟 description 分开列**:在 prompt 里用 "Dialogue:" 前缀,让 LLM 知道这是要烤进图里的
3. **气泡用布局画好的**:不要在成稿里让 LLM 自由放气泡,容易出框或者挤

### 怎么减少翻车

1. **小步迭代**:每页成稿前先让人看 layout,确认构图 OK 再出 final
2. **失败重试机制**:第一次出图不对(角色跑偏/对话错),用同一 prompt 再试 1-2 次
3. **保留中间产物**:character sheet / layout / final 都要存盘,出问题能定位
