#!/usr/bin/env python3
"""
Quick validation script for skills - validates structure, metadata, and quality gates.
"""

import sys
import re
from pathlib import Path

from encoding_utils import configure_utf8_console, read_text_utf8

# Fix Windows console encoding for Unicode output
configure_utf8_console()


def validate_skill(skill_path):
    """
    Validate a skill directory against all quality gates.

    Returns:
        (valid, message, warnings) — valid is bool, message is str, warnings is list[str]
    """
    skill_path = Path(skill_path)
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", []

    # Read and validate frontmatter
    content = read_text_utf8(skill_md)
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", []

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", []

    frontmatter = match.group(1)

    # Check required fields
    if 'name:' not in frontmatter:
        return False, "Missing 'name' in frontmatter", []
    if 'description:' not in frontmatter:
        return False, "Missing 'description' in frontmatter", []

    # Extract and validate name
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"Name '{name}' should be hyphen-case (lowercase letters, digits, and hyphens only)", []
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"Name '{name}' cannot start/end with hyphen or contain consecutive hyphens", []
        # CHECK: Name matches directory name
        if name != skill_path.name:
            warnings.append(f"Name '{name}' doesn't match directory '{skill_path.name}'")

    # Extract and validate description
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)", []
        # CHECK: Description length < 200 chars
        if len(description) >= 200:
            return False, f"Description too long ({len(description)} chars, max 199)", []

    # CHECK: SKILL.md < 150 lines
    lines = content.split('\n')
    if len(lines) > 150:
        warnings.append(f"SKILL.md has {len(lines)} lines (max 150)")

    # CHECK: Reference files < 150 lines
    refs_dir = skill_path / 'references'
    if refs_dir.exists():
        for ref_file in refs_dir.rglob('*.md'):
            try:
                ref_content = read_text_utf8(ref_file)
                ref_lines = ref_content.split('\n')
                if len(ref_lines) > 150:
                    rel_path = ref_file.relative_to(skill_path)
                    warnings.append(f"{rel_path} has {len(ref_lines)} lines (max 150)")
            except Exception:
                rel_path = ref_file.relative_to(skill_path)
                warnings.append(f"Could not read {rel_path}")

    # CHECK: Scripts have tests
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        scripts = [f for f in scripts_dir.glob('*.py')
                   if not f.name.startswith('test_')
                   and f.name != 'encoding_utils.py'
                   and f.name != '__init__.py']
        tests_dir = scripts_dir / 'tests'
        for script in scripts:
            test_file = tests_dir / f'test_{script.name}' if tests_dir.exists() else None
            if not test_file or not test_file.exists():
                warnings.append(f"Script {script.name} has no test file")

    if warnings:
        return True, "Skill is valid with warnings", warnings
    return True, "Skill is valid!", []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message, warnings = validate_skill(sys.argv[1])
    print(message)
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")
    sys.exit(0 if valid else 1)
