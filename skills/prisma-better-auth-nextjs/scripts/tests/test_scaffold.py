#!/usr/bin/env python3
"""Tests for scaffold.py"""

import os
import shutil
import sys
import tempfile
import unittest

# Add parent dir to path so we can import scaffold
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scaffold import FILES, scaffold


class TestScaffold(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_creates_all_files(self):
        created = scaffold(self.tmpdir)
        self.assertEqual(len(created), len(FILES))
        for rel_path in FILES:
            full_path = os.path.join(self.tmpdir, rel_path)
            self.assertTrue(os.path.exists(full_path), f"Missing: {rel_path}")

    def test_file_contents_match(self):
        scaffold(self.tmpdir)
        for rel_path, expected in FILES.items():
            full_path = os.path.join(self.tmpdir, rel_path)
            with open(full_path, "r", encoding="utf-8") as f:
                actual = f.read()
            self.assertEqual(actual, expected, f"Content mismatch: {rel_path}")

    def test_skips_existing_files(self):
        scaffold(self.tmpdir)
        created_second = scaffold(self.tmpdir)
        self.assertEqual(len(created_second), 0, "Should skip all existing files")

    def test_creates_nested_directories(self):
        scaffold(self.tmpdir)
        expected_dirs = [
            "src/lib",
            "src/app/api/auth/[...all]",
            "src/app/sign-up",
            "src/app/sign-in",
            "src/app/dashboard",
        ]
        for d in expected_dirs:
            full = os.path.join(self.tmpdir, d)
            self.assertTrue(os.path.isdir(full), f"Missing dir: {d}")

    def test_prisma_config_has_define_config(self):
        scaffold(self.tmpdir)
        with open(os.path.join(self.tmpdir, "prisma.config.ts"), "r") as f:
            content = f.read()
        self.assertIn("defineConfig", content)
        self.assertIn('env("DATABASE_URL")', content)

    def test_auth_has_prisma_adapter(self):
        scaffold(self.tmpdir)
        with open(os.path.join(self.tmpdir, "src/lib/auth.ts"), "r") as f:
            content = f.read()
        self.assertIn("prismaAdapter", content)
        self.assertIn("emailAndPassword", content)
        self.assertIn("trustedOrigins", content)

    def test_auth_client_exports(self):
        scaffold(self.tmpdir)
        with open(os.path.join(self.tmpdir, "src/lib/auth-client.ts"), "r") as f:
            content = f.read()
        for export in ["signIn", "signUp", "signOut", "useSession"]:
            self.assertIn(export, content, f"Missing export: {export}")

    def test_route_handler_pattern(self):
        scaffold(self.tmpdir)
        route_path = os.path.join(self.tmpdir, "src/app/api/auth/[...all]/route.ts")
        with open(route_path, "r") as f:
            content = f.read()
        self.assertIn("toNextJsHandler", content)
        self.assertIn("POST", content)
        self.assertIn("GET", content)

    def test_dashboard_has_auth_guard(self):
        scaffold(self.tmpdir)
        with open(os.path.join(self.tmpdir, "src/app/dashboard/page.tsx"), "r") as f:
            content = f.read()
        self.assertIn("useSession", content)
        self.assertIn("useEffect", content)
        self.assertIn("isPending", content)
        self.assertIn("/sign-in", content)

    def test_files_use_lf_line_endings(self):
        scaffold(self.tmpdir)
        for rel_path in FILES:
            full_path = os.path.join(self.tmpdir, rel_path)
            with open(full_path, "rb") as f:
                raw = f.read()
            self.assertNotIn(b"\r\n", raw, f"CRLF found in: {rel_path}")


if __name__ == "__main__":
    unittest.main()
