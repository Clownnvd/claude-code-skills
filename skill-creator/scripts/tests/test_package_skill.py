#!/usr/bin/env python3
"""Tests for package_skill.py"""

import sys
import zipfile
from pathlib import Path

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from package_skill import package_skill, should_exclude


def _write(path, content=''):
    path.write_text(content, encoding='utf-8')


def _make_valid_skill(tmp_path, name='test-skill'):
    """Create a minimal valid skill directory."""
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    _write(skill_dir / 'SKILL.md', f'---\nname: {name}\ndescription: Does X when Y\n---\n# Test')
    return skill_dir


# --- should_exclude ---

def test_excludes_pycache(tmp_path):
    f = tmp_path / '__pycache__' / 'module.pyc'
    assert should_exclude(f, tmp_path)


def test_excludes_evals_dir(tmp_path):
    f = tmp_path / 'evals' / 'eval-test.json'
    assert should_exclude(f, tmp_path)


def test_excludes_pyc_files(tmp_path):
    f = tmp_path / 'scripts' / 'main.pyc'
    assert should_exclude(f, tmp_path)


def test_includes_normal_files(tmp_path):
    f = tmp_path / 'SKILL.md'
    assert not should_exclude(f, tmp_path)


def test_includes_script_files(tmp_path):
    f = tmp_path / 'scripts' / 'main.py'
    assert not should_exclude(f, tmp_path)


# --- package_skill ---

def test_packages_valid_skill(tmp_path):
    skill_dir = _make_valid_skill(tmp_path)
    output = tmp_path / 'output'
    output.mkdir()
    result = package_skill(str(skill_dir), str(output))
    assert result is not None
    assert result.exists()
    assert result.suffix == '.zip'


def test_zip_contains_skill_md(tmp_path):
    skill_dir = _make_valid_skill(tmp_path)
    output = tmp_path / 'output'
    output.mkdir()
    result = package_skill(str(skill_dir), str(output))
    with zipfile.ZipFile(result) as zf:
        names = zf.namelist()
        assert any('SKILL.md' in n for n in names)


def test_zip_excludes_evals(tmp_path):
    skill_dir = _make_valid_skill(tmp_path)
    evals = skill_dir / 'evals'
    evals.mkdir()
    _write(evals / 'eval-test.json', '{}')
    output = tmp_path / 'output'
    output.mkdir()
    result = package_skill(str(skill_dir), str(output))
    with zipfile.ZipFile(result) as zf:
        names = zf.namelist()
        assert not any('evals' in n for n in names)


def test_zip_excludes_pycache(tmp_path):
    skill_dir = _make_valid_skill(tmp_path)
    cache = skill_dir / '__pycache__'
    cache.mkdir()
    _write(cache / 'module.pyc', '')
    output = tmp_path / 'output'
    output.mkdir()
    result = package_skill(str(skill_dir), str(output))
    with zipfile.ZipFile(result) as zf:
        names = zf.namelist()
        assert not any('__pycache__' in n for n in names)


def test_rejects_nonexistent_path(tmp_path):
    result = package_skill(str(tmp_path / 'nonexistent'))
    assert result is None


def test_rejects_file_path(tmp_path):
    f = tmp_path / 'not-a-dir.txt'
    _write(f, 'hello')
    result = package_skill(str(f))
    assert result is None


def test_rejects_invalid_skill(tmp_path):
    skill_dir = tmp_path / 'bad-skill'
    skill_dir.mkdir()
    # No SKILL.md
    result = package_skill(str(skill_dir))
    assert result is None


def test_default_output_dir(tmp_path):
    skill_dir = _make_valid_skill(tmp_path)
    result = package_skill(str(skill_dir))
    assert result is not None
    assert result.exists()
    # Clean up zip from cwd
    result.unlink()
