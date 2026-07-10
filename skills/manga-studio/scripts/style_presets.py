"""
画风预设的 Python 常量,供 build_*.py 脚本 import。
保持和 references/style-presets.md 同步。
"""

STYLE_KEYWORDS = {
    'shonen': (
        'shonen manga style, bold black ink lines, dynamic action lines, '
        'speed effects, sweat drops, exaggerated expressions, large eyes with '
        'sharp highlights, screentone shading, high contrast, energetic '
        'composition, manga panel borders with thick black gutters'
    ),
    'shojo': (
        'shojo manga style, delicate thin lines, soft screentone, sparkles and '
        'flower petals, large detailed eyes with long lashes, soft pastel '
        'colors, flowing hair, emotional close-ups, decorative panel borders, '
        'lace and floral backgrounds'
    ),
    'seinen': (
        'seinen manga style, realistic proportions, detailed backgrounds, '
        'heavy use of cross-hatching and detailed screentone, gritty textures, '
        'mature character design, cinematic framing, complex panel layouts, '
        'muted color palette or stark black and white'
    ),
    'chibi': (
        'chibi / super-deformed style, oversized head (1:2 head-to-body ratio), '
        'tiny body, large round eyes, simple dot-like mouth, minimal detail, '
        'cute kawaii expressions, pastel color palette'
    ),
    'ink-wash': (
        'Chinese ink wash painting style, sumi-e brush strokes, monochromatic '
        'black ink, generous white space (liubai), subtle gray gradients, '
        'calligraphic line quality, minimal detail, atmospheric and poetic mood, '
        'traditional East Asian aesthetics'
    ),
    'webtoon': (
        'webtoon style (Korean manhwa), full color, vertical scroll-friendly '
        'composition, soft digital coloring with gradients, clean line art, '
        'simplified backgrounds, large character close-ups for emotional impact, '
        'vibrant color palette, no panel borders or thin gutters'
    ),
    'realistic-cinematic': (
        'semi-realistic cinematic illustration style, movie-like lighting with '
        'strong shadows, photorealistic textures, anamorphic lens feel, '
        'dramatic color grading, moody atmosphere, characters with realistic '
        'proportions and detailed faces'
    ),
    'custom': '',  # 由用户在使用时填入自定义描述
}

ASPECT_RATIO = {
    'A4':             {'w': 595,  'h': 842,  'value': '210:297', 'image_gen_size': '1024x1448'},
    'portrait-3-4':   {'w': 600,  'h': 800,  'value': '3:4',     'image_gen_size': '1024x1366'},
    'square-1-1':     {'w': 800,  'h': 800,  'value': '1:1',     'image_gen_size': '1024x1024'},
    'landscape-16-9': {'w': 1280, 'h': 720,  'value': '16:9',    'image_gen_size': '1280x720'},
}


if __name__ == '__main__':
    import sys, json
    if len(sys.argv) > 1 and sys.argv[1] == 'styles':
        print(json.dumps(STYLE_KEYWORDS, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == 'ratios':
        print(json.dumps(ASPECT_RATIO, indent=2, ensure_ascii=False))
    else:
        print("usage: python3 style_presets.py [styles|ratios]")
