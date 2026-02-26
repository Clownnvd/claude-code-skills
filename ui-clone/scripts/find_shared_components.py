#!/usr/bin/env python3
"""
Analyze all captured screenshots to find shared UI regions.
Uses perceptual hashing to detect consistent elements across screens.

Usage:
  python tools/find_shared_components.py --manifest .tmp/claude/manifest.json
  python tools/find_shared_components.py --manifest .tmp/notion/manifest.json --threshold 50
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("[error] Pillow not installed. Run: pip install -r tools/requirements.txt")
    sys.exit(1)


# ──────────────────────────────────────────────────────────────
# Perceptual hashing
# ──────────────────────────────────────────────────────────────

def phash(img, size=8):
    """Average hash — simple, fast, good enough for layout comparison."""
    small = img.resize((size, size), Image.LANCZOS).convert("L")
    pixels = list(small.getdata())
    avg = sum(pixels) / len(pixels)
    return "".join("1" if p > avg else "0" for p in pixels)


def hamming(h1, h2):
    return sum(c1 != c2 for c1, c2 in zip(h1, h2))


# ──────────────────────────────────────────────────────────────
# Region definitions (as % of image size)
# ──────────────────────────────────────────────────────────────

REGIONS = {
    "sidebar":      (0.00, 0.00, 0.10, 1.00),   # Left strip
    "topbar":       (0.00, 0.00, 1.00, 0.08),   # Top strip
    "bottom-bar":   (0.00, 0.92, 1.00, 1.00),   # Bottom strip
    "chat-input":   (0.08, 0.80, 1.00, 1.00),   # Bottom-right (common for chat apps)
    "main-hero":    (0.10, 0.10, 0.90, 0.80),   # Central content area
}


def crop_region(img, region):
    w, h = img.size
    return img.crop((
        int(w * region[0]),
        int(h * region[1]),
        int(w * region[2]),
        int(h * region[3]),
    ))


# ──────────────────────────────────────────────────────────────
# Main analysis
# ──────────────────────────────────────────────────────────────

def find_shared(manifest_path, consistency_threshold=60):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    app_name = manifest["app"]

    # Collect all valid screenshots
    all_screens = []
    for flow, screens in manifest["flows"].items():
        for screen in screens:
            p = Path(screen["screenshot"])
            if p.exists():
                all_screens.append({
                    "flow": flow,
                    "title": screen["title"],
                    "path": str(p),
                })

    total = len(all_screens)
    print(f"[ok] Analyzing {total} screens for '{app_name}'")

    if total < 2:
        print("[warn] Need at least 2 screenshots to find shared components.")
        return None

    # Hash each region for every screen
    region_hashes = defaultdict(list)

    for screen in all_screens:
        try:
            img = Image.open(screen["path"])
            for region_name, coords in REGIONS.items():
                region_img = crop_region(img, coords)
                h = phash(region_img)
                region_hashes[region_name].append({
                    "hash": h,
                    "screen": screen,
                })
        except Exception as e:
            print(f"  [warn] Skipping {screen['path']}: {e}", file=sys.stderr)

    # Classify: shared vs unique
    shared_components = {}
    unique_regions = {}

    print("\n--- Region Analysis ---")
    for region_name, hash_list in region_hashes.items():
        n = len(hash_list)
        if n < 2:
            continue

        # For each screen, count how many others are "similar" (hamming ≤ 12)
        similarity_scores = []
        for i, item in enumerate(hash_list):
            similar = sum(
                1 for j, other in enumerate(hash_list)
                if i != j and hamming(item["hash"], other["hash"]) <= 12
            )
            similarity_scores.append(similar / (n - 1))

        consistency = round(sum(similarity_scores) / n * 100)

        if consistency >= consistency_threshold:
            shared_components[region_name] = {
                "consistency": consistency,
                "appears_in": n,
                "type": "shared",
            }
            print(f"  [SHARED] {region_name:<15} {consistency:3d}% consistent across {n} screens")
        else:
            unique_regions[region_name] = {
                "consistency": consistency,
                "type": "unique",
            }
            print(f"  [UNIQUE] {region_name:<15} {consistency:3d}% (varies per screen)")

    # Build order: shared first, then flows in manifest order
    build_order = {
        "shared_first": list(shared_components.keys()),
        "then_screens": list(manifest["flows"].keys()),
    }

    n_shared = len(shared_components)
    n_screens = manifest["total_screens"]
    recommendation = (
        f"Build {n_shared} shared component(s) first, "
        f"then {n_screens} screens across {len(manifest['flows'])} flow(s)"
    )

    component_map = {
        "app": app_name,
        "total_screens": n_screens,
        "shared_components": shared_components,
        "unique_regions": unique_regions,
        "build_order": build_order,
        "recommendation": recommendation,
    }

    # Save
    out_path = Path(".tmp") / app_name / "component-map.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(component_map, indent=2), encoding="utf-8")

    print(f"\n[done] {recommendation}")
    print(f"[done] Component map -> {out_path}")
    print(f"\nNext: python tools/visual_diff.py --help (after building components)")
    print(f"  Or: open {out_path} to review build order")

    return str(out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find shared components across screenshots")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json from pageflows_capture.py")
    parser.add_argument("--threshold", type=int, default=60,
                        help="Consistency %% to classify as 'shared' (default: 60)")
    args = parser.parse_args()
    find_shared(args.manifest, args.threshold)
