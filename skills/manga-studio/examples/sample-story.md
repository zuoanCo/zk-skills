# 示例:从剧情到一页漫画,完整跑一遍

## 1. 用户输入

> "我想做一个赛博朋克短篇漫画,16 岁女黑客在新东京旧城找一只发光的流浪猫,揭开城市秘密。少年漫画风,4 格一页,先来一页。"

→ 自动解析:
- `premise`: "16 岁女黑客在新东京旧城找一只发光的流浪猫,揭开城市秘密"
- `style`: "shonen"
- `pageCount`: 1
- `aspectRatio`: "A4"
- `colorMode`: "color"
- `language`: "zh"

## 2. 自动扩展:世界观

LLM 给出世界观(280 字):
> 2087 年的新东京,半空中悬浮着全息广告,流浪 AI 猫穿梭在霓虹巷弄里寻找残存的电信号作为食物。绝大多数人已经迁入云端虚拟空间,旧城只剩下几个执拗的居民和数量庞大的流浪猫。一只普通女高中生意外发现,这些流浪猫正在悄悄修复旧时代被废弃的互联网主干,一旦修复完成,所有云端居民都将被迫回到现实世界。

## 3. 角色设计

智能生成 3 个核心角色:

| 角色 | 一句话描述 |
|------|-----------|
| 林小满 | 16 岁女高中生,黑色齐肩短发,左耳红色耳机,会黑客技术 |
| 老周 | 58 岁前互联网工程师,现流浪汉,旧时代的真相守护者 |
| 摩斯 | 橘色虎斑流浪猫,尾巴会发荧光(它在吃电信号) |

每个角色生成一张 6 视角角色表:

```bash
python3 ~/.claude/skills/manga-studio/scripts/build_character_prompt.py \
  --name "林小满" --description "..." --style shonen \
  --out prompts/char-lin.txt

python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/char-lin.txt)" \
  --size 1024x1024 --sync \
  --out char-sheets/lin-xiaoman.png
```

输出 3 张角色表图像(`char-sheets/lin-xiaoman.png` 等)。

## 4. 故事板生成

用结构化输出,LLM 返回:

```json
{
  "summary": "小满在霓虹巷弄里发现摩斯,被它带去找老周,得知流浪猫正在修复互联网主干。",
  "panels": [
    {
      "panel": 1,
      "description": "极广角俯拍,新东京旧城区的霓虹巷弄...",
      "dialogue": "旁白:新东京的旧城,凌晨两点。",
      "relativeSize": "XL"
    },
    { "panel": 2, "...": "..." },
    { "panel": 3, "...": "..." },
    { "panel": 4, "...": "..." }
  ]
}
```

保存到 `storyboards/page-1.json`。

**先暂停给用户看**,用户确认或修改后,再走下一步。

## 5. 布局草图

```bash
python3 ~/.claude/skills/manga-studio/scripts/build_layout_prompt.py \
  --storyboard-json storyboards/page-1.json \
  --aspect A4 --style shonen \
  --character-sheets "林小满:char-sheets/lin-xiaoman.png,老周:char-sheets/zhou-laofan.png,摩斯:char-sheets/moes-the-cat.png" \
  --out prompts/page-1-layout.txt

python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/page-1-layout.txt)" \
  --ref-images char-sheets/*.png \
  --size 1024x1448 --sync \
  --out layouts/page-1.png
```

输出粗略灰度草图,4 个 panel,无文字,只有角色大致位置。

**再暂停给用户看**,用户可以要求"把第 2 格和第 3 格换个位置"或"第 1 格再大一点"等。

## 6. 成稿

```bash
python3 ~/.claude/skills/manga-studio/scripts/build_final_prompt.py \
  --storyboard-json storyboards/page-1.json \
  --layout layouts/page-1.png \
  --character-sheets "林小满:char-sheets/lin-xiaoman.png,老周:char-sheets/zhou-laofan.png,摩斯:char-sheets/moes-the-cat.png" \
  --style shonen --color-mode color \
  --out prompts/page-1-final.txt

python3 ~/.claude/skills/image-gen/scripts/submit.py \
  --prompt "$(cat prompts/page-1-final.txt)" \
  --ref-images char-sheets/lin-xiaoman.png \
  --ref-images char-sheets/zhou-laofan.png \
  --ref-images char-sheets/moes-the-cat.png \
  --ref-images layouts/page-1.png \
  --size 1024x1448 --sync \
  --out finals/page-1.png
```

输出最终彩色漫画页,4 个 panel,带气泡和对话。

## 7. 渲染为 comic.md

```bash
python3 ~/.claude/skills/manga-studio/scripts/render_comic.py \
  --in comic.json --out comic.md
```

## 时间估算

- 世界观 + 故事板(text):~10 秒
- 3 张角色表(image):~60 秒
- 1 张布局草图(image):~30 秒
- 1 张成稿(image):~45 秒

**总计约 2.5 分钟**。多页模式额外每页 ~90 秒。

## 多页续写

第 2 页调用 `generateDetailedStorySuggestion` 时,传 `previousPages = [page1]`,LLM 看完 page 1 的成稿图像和脚本,自动续写。生成的成稿把 page 1 final 当 ref-image 传入,保持视觉连续性。

## 失败兜底

| 症状 | 处理 |
|------|------|
| 角色脸不像 | 重新跑 `generateCharacterSheet`,把结果当 ref-image 重传 |
| 对话文字错了 | 检查 `build_final_prompt.py` 输出里的 dialogue 块,人工修正 storyboard 重新跑 |
| 多页之间角色穿错衣服 | 确认 `--ref-images finals/page-N-1.png` 在第 N 页命令里 |
| 布局有文字 | 在 layout prompt 里加 `NEVER output text`,重跑 |
