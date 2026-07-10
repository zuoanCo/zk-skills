#!/usr/bin/env python3
"""
build_character_prompt.py
根据 character 描述 + style preset 构造单张角色表的 image-gen prompt。

用法:
  python3 build_character_prompt.py \\
    --name "林小满" --description "16 岁女高中生,黑色短发,总戴红色耳机,会黑客技术" \\
    --style shonen \\
    --out prompts/char-lin-xiaoman.txt
"""
import argparse
import json
import sys
from pathlib import Path

# 引入 style presets
sys.path.insert(0, str(Path(__file__).parent))
try:
    from style_presets import STYLE_KEYWORDS
except ImportError:
    STYLE_KEYWORDS = {
        'shonen': 'shonen manga style, bold black ink lines, dynamic action lines, screentone shading, high contrast',
        'shojo': 'shojo manga style, delicate thin lines, soft screentone, sparkles, large detailed eyes',
        'seinen': 'seinen manga style, realistic proportions, detailed backgrounds, cross-hatching, muted palette',
        'chibi': 'chibi / super-deformed style, oversized head 1:2 ratio, large round eyes, kawaii cute',
        'ink-wash': 'Chinese ink wash sumi-e style, monochromatic black, generous white space, calligraphic',
        'webtoon': 'webtoon style, full color, vertical scroll, soft digital coloring, clean line art, vibrant',
        'realistic-cinematic': 'semi-realistic cinematic, movie lighting, photorealistic textures, dramatic color grading',
        'custom': '',
    }


TEMPLATE = """Professional manga character reference sheet for "{name}".

**Character description**:
{description}

**Style**: {style}

**CRITICAL — Output specification**:
- A single image, 6 panels arranged in 2 rows × 3 columns
- Row 1 (head shots): side view / front-neutral-expression / front-smiling
- Row 2 (full body): front / side / back
- White or neutral background
- Consistent lighting and proportions across all 6 panels
- Bold black outlines

**DO NOT INCLUDE**:
- Any text, labels, character names, or panel numbers anywhere on the image
- Any props, weapons, or scenery
- Any speech bubbles or dialogue
- Any logos or watermarks

**Output**: only the 6-panel character reference image. Nothing else."""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True)
    p.add_argument('--description', required=True)
    p.add_argument('--style', default='shonen',
                   choices=list(STYLE_KEYWORDS.keys()))
    p.add_argument('--has-reference', action='store_true',
                   help='用户提供了参考图,会作为 ref-image 传给 image-gen')
    p.add_argument('--out', help='输出文件路径,默认 stdout')
    args = p.parse_args()

    style_kw = STYLE_KEYWORDS.get(args.style, '')
    prompt = TEMPLATE.format(
        name=args.name,
        description=args.description,
        style=style_kw,
    )

    if args.has_reference:
        # 加一行说明,告诉 image-gen 优先看参考图
        prompt = (
            "Professional manga character reference sheet for "
            f"\"{args.name}\".\n\n"
            "**Reference images provided** (use as visual reference for art style and key traits only):\n"
            "- Match the line art style, coloring, and rendering technique of the reference images\n"
            "- Keep recognizable traits (hair, face shape, age) but the character may wear different clothing/pose\n\n"
            f"**Character description**:\n{args.description}\n\n"
            f"**Style**: {style_kw}\n\n"
            "**CRITICAL — Output specification**:\n"
            "- Single image, 6 panels, 2 rows × 3 columns\n"
            "- Row 1: side view head / front-neutral head / front-smiling head\n"
            "- Row 2: front full body / side full body / back full body\n"
            "- White background, consistent lighting\n"
            "- Bold black outlines\n\n"
            "**DO NOT INCLUDE**: any text, labels, names, numbers, props, scenery, dialogue, logos."
        )

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(prompt, encoding='utf-8')
        print(f"wrote {args.out} ({len(prompt)} chars)", file=sys.stderr)
    else:
        print(prompt)


if __name__ == '__main__':
    main()
