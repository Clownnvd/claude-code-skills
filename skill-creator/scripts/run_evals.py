#!/usr/bin/env python3
"""
Run eval JSON files as executable tests against skill-creator scripts.

Usage:
    python run_evals.py [eval_dir]

Reads eval-*.json files and runs automated checks where possible.
Reports pass/fail/skip for each test case.
"""

import json
import sys
import tempfile
from pathlib import Path

from encoding_utils import configure_utf8_console, write_text_utf8
from quick_validate import validate_skill
from init_skill import init_skill

configure_utf8_console()


def run_validate_evals(tests):
    """Run eval tests that exercise validation."""
    results = []
    for test in tests:
        test_id = test['id']
        setup = test.get('setup', '')

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # Try to set up test scenario based on setup description
            if 'missing' in setup.lower() and 'skill.md' in setup.lower():
                # No SKILL.md
                valid, msg, warnings = validate_skill(tmp_path)
                passed = not valid
            elif 'no frontmatter' in setup.lower() or 'missing frontmatter' in setup.lower():
                write_text_utf8(tmp_path / 'SKILL.md', '# No frontmatter')
                valid, msg, warnings = validate_skill(tmp_path)
                passed = not valid
            elif 'missing name' in setup.lower():
                write_text_utf8(tmp_path / 'SKILL.md', '---\ndescription: test\n---\n# T')
                valid, msg, warnings = validate_skill(tmp_path)
                passed = not valid
            elif 'invalid name' in setup.lower():
                write_text_utf8(tmp_path / 'SKILL.md', '---\nname: Bad_Name\ndescription: test\n---\n# T')
                valid, msg, warnings = validate_skill(tmp_path)
                passed = not valid
            else:
                results.append((test_id, 'SKIP', 'Cannot auto-run this test'))
                continue

            status = 'PASS' if passed else 'FAIL'
            results.append((test_id, status, msg))

    return results


def run_init_evals(tests):
    """Run eval tests that exercise init_skill."""
    results = []
    for test in tests:
        test_id = test['id']

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            if 'basic' in test_id or 'init' in test_id.lower():
                result = init_skill('test-skill', str(tmp_path))
                passed = result is not None and (tmp_path / 'test-skill' / 'SKILL.md').exists()
            elif 'duplicate' in test_id:
                init_skill('test-skill', str(tmp_path))
                result = init_skill('test-skill', str(tmp_path))
                passed = result is None
            else:
                results.append((test_id, 'SKIP', 'Cannot auto-run this test'))
                continue

            status = 'PASS' if passed else 'FAIL'
            results.append((test_id, status, ''))

    return results


def run_evals(eval_dir):
    """Run all eval JSON files in directory."""
    eval_path = Path(eval_dir)
    all_results = []
    total = 0
    passed = 0
    skipped = 0

    for eval_file in sorted(eval_path.glob('eval-*.json')):
        data = json.loads(eval_file.read_text(encoding='utf-8'))
        eval_name = data.get('eval_name', eval_file.stem)
        tests = data.get('tests', [])

        print(f"\n{'='*60}")
        print(f"Running: {eval_name} ({len(tests)} tests)")
        print(f"{'='*60}")

        if 'validate' in eval_name or 'quality' in eval_name:
            results = run_validate_evals(tests)
        elif 'init' in eval_name:
            results = run_init_evals(tests)
        else:
            results = [(t['id'], 'SKIP', 'No runner for this eval type') for t in tests]

        for test_id, status, msg in results:
            icon = {'PASS': '✅', 'FAIL': '❌', 'SKIP': '⏭'}[status]
            print(f"  {icon} {test_id}: {status} {msg}")
            total += 1
            if status == 'PASS':
                passed += 1
            elif status == 'SKIP':
                skipped += 1

        all_results.extend(results)

    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} passed, {skipped} skipped, {total - passed - skipped} failed")
    print(f"{'='*60}")

    return all_results


if __name__ == '__main__':
    eval_dir = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).parent.parent / 'evals')
    results = run_evals(eval_dir)
    failures = [r for r in results if r[1] == 'FAIL']
    sys.exit(1 if failures else 0)
