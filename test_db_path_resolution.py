#!/usr/bin/env python3
"""Unit tests for per-worktree database path resolution (bead o2hs).

Verifies that Monitor resolves the SQLite database path correctly:
- default behavior resolves the configured relative path against the script dir;
- an explicit db_path (--db-path / LLAMA_MONITOR_DB) overrides the config and
  resolves relative to the current working directory;
- the resolved absolute path is published back into the shared config so the
  web server reads the same database file.
"""

import os
import sys
import tempfile
import unittest

import llamamonitor
from config import reload_config


class TestDbPathResolution(unittest.TestCase):
    """Tests for database path resolution in Monitor.initialize()."""

    def setUp(self):
        """Create a Monitor pointing at a temp config with no explicit db_path."""
        fd, self.config_path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        self.tmpdir = tempfile.mkdtemp(prefix="o2hs-db-")
        self.addCleanup(lambda: _rm(self.config_path))
        self.addCleanup(lambda: _rmtree(self.tmpdir))
        # Reset the global config singleton so state does not leak between tests.
        reload_config(self.config_path)

    def _make_monitor(self, db_path=None):
        return llamamonitor.Monitor(
            server_url="http://localhost:8000",
            config_path=self.config_path,
            enable_web=False,
            enable_tui=False,
            db_path=db_path,
        )

    def test_default_resolves_relative_config_to_script_dir(self):
        """With no override, a relative config path resolves against the script dir."""
        monitor = self._make_monitor()
        monitor.initialize()
        try:
            expected = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "llama-monitor.db"
            )
            self.assertEqual(monitor.db.db_path, expected)
            self.assertEqual(monitor.config.get("database.path"), expected)
        finally:
            monitor.db.close()

    def test_absolute_db_path_override(self):
        """An absolute db_path override is used verbatim."""
        target = os.path.join(self.tmpdir, "abs.db")
        monitor = self._make_monitor(db_path=target)
        monitor.initialize()
        try:
            self.assertEqual(monitor.db.db_path, target)
            self.assertEqual(monitor.config.get("database.path"), target)
            self.assertTrue(os.path.exists(target))
        finally:
            monitor.db.close()

    def test_relative_db_path_override_resolves_to_cwd(self):
        """A relative db_path override resolves against the current working directory."""
        relative = os.path.join("relative", "llama-monitor.db")
        monitor = self._make_monitor(db_path=relative)
        monitor.initialize()
        try:
            expected = os.path.abspath(relative)
            self.assertEqual(monitor.db.db_path, expected)
        finally:
            monitor.db.close()

    def test_db_path_published_to_shared_config(self):
        """The resolved path is written to config so web_server reads the same DB."""
        target = os.path.join(self.tmpdir, "shared.db")
        monitor = self._make_monitor(db_path=target)
        monitor.initialize()
        try:
            # The web server reads database.path from the same global config object.
            self.assertEqual(
                monitor.config.get("database.path"), target,
                "web server must read the identical resolved path",
            )
        finally:
            monitor.db.close()

    def test_cli_arg_present(self):
        """parse_args exposes --db-path."""
        old_argv = sys.argv
        sys.argv = ["llamamonitor.py", "--db-path", "/tmp/x.db"]
        try:
            args = llamamonitor.parse_args()
            self.assertEqual(args.db_path, "/tmp/x.db")
        finally:
            sys.argv = old_argv


def _rm(p):
    try:
        os.unlink(p)
    except OSError:
        pass


def _rmtree(p):
    import shutil
    shutil.rmtree(p, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
