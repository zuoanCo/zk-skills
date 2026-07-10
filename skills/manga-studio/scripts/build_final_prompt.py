#!/usr/bin/env python3
"""
build_final_prompt.py
根据 storyboard + layout + characters + colorMode 构造成稿的 image-gen prompt。

用法:
  python3 build_final_prompt.py \\
    --storyboard-json storyboards/page-1.json \\
    --layout layouts/page-1.png \\
    --character-sheets "林小满:char-lin.png,老周:char-zhou.png" \\
    --style shonen --color-mode color \\
    --prev-page-final page-0.png \\
    --out prompts/page-1-final.txt
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from style_presets import STYLE_KEYWORDS


TEMPLATE = """Professional manga artist. Create the final manga page.

**Provided assets**:
1. **Panel layout image** (compositional guide) — follow it as the primary composition reference
2. **Character reference sheets** (one per character) — use them for character appearance
{prev_asset_line}

**Style**: {style_kw}
**Color mode**: {color_mode_line}

**Scene script** (panel by panel, with EXACT dialogue):
{panels_block}

**CRITICAL instructions**:
1. **Composition**: Follow the panel layout faithfully. Larger panels = more detail and dynamic composition. Do not invent new panels not in the layout.
2. **Characters**: Strictly per reference sheets. Only the characters specified for each panel. No extras, no missing characters.
3. **Dialogue** (USE EXACTLY AS WRITTEN — do not paraphrase, translate, or modify):
{dialogue_block}
4. **Speech bubbles**: Place dialogue text inside the speech bubble shapes from the layout. If a panel has dialogue but the layout has no bubble, create an appropriate bubble. **All text must have bold, clear, thick black outlines.**
5. **Visual continuity**: {continuation_line}
6. **Consistency**: All panels in this page must have the same line weight, color palette, and rendering style.

**Output**: A single manga page image. No commentary, no text outside the panels."""


COLOR_PROMPTS = {
    'color':      'Full color manga with vivid but tasteful palette. Soft digital coloring, gentle gradients, clean line art.',
    'monochrome': 'Strictly black and white manga with traditional screentone shading. No color whatsoever. High contrast between solid blacks and pure white.',
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--storyboard-json', required=True)
    p.add_argument('--layout', required=True, help='布局草图路径')
    p.add_argument('--character-sheets', required=True,
                   help='"name1:sheet1.png,name2:sheet2.png"')
    p.add_argument('--style', default='shonen', choices=list(STYLE_KEYWORDS.keys()))
    p.add_argument('--color-mode', default='color', choices=['color', 'monochrome'])
    p.add_argument('--prev-page-final', default='',
                   help='上一页成稿路径(多页模式)')
    p.add_argument('--out')
    args = p.parse_args()

    sb = json.loads(Path(args.storyboard_json).read_text(encoding='utf-8'))
    style_kw = STYLE_KEYWORDS.get(args.style, '')

    # 构造 panels_block 和 dialogue_block
    panels_lines = []
    dialogue_lines = []
    for panel in sb.get('panels', []):
        n = panel.get('panel', '?')
        desc = panel.get('description', '').strip()
        dlg = panel.get('dialogue', '').strip()
        size = panel.get('relativeSize', 'M')
        line = f"Panel {n} (size: {size}):\n  Visual: {desc}"
        if dlg:
            line += f"\n  Dialogue: {dlg}"
        else:
            line += "\n  Dialogue: (no dialogue)"
        panels_lines.append(line)
        if dlg:
            dialogue_lines.append(f'Panel {n}: "{dlg}"')
    panels_block = '\n\n'.join(panels_lines) or '(no panels)'
    dialogue_block = '\n'.join(dialogue_lines) or '(no dialogue in this page)'

    # 前页资产行
    prev_asset_line = ''
    continuation_line = 'First page, no prior context.'
    if args.prev_page_final:
        prev_asset_line = (
            f'3. **Previous page image** (for visual continuity): use it to maintain '
            f'character outfits, locations, lighting, and overall mood.\n'
        )
        continuation_line = (
            'Maintain character outfits, locations, lighting, color palette, and '
            'overall mood from the previous page. Do not reset any visual elements.'
        )

    # 颜色行
    color_mode_line = COLOR_PROMPTS[args.color_mode]

    prompt = TEMPLATE.format(
        prev_asset_line=prev_asset_line,
        style_kw=style_kw,
        color_mode_line=color_mode_line,
        panels_block=panels_block,
        dialogue_block=dialogue_block,
        continuation_line=continuation_line,
    )

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(prompt, encoding='utf-8')
        print(f"wrote {args.out} ({len(prompt)} chars)", file=sys.stderr)
    else:
        print(prompt)


if __name__ == '__main__':
    main()
