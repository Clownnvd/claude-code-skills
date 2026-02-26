#!/usr/bin/env python3
"""
Agent Orchestrator — WAT Multi-Agent Framework
Spawns specialist worker agents in parallel waves.
Usage: python scripts/orchestrator.py "Build complete SaaS app"
       python scripts/orchestrator.py --plan .tmp/agents/plan.json
"""
import json
import os
import subprocess
import sys
import concurrent.futures
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("[error] anthropic not installed. Run: pip install anthropic")
    raise

# ── Config ──────────────────────────────────────────────────────────────────
MODEL = "claude-opus-4-6"
AGENTS_DIR = Path(".tmp/agents")
CWD = Path.cwd()

SYSTEM_PROMPT = """You are an orchestration planner. Analyze the project task and decompose it into specialist agents.

Rules:
- Agents in the same wave run in PARALLEL — they must be truly independent
- Later waves can read outputs from earlier waves via .tmp/agents/{name}/output.md
- Each agent should have ONE clear responsibility
- Return ONLY valid JSON, no markdown fences

Return this exact structure:
{
  "project": "short description",
  "agents": [
    {
      "name": "db-agent",
      "skill": "database",
      "task": "specific task description",
      "depends_on": [],
      "reads": []
    }
  ],
  "waves": [
    ["db-agent", "ui-agent"],
    ["auth-agent"],
    ["api-agent"]
  ]
}

Available skills: database, auth, api, ui-clone, claude-ui, ultimateuiux, infrastructure, security, nextjs, stripe, email"""


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def spawn_agent(agent: dict) -> dict:
    """Run a single agent as a claude --print subprocess."""
    name = agent["name"]
    task = agent["task"]
    skill = agent.get("skill")
    reads = agent.get("reads", [])

    output_dir = AGENTS_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "output.md"

    # Build context from dependencies
    context_parts = []
    for dep in reads:
        dep_output = AGENTS_DIR / dep / "output.md"
        if dep_output.exists():
            context_parts.append(f"## Output from {dep}\n{dep_output.read_text()}")

    context = "\n\n".join(context_parts)
    skill_prefix = f"Invoke the '{skill}' skill. Then: " if skill else ""

    prompt = f"""{skill_prefix}You are the {name}.

Task: {task}

{"Context from previous agents:" + context if context else ""}

Write your output to: .tmp/agents/{name}/output.md
List any files you create in: .tmp/agents/{name}/files.json (as JSON array of paths)
"""

    log(f"[{name}] Starting...")

    result = subprocess.run(
        ["claude", "--print", prompt],
        capture_output=True, text=True,
        cwd=str(CWD)
    )

    output = result.stdout
    if result.returncode != 0:
        output = f"ERROR:\n{result.stderr}"

    # Save output
    output_file.write_text(output, encoding="utf-8")
    log(f"[{name}] Done -> {output_file}")

    return {
        "name": name,
        "status": "done" if result.returncode == 0 else "error",
        "output_file": str(output_file),
        "returncode": result.returncode
    }


def run_wave(agents_in_wave: list[dict], wave_num: int) -> list[dict]:
    """Run all agents in a wave in parallel."""
    names = [a["name"] for a in agents_in_wave]
    log(f"=== Wave {wave_num}: {names} (parallel) ===")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents_in_wave)) as executor:
        futures = {
            executor.submit(spawn_agent, agent): agent["name"]
            for agent in agents_in_wave
        }
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                log(f"[{name}] FAILED: {e}")
                results.append({"name": name, "status": "error", "error": str(e)})

    return results


def plan_from_claude(task: str) -> dict:
    """Ask Claude to generate the orchestration plan."""
    log("Orchestrator planning...")
    client = anthropic.Anthropic()

    # Read CLAUDE.md for project context if exists
    claude_md = CWD / "CLAUDE.md"
    project_context = ""
    if claude_md.exists():
        project_context = f"\n\nProject context (CLAUDE.md):\n{claude_md.read_text()[:2000]}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Task: {task}{project_context}"}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:])
    if raw.endswith("```"):
        raw = "\n".join(raw.split("\n")[:-1])

    plan = json.loads(raw)

    # Save plan
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    plan_file = AGENTS_DIR / "plan.json"
    plan_file.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    log(f"Plan saved -> {plan_file}")

    return plan


def orchestrate(task: str = None, plan_file: str = None):
    """Main orchestration entry point."""
    print("\n" + "=" * 60)
    print("  Agent Orchestrator — WAT Multi-Agent Framework")
    print("=" * 60 + "\n")

    # Load or generate plan
    if plan_file:
        plan = json.loads(Path(plan_file).read_text())
        log(f"Loaded plan from {plan_file}")
    else:
        plan = plan_from_claude(task)

    log(f"Project: {plan['project']}")
    log(f"Agents: {len(plan['agents'])} | Waves: {len(plan['waves'])}\n")

    # Index agents by name
    agents_by_name = {a["name"]: a for a in plan["agents"]}

    # Execute wave by wave
    all_results = []
    for i, wave in enumerate(plan["waves"], 1):
        agents_in_wave = [agents_by_name[name] for name in wave if name in agents_by_name]
        wave_results = run_wave(agents_in_wave, i)
        all_results.extend(wave_results)
        print()

    # Summary
    done = [r for r in all_results if r["status"] == "done"]
    errors = [r for r in all_results if r["status"] == "error"]

    summary = f"""# Orchestrator Summary
Generated: {datetime.now().isoformat()}
Project: {plan['project']}

## Results
- Done: {len(done)}/{len(all_results)} agents
- Errors: {len(errors)}

## Agent Outputs
"""
    for r in all_results:
        status_icon = "OK" if r["status"] == "done" else "FAIL"
        summary += f"- [{status_icon}] {r['name']}: {r.get('output_file', 'N/A')}\n"

    summary_file = AGENTS_DIR / "summary.md"
    summary_file.write_text(summary, encoding="utf-8")

    print("=" * 60)
    log(f"Done: {len(done)}/{len(all_results)} agents succeeded")
    log(f"Summary -> {summary_file}")
    if errors:
        log(f"Errors: {[e['name'] for e in errors]}")
    print("=" * 60 + "\n")

    return all_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agent Orchestrator")
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument("--plan", help="Path to existing plan.json")
    args = parser.parse_args()

    if not args.task and not args.plan:
        print("Usage: python orchestrator.py 'task description'")
        print("       python orchestrator.py --plan .tmp/agents/plan.json")
        sys.exit(1)

    orchestrate(task=args.task, plan_file=args.plan)
