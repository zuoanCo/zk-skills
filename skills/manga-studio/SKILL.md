---
name: manga-studio
description: AI 漫画生成工作流。从剧情/角色/世界观等素材出发,自动产出:①世界观设定 ②角色参考表 ③分镜脚本(JSON) ④分镜布局草图 ⑤成稿画面。覆盖单页和多页连续剧情,内置角色一致性和页间连续性机制。触发场景:(1) 用户要做漫画/分镜/故事板(storyboard/分镜/四格/单幅);(2) 用户给了剧情梗概、角色描述、世界观,要求出图;(3) 用户提到"画漫画"、"AI 漫画"、"manga"、"comic"、"分镜设计"、"画面脚本";(4) 用户想给小说/IP 做可视化分镜;(5) 需要从零设计一套可复用的角色 + 世界观 + 故事线。不适用于:已存在的图片编辑/修复(用 image-gen)、公众号文章配图(用 gzh-design)、PPT 大纲(用 dashiai-ppt)。
---

# manga-studio · AI 漫画工作流

把"剧情/角色素材 → 一本能看的漫画"这件事串起来。源自 morsoli/aimangastudio 的五段式流水线(text 规划 → 草图 → 角色表 → 终稿),改造成可在 Claude Code 里直接跑的 agent 工作流。

## 何时使用

- 用户说"给我画个漫画"/"出个分镜"/"做一页 manga"
- 用户给了剧情、人物设定、世界观,要求出图
- 用户想为短篇/网文/广告做一页或一套视觉故事
- 用户想批量产出多个角色(剧本杀/桌游/小说设定集)
- 用户已经有一个故事大纲,想拆成分镜脚本

## 不适用

- 单图/单头像生成 → 用 `image-gen`
- 公众号文章配图 → 用 `gzh-design`
- PPT 演示文稿 → 用 `dashiai-ppt`
- 修复/编辑已有图片 → 用 `image-gen` 的编辑流程

## 工作流(五段)

每段都是 LLM prompt + 可选 `image-gen` 调用的组合,**严格按顺序**,因为每步的输出是下步的输入。

```
① 世界观 ──── 文字 LLM
   ↓ (若用户没给设定)
② 角色表 ──── 每个角色一张图(用 image-gen,角色名 + 描述 → 提示词)
   ↓
③ 故事板 ──── 文字 LLM,JSON Schema 强制结构(summary + panels[])
   ↓ (用户可编辑)
④ 布局草图 ── 用 image-gen,prompt 强调"粗糙素描、无文字、动态构图"
   ↓ (用户可编辑,标注角色姿态)
⑤ 成稿 ───── 用 image-gen,prompt 把布局 + 角色表 + 脚本合成一页
```

### 单页(默认)
一次跑完 5 段,输出 1 个角色集 + 1 个故事板 + 1 个布局 + 1 张成稿。

### 多页(剧情)
每页跑 ②③④⑤,世界观/角色表复用。`generateDetailedStorySuggestion` 支持传 `previousPages[]`,**前页的脚本 + 成稿图像**作为续写的输入,保证叙事连续性。

## 输入合同

用户最少要提供**剧情梗概(premise)**。其它都有默认值。

| 字段 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `premise` | ✅ | — | 一句话故事前提,例如"少女在赛博朋克城市里寻找失踪的猫" |
| `characters` | ❌ | 智能生成 | 角色列表 `[{name, description, referenceImages?}]`。`referenceImages` 是已知的角色参考图(base64 或 URL),有就用,没有就生成 |
| `worldview` | ❌ | 从 premise 衍生 | 一段背景设定文字 |
| `style` | ❌ | 日系少年漫画 | 画风预设(详见 `references/style-presets.md`) |
| `pageCount` | ❌ | 1 | 连续页数(>1 时开启页间连续性) |
| `aspectRatio` | ❌ | A4 (210:297) | A4 / 竖版 3:4 / 正方形 1:1 / 横版 16:9 |
| `colorMode` | ❌ | color | `color` / `monochrome` |
| `language` | ❌ | zh | 脚本/对话用什么语言生成 |

## 输出合同

输出**一个 `comic.json` + 一个 `comic.md`**(`comic.md` 是人类可读渲染版):

```json
{
  "worldview": "string",
  "characters": [{ "name", "description", "sheetImage": "<path or base64>" }],
  "pages": [
    {
      "pageNumber": 1,
      "storyboard": {
        "summary": "一句话剧情摘要",
        "panels": [
          { "panel": 1, "description": "画面描述", "dialogue": "角色:台词" }
        ]
      },
      "layoutImage": "<path>",
      "finalImage": "<path>"
    }
  ]
}
```

## 关键原则(从 aimangastudio 提炼)

1. **角色一致性靠参考表**:每个角色都必须有 `sheetImage`(6 视角网格,3 头 + 3 全身),所有后续出图都把 sheet 当 reference image 传给 image-gen。不允许"凭记忆"画角色。
2. **故事板必须 JSON Schema**:用结构化输出,避免 LLM 自由发挥。每条 panel 至少有 `panel 编号 + 视觉描述`,对话可选。
3. **布局草图必须无文字**:布局是构图指导,不是终稿。如果出了文字,后续会被烤进成稿,改不掉。
4. **分镜相对尺寸 = 叙事权重**:大 panel = 关键时刻 / 详细构图;小 panel = 过渡 / 反应镜头。**这是核心节奏控制**。
5. **页间连续性靠前页输入**:多页模式下,第 N 页的 `generateDetailedStorySuggestion` 必须传 `previousPages[].{generatedImage, sceneDescription}`。LLM 看了上一张图才知道角色穿什么、场景在哪。
6. **dialogue 在脚本里写明**:成稿 prompt 里说"将对话放进气泡",**对话内容必须在场景脚本里给出**,不要让 AI 自由发挥台词。
7. **每步都可中断**:用户在任何一步说"停"/"改这里",都应该支持重做单步,不要强制从头跑。

## 怎么调 image-gen(组合方式)

**不要在 skill 里自己实现 HTTP 调用**。直接用项目里的 `image-gen` skill:

```bash
# 角色表(每个角色一次)
python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/char-X.txt)" \
  --size 1024x1024 --sync

# 布局草图
python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/page-1-layout.txt)" \
  --size 102x144  # 接近 A4 比例 --sync

# 成稿(可附参考图)
python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/page-1-final.txt)" \
  --ref-images char-sheets/*.png \
  --ref-images layouts/page-1.png \
  --size 1024x1448 --sync
```

**关键细节**:
- 角色表 prompt 末尾要加 `**Output: 6-panel character sheet, 2 rows × 3 columns. Row 1: 3 head shots (side, front-neutral, front-smile). Row 2: 3 full-body (front, side, back). No text, no labels, no names anywhere on the image.**` — 强制网格布局。
- 布局草图 prompt 强调 `**No text, no labels, no numbers, no dialogue. Rough grayscale sketch only. No final art quality. Dynamic composition.**`。
- 成稿 prompt 里指定 `**Use the provided layout image as composition guide. Use the provided character sheets for character appearance. Place the exact dialogue text into the speech bubbles shown in the layout.**`。
- 多页时把上一页的 `finalImage` 加进 `--ref-images`,作为连续性参考。

## 数据模型(完整)

参考 `references/data-model.md`,核心 4 个类型:

```typescript
interface Character {
  id: string;
  name: string;
  description: string;          // 一段人物描述,世界观/人设关键
  sheetImage?: string;          // 6 视角角色表(base64 或路径)
  referenceImages?: string[];   // 用户提供的原始参考图(可选)
}

interface Panel {
  panel: number;                // 1-based
  description: string;          // 画面描述(必填)
  dialogue?: string;            // 对话,格式 "角色:台词" 或纯旁白
}

interface Storyboard {
  summary: string;              // 一句话剧情
  panels: Panel[];              // 通常 2-4 个
}

interface Page {
  pageNumber: number;
  storyboard: Storyboard;
  layoutImage?: string;         // 分镜布局草图
  finalImage?: string;          // 成稿
}
```

## 编排脚本(在 `scripts/` 下)

每个步骤都对应一个 Python 脚本,**只负责构造 prompt 和调用 image-gen**,不重新实现 LLM 调用(LLM 直接由 agent 自己来)。

| 脚本 | 职责 |
|------|------|
| `build_character_prompt.py` | 根据 character.name + description + style → 单个角色的角色表 prompt |
| `build_layout_prompt.py` | 根据 storyboard + aspect ratio + style → 布局草图 prompt |
| `build_final_prompt.py` | 根据 storyboard + layout + characters + colorMode → 成稿 prompt |
| `render_comic.py` | 把 `comic.json` 渲染成人类可读的 `comic.md` |

## 完整示例

跑一遍 `examples/sample-story.md`,从 premise 到 4 张成稿,大概 5-8 分钟,见示例文件。

## 故障排查

| 现象 | 原因 | 解决 |
|------|------|------|
| 角色长得跟设定不一样 | 缺角色表 / 角色表没当 reference 传 | 检查每页成稿 prompt 是否带了 `--ref-images char-sheets/*.png` |
| 多页之间角色衣服/场景突变 | 上一页 finalImage 没传进来 | 多页模式下,每页成稿都要加 `--ref-images final-page-N-1.png` |
| 布局里冒出文字 | 布局 prompt 没强调 "no text" | 改 `build_layout_prompt.py` 的强制约束 |
| 对话气泡是空的 / 跑题 | dialogue 没写进脚本 / 没在成稿 prompt 里强调 "exact dialogue" | 改 storyboard 重新生成,确保每条 dialogue 都显式列出 |
| 角色姿态不对应布局 | 布局里画了角色 A,成稿 prompt 没指明 A 在哪 | 在成稿 prompt 里加 "**Place character A in the largest panel per the layout, character B in the smaller panel**" |

## 安全与人工把关

- **生成前展示完整 plan**:世界观、角色、故事板、布局 prompt 给用户看,得到 OK 后再调 image-gen。
- **每页成稿前停下来问**:用户可能想改对白、改构图,**不要一口气跑完全部**。
- **儿童/敏感题材**:世界观里加明确声明,prompt 里强调 `Avoid any content depicting minors in inappropriate situations / graphic violence.`
