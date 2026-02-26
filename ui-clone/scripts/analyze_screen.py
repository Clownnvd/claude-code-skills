#!/usr/bin/env python3
"""
Analyze a screenshot to extract design tokens.
Uses PIL for color analysis. Outputs structured JSON.

Usage:
  python tools/analyze_screen.py --image screenshots/claude/onboarding/01-terms.png
  python tools/analyze_screen.py --image screenshots/claude/onboarding/01-terms.png --output .tmp/claude/tokens.json
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("[error] Pillow not installed. Run: pip install -r tools/requirements.txt")
    sys.exit(1)


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def brightness(r, g, b):
    return (0.299 * r + 0.587 * g + 0.114 * b)


def extract_colors(image_path, top_n=12):
    """Extract dominant colors using quantization."""
    img = Image.open(image_path).convert("RGB")
    # Resize for speed
    img_small = img.resize((150, 150), Image.LANCZOS)
    # Quantize to reduce noise
    quantized = img_small.quantize(colors=24, method=Image.Quantize.FASTOCTREE).convert("RGB")

    pixels = list(quantized.getdata())
    total = len(pixels)
    counter = Counter(pixels)

    colors = []
    for (r, g, b), count in counter.most_common(top_n):
        colors.append({
            "hex": rgb_to_hex(r, g, b),
            "rgb": [r, g, b],
            "percentage": round(count / total * 100, 1),
            "brightness": round(brightness(r, g, b)),
            "role": classify_color(r, g, b),
        })
    return colors


def classify_color(r, g, b):
    """Guess the likely role of a color."""
    br = brightness(r, g, b)
    saturation = max(r, g, b) - min(r, g, b)

    if br > 240:
        return "background/surface"
    if br < 30:
        return "text/dark"
    if saturation > 80:
        # Colorful — likely brand/accent
        if r > g and r > b:
            return "brand-accent (warm)"
        if b > r and b > g:
            return "brand-accent (cool)"
        return "brand-accent"
    if br > 200:
        return "background/light"
    if br > 100:
        return "text-muted/border"
    return "text/dark-gray"


def extract_layout(image_path):
    """Basic layout heuristics from pixel analysis."""
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    def region_dominant(left, top, right, bottom):
        crop = img.crop((left, top, right, bottom)).resize((20, 20))
        pixels = list(crop.getdata())
        return Counter(pixels).most_common(1)[0][0]

    left_dom = region_dominant(0, 0, max(1, w // 12), h)
    center_dom = region_dominant(w // 4, 0, w, h)
    top_dom = region_dominant(0, 0, w, max(1, h // 12))

    left_br = brightness(*left_dom)
    center_br = brightness(*center_dom)
    top_br = brightness(*top_dom)

    has_sidebar = abs(left_br - center_br) > 25
    has_topbar = abs(top_br - center_br) > 25

    return {
        "width": w,
        "height": h,
        "aspect_ratio": round(w / h, 2),
        "has_sidebar": has_sidebar,
        "has_topbar": has_topbar,
        "layout_hint": _layout_hint(w, h, has_sidebar),
    }


def _layout_hint(w, h, has_sidebar):
    if w > h * 1.3 and has_sidebar:
        return "app-shell (sidebar + main)"
    if w > h * 1.5:
        return "split-layout (two columns)"
    if w < h:
        return "single-column (mobile/centered)"
    return "single-column (centered)"


def analyze_screen(image_path):
    path = Path(image_path)
    if not path.exists():
        print(f"[error] File not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    colors = extract_colors(image_path)
    layout = extract_layout(image_path)

    # Find likely background (highest %)
    background = colors[0]["hex"] if colors else "#FFFFFF"
    # Find likely brand color (most saturated non-background)
    brand = next(
        (c["hex"] for c in colors if "brand" in c["role"]),
        None
    )

    return {
        "file": str(path),
        "colors": colors,
        "layout": layout,
        "inferred_tokens": {
            "background": background,
            "brand_accent": brand,
            "text_primary": next(
                (c["hex"] for c in colors if c["role"] in ("text/dark", "text/dark-gray")),
                "#111111"
            ),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze screenshot for design tokens")
    parser.add_argument("--image", required=True, help="Path to screenshot")
    parser.add_argument("--output", help="Save result to JSON file")
    args = parser.parse_args()

    result = analyze_screen(args.image)
    output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[ok] Saved to {args.output}")
    else:
        print(output)
