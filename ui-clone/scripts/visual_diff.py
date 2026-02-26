#!/usr/bin/env python3
"""
Compare implementation screenshot vs original PageFlows screenshot.
Reports match % and saves a highlighted diff image.

Usage:
  # Compare two local files:
  python tools/visual_diff.py --original screenshots/claude/onboarding/01.png --impl .tmp/impl/01.png

  # Screenshot a live URL and compare:
  python tools/visual_diff.py --original screenshots/claude/onboarding/01.png --url http://localhost:3000/onboarding

  # Batch compare all screens in a flow:
  python tools/visual_diff.py --manifest .tmp/claude/manifest.json --base-url http://localhost:3000 --routes-map .tmp/claude/routes.json
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageEnhance, ImageDraw
except ImportError:
    print("[error] Pillow not installed. Run: pip install -r tools/requirements.txt")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────
# Browser screenshot via agent-browser
# ──────────────────────────────────────────────────────────────

def screenshot_url(url, output_path, session="visual-diff"):
    """Take a full-page screenshot of a URL."""
    subprocess.run(["agent-browser", "--session", session, "open", url], check=True, capture_output=True)
    subprocess.run(["agent-browser", "--session", session, "wait", "--load", "networkidle"],
                   check=True, capture_output=True)
    subprocess.run(["agent-browser", "--session", session, "screenshot", "--full", str(output_path)],
                   check=True, capture_output=True)


# ──────────────────────────────────────────────────────────────
# Image comparison
# ──────────────────────────────────────────────────────────────

DIFF_THRESHOLD = 20  # Per-channel difference to count as "different"


def compare_images(original_path, impl_path, diff_output_path=None):
    """Compare two images. Returns a result dict."""
    img1 = Image.open(original_path).convert("RGB")
    img2 = Image.open(impl_path).convert("RGB")

    # Resize both to the same size (use smaller dimension)
    target_w = min(img1.width, img2.width)
    target_h = min(img1.height, img2.height)
    img1 = img1.resize((target_w, target_h), Image.LANCZOS)
    img2 = img2.resize((target_w, target_h), Image.LANCZOS)

    diff = ImageChops.difference(img1, img2)
    pixels = list(diff.getdata())
    total = len(pixels)

    diff_count = sum(
        1 for (r, g, b) in pixels
        if r > DIFF_THRESHOLD or g > DIFF_THRESHOLD or b > DIFF_THRESHOLD
    )
    diff_pct = round(diff_count / total * 100, 1)
    match_pct = round(100 - diff_pct, 1)

    status = "PASS" if match_pct >= 80 else ("WARN" if match_pct >= 60 else "FAIL")

    # Create diff image: dimmed original + red highlights on diff pixels
    if diff_output_path:
        dimmed = ImageEnhance.Brightness(img1).enhance(0.45)
        result_img = dimmed.copy()
        enhanced_diff = ImageEnhance.Brightness(diff).enhance(4.0)
        diff_pixels = list(enhanced_diff.getdata())
        orig_pixels = list(result_img.getdata())
        new_pixels = [
            (220, 50, 50) if (d[0] > 50 or d[1] > 50 or d[2] > 50) else o
            for d, o in zip(diff_pixels, orig_pixels)
        ]
        result_img.putdata(new_pixels)

        # Add text overlay
        draw = ImageDraw.Draw(result_img)
        color = (80, 200, 80) if status == "PASS" else ((220, 180, 0) if status == "WARN" else (220, 60, 60))
        draw.rectangle([0, 0, 220, 28], fill=(0, 0, 0, 180))
        draw.text((8, 6), f"{status}  {match_pct}% match  ({diff_pct}% diff)", fill=color)

        Path(diff_output_path).parent.mkdir(parents=True, exist_ok=True)
        result_img.save(str(diff_output_path))

    return {
        "original": str(original_path),
        "implementation": str(impl_path),
        "match_percentage": match_pct,
        "diff_percentage": diff_pct,
        "diff_pixels": diff_count,
        "total_pixels": total,
        "status": status,
        "diff_image": str(diff_output_path) if diff_output_path else None,
    }


# ──────────────────────────────────────────────────────────────
# Single comparison
# ──────────────────────────────────────────────────────────────

def run_single(original, impl_path, url, output, threshold):
    if not impl_path and not url:
        print("[error] Provide --impl or --url", file=sys.stderr)
        sys.exit(1)

    # Screenshot the URL if needed
    if url:
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        impl_path = tmp.name
        tmp.close()
        print(f"[->] Screenshotting {url} …")
        try:
            screenshot_url(url, impl_path)
        except subprocess.CalledProcessError as e:
            print(f"[error] agent-browser failed: {e}", file=sys.stderr)
            sys.exit(1)

    diff_out = output or str(Path(original).parent / "diff-output.png")
    result = compare_images(original, impl_path, diff_out)

    symbol = "OK" if result["status"] == "PASS" else ("WARN" if result["status"] == "WARN" else "FAIL")
    print(f"\n{symbol}  {result['match_percentage']}% match  [{result['status']}]")
    print(f"   Diff: {result['diff_percentage']}% of pixels changed")
    if result["diff_image"]:
        print(f"   Diff image: {result['diff_image']}")

    if result["match_percentage"] < threshold:
        print(f"\n[fail] Below threshold ({threshold}%). Fix and re-run.")
        sys.exit(1)
    else:
        print(f"\n[pass] Meets threshold ({threshold}%).")


# ──────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual diff: original vs implementation")
    parser.add_argument("--original", help="Original PageFlows screenshot")
    parser.add_argument("--impl", help="Implementation screenshot to compare")
    parser.add_argument("--url", help="URL to screenshot for comparison (uses agent-browser)")
    parser.add_argument("--output", help="Output diff image path")
    parser.add_argument("--threshold", type=int, default=80,
                        help="Pass threshold in %% (default: 80)")
    args = parser.parse_args()

    if not args.original:
        parser.print_help()
        sys.exit(1)

    run_single(args.original, args.impl, args.url, args.output, args.threshold)
