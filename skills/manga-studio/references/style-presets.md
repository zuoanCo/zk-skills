# 画风预设

每种预设给出 **英文 prompt 片段** + **典型用途**,直接拼到角色表 / 布局 / 成稿的 prompt 后面。

## shonen(少年漫画)

**风格关键词**:
```
shonen manga style, bold black ink lines, dynamic action lines, speed effects,
sweat drops, exaggerated expressions, large eyes with sharp highlights,
screentone shading, high-contrast black and white (or vivid saturated color),
energetic composition, manga panel borders with thick black gutters
```

**典型**:Jump 系热血少年漫(海贼/火影/我的英雄学院)

**适合**:冒险/战斗/热血/友情/成长

## shojo(少女漫画)

**风格关键词**:
```
shojo manga style, delicate thin lines, soft screentone, sparkles and flower
petals, large detailed eyes with long lashes, soft pastel colors (or elegant B&W),
flowing hair, emotional close-ups, decorative panel borders, lace and floral
backgrounds
```

**典型**:りぼん/花とゆず系(美少女战士/赤发白雪姬)

**适合**:恋爱/校园/友情/情感/成长

## seinen(青年漫画)

**风格关键词**:
```
seinen manga style, realistic proportions, detailed backgrounds, heavy use of
cross-hatching and detailed screentone, gritty textures, mature character design,
cinematic framing, complex panel layouts, muted color palette (or stark B&W)
```

**典型**:ヤングマガジン/アフタヌーン(攻壳/怪物)

**适合**:剧情/悬疑/科幻/社会/成人向

## chibi(Q 版)

**风格关键词**:
```
chibi / super-deformed style, oversized head (1:2 head-to-body ratio), tiny
body, large round eyes, simple dot-like mouth, minimal detail, cute kawaii
expressions, pastel color palette
```

**典型**:四格漫画 / 表情包 / 角色立绘

**适合**:搞笑/日常/萌系/教学/科普

## ink-wash(水墨)

**风格关键词**:
```
Chinese ink wash painting style, sumi-e brush strokes, monochromatic black ink,
generous white space (留白), subtle gray gradients, calligraphic line quality,
minimal detail, atmospheric and poetic mood, traditional East Asian aesthetics
```

**典型**:墨流し / 禅意漫画 / 古风武侠

**适合**:意境/古风/禅意/写意/抒情

## webtoon(条漫)

**风格关键词**:
```
webtoon style (Korean manhwa / LINE manga), full color, vertical scroll-friendly
composition, soft digital coloring with gradients, clean line art, simplified
backgrounds, large character close-ups for emotional impact, vibrant color
palette, no panel borders or thin gutters
```

**典型**:네이버 웹툰 系列(女神降临/看脸时代)

**适合**:网文改编/手机阅读/长篇连载/全彩叙事

## realistic-cinematic(半写实电影感)

**风格关键词**:
```
semi-realistic cinematic illustration style, movie-like lighting with strong
shadows, photorealistic textures, anamorphic lens feel, dramatic color grading,
moody atmosphere, characters with realistic proportions and detailed faces
```

**典型**:好莱坞概念图 / 游戏 CG / 改编电影分镜

**适合**:改编/概念图/海报/写实向

## custom(自定义)

如果用户给了具体风格描述(比如"吉卜力风"、"皮克斯 3D"、"新海诚风"等),不预设词,直接用用户描述的英文翻译版。

---

# 比例预设

| Key | w × h | image-gen size | 适用 |
|-----|-------|----------------|------|
| `A4` | 595 × 842 | `1024x1448` (近似 2:3) | 传统漫画 |
| `portrait-3-4` | 600 × 800 | `1024x1366` | 竖屏手机 |
| `square-1-1` | 800 × 800 | `1024x1024` | 社媒/四格 |
| `landscape-16-9` | 1280 × 720 | `1280x720` | 演示/横幅 |

---

# 颜色模式

- `color`:全彩,默认
- `monochrome`:黑白 + 网点(screentone)

单色模式 prompt 末尾追加:
```
Strictly black and white manga with traditional screentone shading. No color
whatsoever. High contrast between solid blacks and pure white.
```
