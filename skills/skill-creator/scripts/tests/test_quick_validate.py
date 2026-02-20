#!/usr/bin/env python3
"""Tests for quick_validate.py"""

import sys
from pathlib import Path

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from quick_validate import validate_skill


def _write(path, content):
    path.write_text(content, encoding='utf-8')


def _make_valid_skill(tmp_path):
    """Create a minimal valid skill directory."""
    _write(tmp_path / 'SKILL.md', '---\nname: test-skill\ndescription: Does X when Y\n---\n# Test')
    return tmp_path


# --- Core validation ---

def test_valid_skill_passes(tmp_path):
    _make_valid_skill(tmp_path)
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert 'valid' in msg.lower()


def test_missing_skill_md(tmp_path):
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'not found' in msg.lower()


def test_no_frontmatter(tmp_path):
    _write(tmp_path / 'SKILL.md', '# No frontmatter here')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'frontmatter' in msg.lower()


def test_invalid_frontmatter(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nbroken\n# No closing ---')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid


def test_missing_name(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\ndescription: test desc\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'name' in msg.lower()


def test_missing_description(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: test-skill\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'description' in msg.lower()


# --- Name validation ---

def test_name_not_kebab_case(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: TestSkill\ndescription: test\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'hyphen-case' in msg.lower()


def test_name_leading_hyphen(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: -test-skill\ndescription: test\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid


def test_name_consecutive_hyphens(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: test--skill\ndescription: test\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid


def test_name_mismatch_directory_warns(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: other-name\ndescription: test desc\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert any("doesn't match" in w for w in warnings)


# --- Description validation ---

def test_description_angle_brackets(tmp_path):
    _write(tmp_path / 'SKILL.md', '---\nname: test-skill\ndescription: Use <thing>\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'angle brackets' in msg.lower()


def test_description_over_200_chars(tmp_path):
    long_desc = 'x' * 200
    _write(tmp_path / 'SKILL.md', f'---\nname: test-skill\ndescription: {long_desc}\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert not valid
    assert 'too long' in msg.lower()


def test_description_at_199_chars_passes(tmp_path):
    desc = 'x' * 199
    _write(tmp_path / 'SKILL.md', f'---\nname: test-skill\ndescription: {desc}\n---\n# Test')
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid


# --- Size limits ---

def test_skill_md_over_150_lines_warns(tmp_path):
    content = '---\nname: test-skill\ndescription: test desc\n---\n' + '\n'.join(['line'] * 160)
    _write(tmp_path / 'SKILL.md', content)
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid  # Warning, not failure
    assert any('SKILL.md' in w and 'lines' in w for w in warnings)


def test_reference_over_150_lines_warns(tmp_path):
    _make_valid_skill(tmp_path)
    refs = tmp_path / 'references'
    refs.mkdir()
    _write(refs / 'big-ref.md', '\n'.join(['line'] * 160))
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert any('big-ref.md' in w for w in warnings)


def test_reference_under_150_lines_no_warning(tmp_path):
    skill_dir = tmp_path / 'test-skill'
    skill_dir.mkdir()
    _write(skill_dir / 'SKILL.md', '---\nname: test-skill\ndescription: Does X when Y\n---\n# Test')
    refs = skill_dir / 'references'
    refs.mkdir()
    _write(refs / 'small-ref.md', '\n'.join(['line'] * 50))
    valid, msg, warnings = validate_skill(skill_dir)
    assert valid
    assert len(warnings) == 0


# --- Script test coverage ---

def test_script_without_test_warns(tmp_path):
    _make_valid_skill(tmp_path)
    scripts = tmp_path / 'scripts'
    scripts.mkdir()
    _write(scripts / 'my_script.py', 'print("hello")')
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert any('my_script.py' in w and 'no test' in w for w in warnings)


def test_script_with_test_no_warning(tmp_path):
    _make_valid_skill(tmp_path)
    scripts = tmp_path / 'scripts'
    scripts.mkdir()
    tests = scripts / 'tests'
    tests.mkdir()
    _write(scripts / 'my_script.py', 'print("hello")')
    _write(tests / 'test_my_script.py', 'def test_it(): pass')
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert not any('my_script.py' in w for w in warnings)


def test_encoding_utils_excluded_from_test_check(tmp_path):
    _make_valid_skill(tmp_path)
    scripts = tmp_path / 'scripts'
    scripts.mkdir()
    _write(scripts / 'encoding_utils.py', 'pass')
    valid, msg, warnings = validate_skill(tmp_path)
    assert valid
    assert not any('encoding_utils.py' in w for w in warnings)
