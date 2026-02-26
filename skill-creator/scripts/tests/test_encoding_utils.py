#!/usr/bin/env python3
"""Tests for encoding_utils.py"""

import sys
from pathlib import Path

import pytest

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from encoding_utils import configure_utf8_console, read_text_utf8, write_text_utf8


def test_configure_utf8_console_does_not_crash():
    """Should run without error on any platform."""
    configure_utf8_console()


def test_write_and_read_utf8(tmp_path):
    f = tmp_path / 'test.txt'
    write_text_utf8(f, 'hello world')
    assert read_text_utf8(f) == 'hello world'


def test_unicode_roundtrip(tmp_path):
    f = tmp_path / 'unicode.txt'
    content = 'Hello Unicode! Arrows: → ← ↑ ↓'
    write_text_utf8(f, content)
    assert read_text_utf8(f) == content


def test_emoji_roundtrip(tmp_path):
    f = tmp_path / 'emoji.txt'
    content = 'Status: ✅ ❌ ⚠ 🚀'
    write_text_utf8(f, content)
    assert read_text_utf8(f) == content


def test_empty_file(tmp_path):
    f = tmp_path / 'empty.txt'
    write_text_utf8(f, '')
    assert read_text_utf8(f) == ''


def test_multiline(tmp_path):
    f = tmp_path / 'multi.txt'
    content = 'line1\nline2\nline3'
    write_text_utf8(f, content)
    assert read_text_utf8(f) == content
