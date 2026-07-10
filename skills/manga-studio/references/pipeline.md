# 五段式流水线

每段都列出:**输入 → 提示词要点 → 输出 → 验证点**。

---

## ① 世界观(可选,文字 LLM)

**输入**:character 列表(尤其 description)、premise
**输出**:一段 200-400 字的背景设定(中文/英文/日文,根据 `language` 字段)
**调不调**:用户给了就不调,直接用;没给才生成

**Prompt 要点**(参考 `geminiService.generateWorldview`):
- 角色是"已知事实",围绕他们构造世界
- 包含:独特背景 / 关键规则 / 冲突或谜团 / 角色与世界的关联
- 语调要"给漫画艺术家灵感",不能干巴巴
- 输出"一整段文字"而非列表

**示例 prompt 模板**:
```
你是一位富有创意的世界观构建者和故事讲述者。

**角色**:
- 林小满:16 岁女高中生,黑色短发,总戴红色耳机,会黑客技术
- 老周:50 岁流浪汉,实际上是退休的网络安全专家

**剧情梗概**:
少女在赛博朋克城市里寻找失踪的猫,意外揭开城市 AI 主脑的秘密。

**任务**:
- 创造独特背景设定
- 描述关键规则/冲突/谜团
- 解释角色与世界的关联
- 200-400 字,一整段
```

---

## ② 角色表(每个角色一次 image-gen)

**输入**:character.{name, description, referenceImages?}, style
**输出**:6 视角网格图(2 行 × 3 列):头顶 = 3 头像,底行 = 3 全身
**关键约束**:
- 用户给了 `referenceImages` 就当 `--ref-images` 传
- 无论有没有参考图,prompt 都强制网格布局
- prompt 末尾必带"no text / no labels / no names"

**Prompt 模板**:
```
Professional manga character reference sheet for "[name]".

[description]

Style: [style preset details — e.g. "clean shonen line art, bold strokes"]

**Output: a single 6-panel character sheet, 2 rows × 3 columns:**
- Row 1 (head shots): side view / front-neutral / front-smile
- Row 2 (full body): front / side / back

White background. No text. No labels. No character name on the image. No speech bubbles. No props. The character only.
```

**验证**:
- 6 个格子都有图?✓
- 角色特征跟 description 一致(发色、服饰、年龄)?✓
- 没有任何文字?✓
- 3 个全身像要包含正面/侧面/背面(不能都是正面)✓

---

## ③ 故事板(文字 LLM + JSON Schema)

**输入**:premise, worldview, characters[], previousPages?[]
**输出**:`Storyboard = {summary, panels: [{panel, description, dialogue?}]}`
**调不调**:用户给了故事大纲 → 拆 panel;没给 → 从 premise 生成整页

**Prompt 模板**(强制 JSON):
```
你是单页漫画编剧。

**世界观**:
{worldview}

**角色**:
- 林小满: 16 岁女高中生,黑短发红耳机
- 老周: 50 岁流浪汉,退休网络安全专家

**前情(若多页)**:
- Page 1: {summary + panels of previous page}

**本页前提**:
{premise}

**任务**:生成本页 storyboard。
- 2-4 个分镜(panels)
- 每个分镜必带:视觉描述(谁在哪、镜头角度、构图)+ 角色名(若有)
- dialogue 可选,格式:角色名:台词
- 所有对话使用 {language}
- 输出 JSON: {summary, panels: [{panel, description, dialogue?}]}
```

**验证**:
- JSON Schema 严格:`summary` 字符串 + `panels` 数组
- 每个 panel 的 description 至少 30 字,带镜头语言
- dialogue 角色名跟 characters 列表匹配
- 如果多页,跟 previousPage 衔接合理

---

## ④ 布局草图(每个 page 一次 image-gen)

**输入**:storyboard, aspectRatio, characters(只要 sheetImage 路径列表), previousPage?
**输出**:粗略灰度素描,展示分镜布局和角色位置
**关键约束**:
- 强调"无文字",否则文字会被烤进成稿
- 强调"动态构图",避免 LLM 出 2x2 等距网格
- aspect ratio 严格匹配,不留边距
- previousPage 传入作为构图连续性参考(多页时)

**Prompt 模板**:
```
Professional manga storyboard layout artist. Create a ROUGH GRAYSCALE SKETCH.

**Story to visualize**:
{summary}
{逐 panel 描述,格式 "Panel {n}: {description}"}

**Aspect ratio**: {w}:{h}, filling the entire canvas with NO margins.

**Composition instructions**:
- Use dynamic, professional comic panel layout
- Vary panel sizes: bigger panel for key moments, smaller for reactions/transitions
- Use diagonal cuts, overlapping panels, insets, or panel-bleeds for impact
- DO NOT use simple 2x2 equal grids unless the story truly needs it

**CRITICAL — visual sketch only, NOT final art**:
- Rough, simple lines, basic shapes
- Place characters using the provided character sheets as appearance reference
- **No text, no labels, no numbers, no dialogue, no speech bubbles with text**
- No final art quality — this is a layout guide only
- Grayscale or line-art only

**Character reference sheets**: {列出每个角色的 sheet 路径}
**Previous page layout**: {多页时附}
```

**验证**:
- 完全没有文字/数字/对话气泡文字?✓
- panel 数量跟 storyboard 一致?✓
- 尺寸有变化(不是等距网格)?✓
- 角色位置大致对应 storyboard 里的描述?✓

---

## ⑤ 成稿(每个 page 一次 image-gen)

**输入**:storyboard, layoutImage, characters, colorMode, previousPage?
**输出**:最终彩色(或黑白)漫画页
**关键约束**:
- 必传 layoutImage 作为构图参考
- 必传所有出场角色的 sheetImage 作为外观参考
- 多页时,额外传 previousPage.finalImage 作为连续性参考
- dialogue 必须原样出现(从 storyboard 里复制,不要让 LLM 改写)
- bubble 是布局画好的(空 bubble),成稿只负责填对话

**Prompt 模板**:
```
Professional manga artist. Finalize one manga page.

**Provided assets**:
1. Panel layout (compositional guide — use it, don't deviate significantly)
2. Character reference sheets (use them for character appearance)
3. Previous page image (for visual continuity if provided)
4. Scene script (panel-by-panel descriptions + exact dialogue)

**Style**: {style preset}
**Color mode**: {color | monochrome}

**CRITICAL instructions**:
1. **Composition**: Follow the panel layout. Larger panels = more detail, more dynamic composition.
2. **Characters**: Strictly per reference sheets. Only the characters specified for each panel. No extras.
3. **Dialogue** (use EXACTLY as written, do not change wording):
{逐 panel 列出 "Panel {n}: {description}\n  Dialogue: {dialogue}"}
4. **Speech bubbles**: Draw bubbles (per layout), fill with the exact dialogue text above. Bold black outlines on all text.
5. **Visual continuity**: {若多页,加"Maintain character outfits, locations, and mood from previous page."}

**Output**: A single manga page image. No commentary, no text outside the panels.
```

**验证**:
- 对话文字跟 storyboard 完全一致(不是 AI 改写的)?✓
- 角色外观跟 sheetImage 一致(发色/服装)?✓
- panel 布局跟 layoutImage 大致对应?✓
- 多页时,服装/场景跟前页连贯?✓

---

## 多页流程

```
page 1: ②③④⑤ (跑全套)
page 2: ③' (用 page1 当 previousPage) ④' (用 page1.layout 当参考) ⑤' (用 page1.final 当参考)
page 3: 同 page 2
...
```

`generateDetailedStorySuggestion` 的 `previousPages` 字段接受 `Pick<Page, 'generatedImage' | 'sceneDescription'>[]`,**传前几页的成稿和脚本**,LLM 自动续写。

**注意**:第 N 页成稿应该把 page N-1 的 finalImage 当 ref-image 传(不是 storyboard 文本),保持视觉连续性。
