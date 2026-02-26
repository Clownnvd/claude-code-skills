#!/usr/bin/env python3
"""Tests for run_evals.py"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from run_evals import run_evals, run_validate_evals, run_init_evals


def test_run_evals_with_empty_dir(tmp_path):
    """Running evals on an empty dir returns empty results."""
    results = run_evals(str(tmp_path))
    assert results == []


def test_run_evals_with_valid_eval_file(tmp_path):
    """Running a basic init eval file passes."""
    eval_data = {
        "skill": "test",
        "eval_name": "eval-init-test",
        "tests": [
            {
                "id": "basic-initialization",
                "name": "Basic Init",
                "prompt": "init test-skill",
                "setup": "Empty directory.",
                "expectations": ["SKILL.md created"]
            }
        ]
    }
    eval_file = tmp_path / 'eval-init-test.json'
    eval_file.write_text(json.dumps(eval_data), encoding='utf-8')
    results = run_evals(str(tmp_path))
    assert len(results) == 1
    assert results[0][0] == 'basic-initialization'
    assert results[0][1] == 'PASS'


def test_run_validate_evals_missing_skill_md():
    """Validate eval catches missing SKILL.md."""
    tests = [{"id": "test-missing", "setup": "Missing SKILL.md."}]
    results = run_validate_evals(tests)
    assert len(results) == 1
    assert results[0][1] == 'PASS'


def test_run_validate_evals_invalid_name():
    """Validate eval catches invalid name."""
    tests = [{"id": "test-invalid", "setup": "Invalid name format."}]
    results = run_validate_evals(tests)
    assert len(results) == 1
    assert results[0][1] == 'PASS'
