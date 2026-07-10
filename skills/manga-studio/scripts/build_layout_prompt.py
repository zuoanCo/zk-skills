#!/usr/bin/env python3
"""
build_layout_prompt.py
根据 storyboard + aspect ratio + style 构造布局草图的 image-gen prompt。

用法:
  python3 build_layout_prompt.py \\
    --storyboard-json storyboards/page-1.json \\
    --aspect A4 \\
    --style shonen \\
    --character-sheets "char-lin.json:lin.png,char-zhou.json:zhou.png" \\
    --prev-page-layout layouts/page-0.png \\
    --out prompts/page-1-layout.txt
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from style_presets import STYLE_KEYWORDS, ASPECT_RATIO


TEMPLATE = """Professional manga storyboard layout artist. Create a ROUGH GRAYSCALE SKETCH.

**Story to visualize**:
{summary}

**Panels** (larger panel = more important narrative moment):
{panels_block}

**Aspect ratio**: {aspect_value}, filling the entire canvas with NO margins or padding.

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

**Character reference sheets provided**:
{char_sheets_block}
{prev_layout_block}
"""


PREV_LAYOUT_BLOCK = """

**Previous page layout (for visual continuity)**:
Maintain the same line style, panel rhythm, and overall composition density as the previous page. Do not copy the exact same layout — vary it.
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--storyboard-json', required=True,
                   help='storyboard JSON 文件路径')
    p.add_argument('--aspect', default='A4', choices=list(ASPECT_RATIO.keys()))
    p.add_argument('--style', default='shonen', choices=list(STYLE_KEYWORDS.keys()))
    p.add_argument('--character-sheets', default='',
                   help='"name1:sheet1.png,name2:sheet2.png" 格式')
    p.add_argument('--prev-page-layout', default='',
                   help='上一页 layout 图像路径(可选,多页模式用)')
    p.add_argument('--out')
    args = p.parse_args()

    sb = json.loads(Path(args.storyboard_json).read_text(encoding='utf-8'))
    aspect = ASPECT_RATIO[args.aspect]
    style_kw = STYLE_KEYWORDS.get(args.style, '')

    panels_block_lines = []
    for panel in sb.get('panels', []):
        size = panel.get('relativeSize', 'M')
        desc = panel.get('description', '').strip()
        dlg = panel.get('dialogue', '').strip()
        line = f"Panel {panel.get('panel', '?')} (size: {size}): {desc}"
        if dlg:
            line += f"\n  Dialogue: {dlg}"
        panels_block_lines.append(line)
    panels_block = '\n\n'.join(panels_block_lines) or '(no panels)'

    char_sheets_block = '  (none)'
    if args.character_sheets:
        lines = []
        for entry in args.character_sheets.split(','):
            name, path = entry.split(':')
            lines.append(f'  - {name}: {path}')
        char_sheets_block = '\n'.join(lines)

    prev_layout_block = ''
    if args.prev_page_layout:
        prev_layout_block = PREV_LAYOUT_BLOCK

    prompt = TEMPLATE.format(
        summary=sb.get('summary', ''),
        panels_block=panels_block,
        aspect_value=aspect['value'],
        char_sheets_block=char_sheets_block,
        prev_layout_block=prev_layout_block,
    )

    if args.style and style_kw:
        prompt += f"\n**Overall style hint**: {style_kw}\n"

    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(prompt, encoding='utf-8')
        print(f"wrote {args.out} ({len(prompt)} chars)", file=sys.stderr)
    else:
        print(prompt)


if __name__ == '__main__':
    main()
