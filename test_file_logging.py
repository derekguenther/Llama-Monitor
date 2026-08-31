#!/usr/bin/env python3
"""Tests for the optional file logging feature (bead llama-monitor-5kiw)."""

import logging
import os
import tempfile
import unittest


class TestFileLogging(unittest.TestCase):
    """Tests that Monitor adds a rotating file handler to the root logger."""

    def setUp(self):
        # Remove any pre-existing handlers on the root logger so assertions
        # about our own handler are clean.
        self._saved_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers = []
        self._tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        logging.getLogger().handlers = self._saved_handlers
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def _monitor(self, log_file):
        """Create a Monitor instance pointing at a temp config with a log file."""
        from llamamonitor import Monitor
        return Monitor(
            config_path=os.path.join(self._tmpdir, "does-not-exist.yaml"),
            enable_web=False,
            enable_tui=False,
            log_file=log_file,
        )

    def test_file_handler_added_to_root_logger(self):
        """A RotatingFileHandler is attached to the root logger when log_file is set."""
        log_path = os.path.join(self._tmpdir, "monitor.log")
        self._monitor(log_path)

        handlers = logging.getLogger().handlers
        file_handlers = [h for h in handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(file_handlers), 1)
        self.assertEqual(file_handlers[0].baseFilename, os.path.abspath(log_path))

    def test_no_file_handler_when_log_file_not_set(self):
        """No RotatingFileHandler is added when log_file is None."""
        self._monitor(None)
        handlers = logging.getLogger().handlers
        file_handlers = [h for h in handlers if isinstance(h, logging.handlers.RotatingFileHandler)]
        self.assertEqual(len(file_handlers), 0)

    def test_warning_written_to_file(self):
        """A warning emitted through the root logger appears in the log file."""
        log_path = os.path.join(self._tmpdir, "monitor.log")
        self._monitor(log_path)

        # Emit a warning through a module-level logger (like the CPU clamp warning).
        logger = logging.getLogger("aggregator")
        logger.setLevel(logging.WARNING)
        logger.warning("CPU usage clamped to 100%")

        # Flush handlers and read the file.
        for handler in logging.getLogger().handlers:
            handler.flush()

        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CPU usage clamped to 100%", content)


if __name__ == "__main__":
    unittest.main()
