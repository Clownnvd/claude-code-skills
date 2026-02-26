#!/usr/bin/env python3
"""
Capture all screens for a target app from PageFlows.

Usage:
  python tools/pageflows_capture.py --app claude
  python tools/pageflows_capture.py --app notion --flows "onboarding,settings,login"
  python tools/pageflows_capture.py --app linear --wait 3000
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ──────────────────────────────────────────────────────────────
# agent-browser helpers
# ──────────────────────────────────────────────────────────────

def ab(*args, session=None, stdin_data=None, timeout=60):
    """Run an agent-browser command, return stdout string."""
    cmd = ["agent-browser"]
    if session:
        cmd += ["--session", session]
    cmd += list(args)
    result = subprocess.run(
        cmd,
        input=stdin_data,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if result.returncode != 0 and result.stderr.strip():
        print(f"  [warn] {result.stderr.strip()[:120]}", file=sys.stderr)
    return result.stdout.strip()


def ab_open(url, session, wait_ms=None):
    ab("open", url, session=session)
    ab("wait", "--load", "networkidle", session=session)
    if wait_ms:
        ab("wait", str(wait_ms), session=session)


def ab_eval(js, session):
    """Run JS in the browser via stdin to avoid shell quoting issues."""
    return ab("eval", "--stdin", session=session, stdin_data=js)


def ab_screenshot(output_path, session, full=True):
    args = ["screenshot"]
    if full:
        args.append("--full")
    args.append(str(output_path))
    ab(*args, session=session)


# ──────────────────────────────────────────────────────────────
# Auth
# ──────────────────────────────────────────────────────────────

def load_auth(auth_file, session):
    if os.path.exists(auth_file):
        ab("state", "load", auth_file, session=session)
        print(f"[auth] Loaded session from {auth_file}")
    else:
        print(f"[warn] No auth file at {auth_file}. PageFlows may require login.")
        print("       Run: agent-browser --headed open https://pageflows.com")
        print("       Login manually, then: agent-browser state save pageflows-auth.json")


# ──────────────────────────────────────────────────────────────
# Flow discovery
# ──────────────────────────────────────────────────────────────

DISCOVER_JS = """
JSON.stringify(
  Array.from(document.querySelectorAll('a[href*="/post/desktop-web/"]'))
    .map(a => {
      const m = a.href.match(/\\/post\\/desktop-web\\/([^\\/]+)\\/([^\\/]+)\\//);
      return m ? { flow: m[1], app: m[2], href: a.href } : null;
    })
    .filter((x, i, arr) =>
      x && arr.findIndex(y => y && y.flow === x.flow) === i
    )
)
"""


def discover_flows(app_name, session):
    print(f"[->] Discovering flows for '{app_name}' on PageFlows…")
    search_url = f"https://pageflows.com/search/?q={app_name}"
    ab_open(search_url, session)

    raw = ab_eval(DISCOVER_JS, session)
    try:
        items = json.loads(raw)
        flows = [item["flow"] for item in items if item and item.get("app", "").lower() == app_name.lower()]
        if not flows:
            # Try without app filter — user may have a different slug
            flows = [item["flow"] for item in items if item]
        print(f"[ok]  Found {len(flows)} flows: {', '.join(flows[:10])}")
        return flows
    except (json.JSONDecodeError, TypeError):
        print("[warn] Auto-discovery failed. Pass --flows manually.")
        return []


# ──────────────────────────────────────────────────────────────
# Screen extraction
# ──────────────────────────────────────────────────────────────

SCREENS_JS = """
JSON.stringify(
  Array.from(document.querySelectorAll('li[data-url]'))
    .map(el => ({ title: el.dataset.title || el.textContent.trim(), url: el.dataset.url }))
    .filter((x, i, arr) => x.url && arr.findIndex(y => y.url === x.url) === i)
)
"""


def extract_screens(app_name, flow_name, session, wait_ms):
    url = f"https://pageflows.com/post/desktop-web/{flow_name}/{app_name}/"
    print(f"  [->] {url}")
    ab_open(url, session, wait_ms=wait_ms)

    raw = ab_eval(SCREENS_JS, session)
    try:
        screens = json.loads(raw)
        print(f"  [ok] {len(screens)} screens in '{flow_name}'")
        return screens
    except (json.JSONDecodeError, TypeError):
        print(f"  [warn] Could not extract screens for '{flow_name}'")
        return []


# ──────────────────────────────────────────────────────────────
# Screenshot
# ──────────────────────────────────────────────────────────────

def screenshot_screen(screen_url, output_path, session, wait_ms):
    """Open a screen image URL and save it."""
    ab_open(screen_url, session, wait_ms=wait_ms)
    ab_screenshot(output_path, session, full=True)


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def capture_app(app_name, flows=None, output_dir="screenshots", auth_file="pageflows-auth.json", wait_ms=None):
    session = f"pf-{app_name}"
    app_dir = Path(output_dir) / app_name

    load_auth(auth_file, session)

    if flows is None:
        flows = discover_flows(app_name, session)
    if not flows:
        print("[error] No flows. Use --flows to specify them manually.")
        ab("close", session=session)
        return None

    manifest = {
        "app": app_name,
        "captured_at": datetime.now().isoformat(),
        "flows": {},
        "total_screens": 0,
    }

    for flow in flows:
        print(f"\n[flow] {flow}")
        flow_dir = app_dir / flow
        flow_dir.mkdir(parents=True, exist_ok=True)

        screens = extract_screens(app_name, flow, session, wait_ms)
        flow_screens = []

        for i, screen in enumerate(screens):
            title = screen.get("title", f"screen-{i+1}")
            safe = title.lower().replace(" ", "-").replace("/", "-")[:35]
            name = f"{i+1:02d}-{safe}"
            out_path = flow_dir / f"{name}.png"

            print(f"    [{i+1}/{len(screens)}] {title}")

            if screen.get("url"):
                try:
                    screenshot_screen(screen["url"], str(out_path), session, wait_ms)
                except Exception as e:
                    print(f"    [warn] Failed: {e}")

            flow_screens.append({
                "index": i + 1,
                "title": title,
                "source_url": screen.get("url", ""),
                "screenshot": str(Path(output_dir) / app_name / flow / f"{name}.png"),
            })

        manifest["flows"][flow] = flow_screens
        manifest["total_screens"] += len(flow_screens)

    # Save manifest
    tmp_dir = Path(".tmp") / app_name
    tmp_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = tmp_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    ab("close", session=session)

    print(f"\n[done] {manifest['total_screens']} screens captured")
    print(f"[done] Screenshots -> {app_dir}/")
    print(f"[done] Manifest    -> {manifest_path}")
    print(f"\nNext: python tools/find_shared_components.py --manifest {manifest_path}")

    return str(manifest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture PageFlows screens for any app")
    parser.add_argument("--app", required=True, help="App name slug (e.g. claude, notion, linear)")
    parser.add_argument("--flows", help="Comma-separated flow names (auto-discover if omitted)")
    parser.add_argument("--output-dir", default="screenshots", help="Screenshot output directory")
    parser.add_argument("--auth-file", default="pageflows-auth.json", help="PageFlows auth session file")
    parser.add_argument("--wait", type=int, default=None, help="Extra wait ms after page load (for slow pages)")
    args = parser.parse_args()

    flows = [f.strip() for f in args.flows.split(",")] if args.flows else None
    result = capture_app(
        app_name=args.app,
        flows=flows,
        output_dir=args.output_dir,
        auth_file=args.auth_file,
        wait_ms=args.wait,
    )
    sys.exit(0 if result else 1)
