#!/usr/bin/env python3
"""
render_comic.py
把 comic.json 渲染成人类可读的 comic.md。

用法:
  python3 render_comic.py --in comic.json --out comic.md
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def panel_md(panel: dict) -> str:
    n = panel.get('panel', '?')
    size = panel.get('relativeSize', '')
    desc = panel.get('description', '').strip()
    dlg = panel.get('dialogue', '').strip()
    sfx = panel.get('sfx', '').strip()
    lines = [f"### Panel {n}" + (f" ({size})" if size else ''), '', f"**画面**: {desc}"]
    if dlg:
        lines += ['', f"**对话**: {dlg}"]
    if sfx:
        lines += ['', f"**音效**: *{sfx}*"]
    return '\n'.join(lines)


def character_md(char: dict) -> str:
    name = char.get('name', '?')
    desc = char.get('description', '').strip()
    sheet = char.get('sheetImage')
    refs = char.get('referenceImages') or []
    lines = [f"### {name}", '', f"**设定**: {desc}"]
    if sheet:
        lines += ['', f"**角色表**: ![]({sheet})"]
    if refs:
        lines += ['', f"**参考图**: " + ' / '.join(f"![]({r})" for r in refs)]
    return '\n'.join(lines)


def page_md(page: dict) -> str:
    n = page.get('pageNumber', '?')
    sb = page.get('storyboard') or {}
    layout = page.get('layoutImage')
    final = page.get('finalImage')
    summary = sb.get('summary', '').strip()
    panels = sb.get('panels', [])

    lines = [f"## 第 {n} 页", '']
    if summary:
        lines += [f"**剧情**: {summary}", '']
    if layout:
        lines += [f"**布局草图**: ![]({layout})", '']
    if final:
        lines += [f"**成稿**: ![]({final})", '']

    if panels:
        lines.append('### 分镜脚本')
        lines.append('')
        for p in panels:
            lines.append(panel_md(p))
            lines.append('')
    return '\n'.join(lines)


def render(project: dict) -> str:
    title = project.get('title', 'Untitled')
    worldview = project.get('worldview', '').strip()
    style = project.get('style', 'shonen')
    aspect = project.get('aspectRatio', 'A4')
    color = project.get('colorMode', 'color')
    language = project.get('language', 'zh')
    characters = project.get('characters', [])
    pages = project.get('pages', [])

    lines = [
        f"# 《{title}》",
        '',
        f"> 生成时间:{datetime.now().strftime('%Y-%m-%d %H:%M')}  ·  画风:{style}  ·  比例:{aspect}  ·  颜色:{color}  ·  语言:{language}",
        '',
    ]

    if worldview:
        lines += ['## 世界观', '', worldview, '']

    if characters:
        lines += ['## 角色', '']
        for c in characters:
            lines.append(character_md(c))
            lines.append('')

    if pages:
        lines += ['## 页面', '']
        for p in pages:
            lines.append(page_md(p))
            lines.append('')

    lines += ['---', '', '*由 manga-studio skill 自动生成*']
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--in', dest='inp', required=True)
    p.add_argument('--out')
    args = p.parse_args()

    project = json.loads(Path(args.inp).read_text(encoding='utf-8'))
    md = render(project)
    if args.out:
        Path(args.out).write_text(md, encoding='utf-8')
        print(f"wrote {args.out} ({len(md)} chars)", file=sys.stderr)
    else:
        print(md)


if __name__ == '__main__':
    main()
