#!/usr/bin/env python3
"""Tests for init_skill.py"""

import sys
from pathlib import Path

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from init_skill import init_skill, title_case_skill_name, SKILL_TYPES


# --- title_case_skill_name ---

def test_title_case_single_word():
    assert title_case_skill_name('payment') == 'Payment'


def test_title_case_multi_word():
    assert title_case_skill_name('payment-integration') == 'Payment Integration'


def test_title_case_with_numbers():
    assert title_case_skill_name('api-v2-helper') == 'Api V2 Helper'


# --- init_skill (general) ---

def test_creates_skill_directory(tmp_path):
    result = init_skill('test-skill', str(tmp_path))
    assert result is not None
    skill_dir = tmp_path / 'test-skill'
    assert skill_dir.exists()
    assert skill_dir.is_dir()


def test_creates_skill_md(tmp_path):
    init_skill('test-skill', str(tmp_path))
    skill_md = tmp_path / 'test-skill' / 'SKILL.md'
    assert skill_md.exists()
    content = skill_md.read_text(encoding='utf-8')
    assert 'name: test-skill' in content
    assert 'Test Skill' in content


def test_creates_license(tmp_path):
    init_skill('test-skill', str(tmp_path))
    license_file = tmp_path / 'test-skill' / 'LICENSE.txt'
    assert license_file.exists()
    content = license_file.read_text(encoding='utf-8')
    assert 'Apache License' in content


def test_creates_subdirectories(tmp_path):
    init_skill('test-skill', str(tmp_path))
    skill_dir = tmp_path / 'test-skill'
    assert (skill_dir / 'scripts').is_dir()
    assert (skill_dir / 'references').is_dir()
    assert (skill_dir / 'assets').is_dir()


def test_creates_example_files(tmp_path):
    init_skill('test-skill', str(tmp_path))
    skill_dir = tmp_path / 'test-skill'
    assert (skill_dir / 'scripts' / 'example.py').exists()
    assert (skill_dir / 'references' / 'api_reference.md').exists()
    assert (skill_dir / 'references' / 'best-practices.md').exists()
    assert (skill_dir / 'assets' / 'example_asset.txt').exists()


def test_best_practices_under_150_lines(tmp_path):
    init_skill('test-skill', str(tmp_path))
    bp = tmp_path / 'test-skill' / 'references' / 'best-practices.md'
    content = bp.read_text(encoding='utf-8')
    lines = content.split('\n')
    assert len(lines) <= 150, f"best-practices.md has {len(lines)} lines, max 150"


def test_duplicate_directory_fails(tmp_path):
    init_skill('test-skill', str(tmp_path))
    result = init_skill('test-skill', str(tmp_path))
    assert result is None


def test_nested_path_creation(tmp_path):
    nested = tmp_path / 'deep' / 'nested' / 'path'
    result = init_skill('test-skill', str(nested))
    assert result is not None
    assert (nested / 'test-skill' / 'SKILL.md').exists()


def test_skill_md_has_frontmatter(tmp_path):
    init_skill('test-skill', str(tmp_path))
    content = (tmp_path / 'test-skill' / 'SKILL.md').read_text(encoding='utf-8')
    assert content.startswith('---')
    assert 'name: test-skill' in content
    assert 'description:' in content


# --- --type flag ---

def test_scoring_type_uses_template(tmp_path):
    init_skill('test-scoring', str(tmp_path), skill_type='scoring')
    content = (tmp_path / 'test-scoring' / 'SKILL.md').read_text(encoding='utf-8')
    assert 'Scoring' in content
    assert 'criteria' in content.lower() or 'Criteria' in content


def test_generate_type_uses_template(tmp_path):
    init_skill('test-gen', str(tmp_path), skill_type='generate')
    content = (tmp_path / 'test-gen' / 'SKILL.md').read_text(encoding='utf-8')
    assert 'Generate' in content


def test_review_type_uses_template(tmp_path):
    init_skill('test-review', str(tmp_path), skill_type='review')
    content = (tmp_path / 'test-review' / 'SKILL.md').read_text(encoding='utf-8')
    assert 'Review' in content


def test_all_types_defined():
    expected = {'general', 'scoring', 'fix', 'generate', 'migrate', 'review', 'test'}
    assert set(SKILL_TYPES.keys()) == expected


# --- --minimal flag ---

def test_minimal_creates_skill_md(tmp_path):
    init_skill('test-min', str(tmp_path), minimal=True)
    assert (tmp_path / 'test-min' / 'SKILL.md').exists()


def test_minimal_creates_license(tmp_path):
    init_skill('test-min', str(tmp_path), minimal=True)
    assert (tmp_path / 'test-min' / 'LICENSE.txt').exists()


def test_minimal_creates_empty_dirs(tmp_path):
    init_skill('test-min', str(tmp_path), minimal=True)
    skill_dir = tmp_path / 'test-min'
    assert (skill_dir / 'scripts').is_dir()
    assert (skill_dir / 'references').is_dir()
    assert (skill_dir / 'assets').is_dir()


def test_minimal_no_example_files(tmp_path):
    init_skill('test-min', str(tmp_path), minimal=True)
    skill_dir = tmp_path / 'test-min'
    assert not (skill_dir / 'scripts' / 'example.py').exists()
    assert not (skill_dir / 'references' / 'api_reference.md').exists()
    assert not (skill_dir / 'assets' / 'example_asset.txt').exists()
