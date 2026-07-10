# 数据模型参考

源自 morsoli/aimangastudio 的 `types.ts`,做了精简和面向 skill 的改造。

## 顶层结构

```typescript
interface ComicProject {
  title: string;
  worldview: string;
  style: MangaStyle;
  aspectRatio: AspectRatio;
  colorMode: 'color' | 'monochrome';
  language: 'zh' | 'en' | 'ja';
  characters: Character[];
  pages: Page[];
}
```

## Character

```typescript
interface Character {
  id: string;                    // 短 uuid 或 'char-{name-slug}'
  name: string;                  // 显示名,中文/日文/英文均可
  description: string;           // 1-3 句核心设定(性格+外观关键特征)
  referenceImages?: string[];    // 原始参考图(base64 / URL / 路径),可选
  sheetImage?: string;           // 生成的 6 视角角色表,**关键字段**
  poses?: Pose[];                // 收藏的姿势(从分镜复用)
}
```

**关键约束**:`sheetImage` 一旦生成,后续所有出图都必须把它作为 reference image 传入。**没有 sheetImage 就不出图**(先回去补这一步)。

## Panel / Storyboard

```typescript
interface Panel {
  panel: number;                 // 1-based,页内编号
  description: string;           // 必填。视觉描述:谁在哪、做什么、镜头角度、构图
  dialogue?: string;             // 选填。对话格式 "角色名:台词" 或旁白
  sfx?: string;                  // 选填。音效词(KABOOM! 砰!)
  relativeSize?: 'S' | 'M' | 'L' | 'XL';  // 选填。控制 panel 在页面里的相对尺寸
}

interface Storyboard {
  summary: string;               // 一句话剧情摘要
  panels: Panel[];               // 单页通常 2-4 格,4 格漫画用 4
}
```

**约束**:
- 每页 panel 数:简单剧情 2-3,标准 4,大场面可拆到 6
- `description` 必带"镜头语言"提示:close-up / wide shot / over-the-shoulder / bird's eye
- `dialogue` 必带角色名(LLM 才知道气泡指向谁)
- `relativeSize` 不写默认 M;刻意写 L/XL 来制造视觉重点

## Page

```typescript
interface Page {
  pageNumber: number;
  storyboard: Storyboard;
  layoutImage?: string;          // 草图阶段产物
  finalImage?: string;           // 成稿阶段产物
  previousPage?: Pick<Page, 'finalImage' | 'storyboard'>;  // 连续性参考
}
```

多页模式下,`previousPage.finalImage` 必须传给下一步的 LLM。

## 画风预设(MangaStyle)

```typescript
type MangaStyle =
  | 'shonen'        // 少年漫画:粗线条、大动作、热血
  | 'shojo'         // 少女漫画:细腻、花朵、闪亮效果
  | 'seinen'        // 青年漫画:写实、复杂构图
  | 'chibi'         // Q 版:头大身小、可爱
  | 'ink-wash'      // 水墨:留白、意境
  | 'webtoon'       // 条漫:竖屏滑动、彩色、简化背景
  | 'realistic-cinematic'  // 半写实电影感
  | 'custom';       // 用户自描述
```

## 比例(AspectRatio)

| Key | w × h | value (用于 image-gen size) | 适用场景 |
|-----|-------|----------------------------|----------|
| `A4` | 595×842 | `595:842` ≈ `2:3` | 传统漫画页 |
| `portrait-3-4` | 600×800 | `3:4` | 竖版手机 |
| `square-1-1` | 800×800 | `1:1` | 社媒头像/四格 |
| `landscape-16-9` | 1280×720 | `16:9` | 演示/横幅 |

## 颜色(ColorMode)

- `color`:全彩,默认
- `monochrome`:黑白 + 网点(经典漫画风)

## 注意事项

1. **character.description 是核心**——LLM 画角色时只信这个,不信对话里临时改的描述。如果用户中途说"角色 A 改成红头发",**必须先更新 description,再回去重新出图**。
2. **storyboard 是单一真相源**——layout prompt 和 final prompt 都从同一份 storyboard 派生,不要在两个 prompt 里分别写描述(会不一致)。
3. **多页的 previousPage 不能丢**——少了就一定翻车,角色穿错衣服、场景跳台。
