#!/usr/bin/env python3
"""
Generate skill reference files from captured screenshots + component map.
Creates skeleton .md files for each component and screen.
Claude fills in the implementation details — this tool creates the structure.

Usage:
  python tools/generate_skill_refs.py --app claude --component-map .tmp/claude/component-map.json
  python tools/generate_skill_refs.py --app notion  --component-map .tmp/notion/component-map.json --output-dir .claude/skills
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def safe_slug(title, max_len=40):
    return title.lower().replace(" ", "-").replace("/", "-").replace("'", "")[:max_len]


def find_source_file(app_name, component_name):
    """Try to locate the built component file."""
    candidates = [
        Path("src") / "components" / f"{component_name}.tsx",
        Path("src") / "components" / app_name / f"{component_name}.tsx",
        Path("src") / "components" / f"{component_name}.tsx",
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def find_page_file(app_name, flow_name):
    candidates = [
        Path("src") / "app" / "(clone)" / flow_name / "page.tsx",
        Path("src") / "app" / f"({app_name})" / flow_name / "page.tsx",
        Path("src") / "app" / flow_name / "page.tsx",
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


# ──────────────────────────────────────────────────────────────
# Reference file generators
# ──────────────────────────────────────────────────────────────

def gen_component_ref(component_name, app_name, component_map):
    shared = component_map.get("shared_components", {})
    info = shared.get(component_name, {})
    source = find_source_file(app_name, component_name)

    lines = [f"# {component_name.replace('-', ' ').title()}\n"]

    if source:
        lines.append(f"**File:** `{source}`")
    else:
        lines.append(f"**File:** `src/components/{component_name}.tsx` _(not yet built)_")

    if info:
        lines.append(f"**Shared:** appears in {info.get('appears_in', '?')} screens "
                     f"({info.get('consistency', '?')}% consistent)")

    lines += [
        "",
        "## States\n",
        "| State | Description |",
        "|-------|-------------|",
        "| default | ... |",
        "| hover | ... |",
        "| active | ... |",
        "",
        "## Key Classes\n",
        "| Element | Class |",
        "|---------|-------|",
        "| Container | ... |",
        "| Active item | ... |",
        "",
        "## Critical Notes\n",
        "_(Add non-obvious decisions, bugs fixed, quirks here)_",
        "",
        "## Screenshots\n",
        "_(Add paths to 1-2 reference screenshots)_",
        "",
    ]
    return "\n".join(lines)


def gen_screen_ref(screen, flow_name, app_name):
    title = screen["title"]
    screenshot = screen.get("screenshot", "")
    source = find_page_file(app_name, flow_name)

    lines = [f"# {title}\n"]
    lines.append(f"**Flow:** `{flow_name}`")

    if source:
        lines.append(f"**File:** `{source}`")
    else:
        lines.append(f"**File:** `src/app/(clone)/{flow_name}/page.tsx` _(not yet built)_")

    if screenshot:
        lines.append(f"**Screenshot:** `{screenshot}`")

    lines += [
        "",
        "## Layout\n",
        "```",
        "┌─────────────────────────────────────┐",
        "│  (ASCII diagram of this screen)     │",
        "└─────────────────────────────────────┘",
        "```",
        "",
        "## Unique Elements\n",
        "_(Elements specific to this screen, not in shared components)_",
        "",
        "## Critical Notes\n",
        "_(Bugs fixed, non-obvious CSS, interaction notes)_",
        "",
    ]
    return "\n".join(lines)


def gen_design_tokens(app_name):
    # Try to read globals.css for tokens
    css_candidates = [
        Path("src") / "app" / "globals.css",
        Path("src") / "styles" / "globals.css",
    ]
    css_content = ""
    for p in css_candidates:
        if p.exists():
            css_content = p.read_text(encoding="utf-8")[:2000]
            break

    lines = [
        f"# Design Tokens — {app_name.title()}\n",
        "## Colors\n",
        "| Token | Value | Usage |",
        "|-------|-------|-------|",
        "| Background | `#...` | Page background |",
        "| Surface | `#...` | Cards, modals |",
        "| Brand accent | `#...` | Primary CTA, logo |",
        "| Text primary | `#...` | Body text |",
        "| Text muted | `#...` | Secondary text |",
        "| Border | `#...` | All borders |",
        "",
        "## Typography\n",
        "| Role | Font | Size |",
        "|------|------|------|",
        "| Heading | ... | ... |",
        "| Body | ... | ... |",
        "",
        "## Spacing\n",
        "| Use | Value |",
        "|-----|-------|",
        "| Section padding | ... |",
        "| Component gap | ... |",
        "",
        "## Tailwind v4 @theme\n",
        "```css",
        "@theme inline {",
        "  --color-background: #...;",
        "  --color-brand: #...;",
        "  --color-border: #...;",
        "}",
        "```",
        "",
    ]

    if css_content:
        lines += [
            "## Extracted from globals.css\n",
            "```css",
            css_content[:800],
            "```",
            "",
        ]

    return "\n".join(lines)


def gen_flows_ref(manifest):
    app = manifest["app"]
    total = manifest["total_screens"]
    flows = manifest["flows"]

    lines = [
        f"# Flows — {app.title()}\n",
        f"**Source:** PageFlows — captured {manifest.get('captured_at', '')[:10]}",
        f"**Total:** {total} screens across {len(flows)} flows\n",
        "## Flow Map\n",
        "| Flow | Screens | Key screen |",
        "|------|---------|------------|",
    ]

    for flow_name, screens in flows.items():
        first = screens[0]["title"] if screens else "-"
        lines.append(f"| `{flow_name}` | {len(screens)} | {first} |")

    lines += [
        "",
        "## Navigation Rules\n",
        "_(Add routing patterns, URL structure, redirects)_",
        "",
    ]
    return "\n".join(lines)


def gen_skill_index(app_name, component_map, manifest):
    shared = list(component_map.get("shared_components", {}).keys())
    flows = list(manifest.get("flows", {}).keys())
    total = manifest.get("total_screens", 0)
    captured = manifest.get("captured_at", "")[:10]

    desc = (
        f"Full {app_name.title()} UI clone: Next.js 16 + Tailwind v4. "
        f"{total} screens, {len(flows)} flows, {len(shared)} shared components. "
        f"Source: PageFlows {captured}."
    )
    # Trim description to < 200 chars
    if len(desc) > 195:
        desc = desc[:192] + "..."

    lines = [
        "---",
        f"name: {app_name}-ui",
        f'description: "{desc}"',
        "---",
        "",
        f"# {app_name.title()} UI — Implementation Index\n",
        f"Source: PageFlows {captured}. {total} screens across {len(flows)} flows.",
        "",
        "---",
        "",
        "## Critical Rules\n",
        "| Bug | Correct |",
        "|-----|---------|",
        "| _(Add top mistakes found during implementation)_ | _(Correct approach)_ |",
        "",
        "---",
        "",
        "## Reference Directory\n",
        "### Design System",
        "- `references/design-tokens.md` — Colors, typography, Tailwind @theme",
        "- `references/flows.md` — All flows, screen map, navigation rules",
        "",
        "### Shared Components",
    ]

    for comp in shared:
        lines.append(f"- `references/components/{comp}.md`")

    if not shared:
        lines.append("- _(Run find_shared_components.py to populate)_")

    lines += ["", "### Pages by Flow"]

    for flow in flows:
        n = len(manifest["flows"].get(flow, []))
        lines.append(f"- `references/pages/{flow}/` — {n} screens")

    lines += [
        "",
        "---",
        "",
        "## Reuse Pattern\n",
        "To implement any screen:",
        "1. Read `references/pages/[flow]/[screen].md`",
        "2. Read linked source file for the actual code",
        "3. Check `references/components/` for shared parts",
        "4. Build — no PageFlows scraping needed",
        "",
    ]

    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def generate_refs(app_name, component_map_path, manifest_path=None, output_dir=None):
    component_map = json.loads(Path(component_map_path).read_text(encoding="utf-8"))

    if not manifest_path:
        manifest_path = str(Path(".tmp") / app_name / "manifest.json")
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))

    skill_dir = Path(output_dir) if output_dir else Path(".claude") / "skills" / f"{app_name}-ui"
    refs_dir = skill_dir / "references"

    print(f"[->] Generating skill for '{app_name}' -> {skill_dir}")

    # 1. SKILL.md
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(gen_skill_index(app_name, component_map, manifest), encoding="utf-8")
    print(f"  [ok] SKILL.md")

    # 2. design-tokens.md
    refs_dir.mkdir(parents=True, exist_ok=True)
    (refs_dir / "design-tokens.md").write_text(gen_design_tokens(app_name), encoding="utf-8")
    print(f"  [ok] references/design-tokens.md")

    # 3. flows.md
    (refs_dir / "flows.md").write_text(gen_flows_ref(manifest), encoding="utf-8")
    print(f"  [ok] references/flows.md")

    # 4. Component refs
    comp_dir = refs_dir / "components"
    comp_dir.mkdir(parents=True, exist_ok=True)
    for comp_name in component_map.get("shared_components", {}):
        content = gen_component_ref(comp_name, app_name, component_map)
        (comp_dir / f"{comp_name}.md").write_text(content, encoding="utf-8")
    print(f"  [ok] references/components/ ({len(component_map.get('shared_components', {}))} files)")

    # 5. Page refs
    pages_dir = refs_dir / "pages"
    for flow_name, screens in manifest.get("flows", {}).items():
        flow_dir = pages_dir / flow_name
        flow_dir.mkdir(parents=True, exist_ok=True)
        for screen in screens:
            slug = safe_slug(screen["title"])
            content = gen_screen_ref(screen, flow_name, app_name)
            (flow_dir / f"{slug}.md").write_text(content, encoding="utf-8")
        print(f"  [ok] references/pages/{flow_name}/ ({len(screens)} screens)")

    print(f"\n[done] Skill generated at {skill_dir}")
    print(f"\nNext:")
    print(f"  1. Fill in Critical Rules in SKILL.md (from your implementation mistakes)")
    print(f"  2. Fill in component refs with key classes/quirks")
    print(f"  3. Commit: cd .claude/skills && git add {app_name}-ui/ && git commit -m 'feat: {app_name}-ui skill'")

    return str(skill_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate skill reference files from implementation")
    parser.add_argument("--app", required=True, help="App name (e.g. claude, notion)")
    parser.add_argument("--component-map", required=True, help="Path to component-map.json")
    parser.add_argument("--manifest", help="Path to manifest.json (auto-detected if omitted)")
    parser.add_argument("--output-dir", help="Output skill directory (default: .claude/skills/[app]-ui)")
    args = parser.parse_args()

    generate_refs(args.app, args.component_map, args.manifest, args.output_dir)
