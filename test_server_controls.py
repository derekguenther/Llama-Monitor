#!/usr/bin/env python3
"""Tests for the Server Control UI (Restart / Stop buttons + confirmation modal).

Validates that the dashboard template renders the restart/stop controls and
that the confirmation modal requires an explicit typed confirmation word before
the destructive action can be executed (safety requirement: never allow a
shutdown without the user being VERY sure).
"""

import unittest


class TestServerControlButtons(unittest.TestCase):
    """Tests that the template renders the server control buttons."""

    def setUp(self):
        from web_server import app
        with app.test_client() as client:
            self.html = client.get("/").get_data(as_text=True)

    def test_html_has_restart_button(self):
        self.assertIn('id="restart-server-btn"', self.html)

    def test_html_has_stop_button(self):
        self.assertIn('id="stop-server-btn"', self.html)

    def test_html_has_confirmation_modal(self):
        self.assertIn('id="server-control-modal"', self.html)

    def test_html_has_confirmation_input(self):
        self.assertIn('id="server-control-confirm-input"', self.html)

    def test_confirm_button_starts_disabled(self):
        # The confirm button must be disabled by default (requires typed word)
        self.assertIn('id="confirm-server-control-btn"', self.html)
        self.assertIn("disabled", self.html.split('id="confirm-server-control-btn"')[1].split(">")[0])


class TestServerControlSafety(unittest.TestCase):
    """Tests the safety-critical confirmation logic in the JS."""

    def setUp(self):
        from web_server import app
        with app.test_client() as client:
            self.html = client.get("/").get_data(as_text=True)

    def test_stop_warning_is_prominent(self):
        # The stop action must carry a clear, prominent warning
        self.assertIn("STOP SERVER", self.html)
        self.assertIn("server-control-warning", self.html)
        self.assertIn("server-control-warning-text", self.html)

    def test_confirmation_requires_typed_word(self):
        # The confirm button must be enabled only when the typed word matches
        self.assertIn("SERVER_ACTION_CONFIRM_WORDS", self.html)
        self.assertIn("serverControlConfirmBtn.disabled = (typed !== requiredWord);", self.html)

    def test_confirm_word_is_explicit(self):
        # The stop confirmation word must be explicit (STOP), not a vague 'OK'
        self.assertIn("stop: 'STOP'", self.html)

    def test_js_wires_stop_to_endpoint(self):
        # JS must call /api/server/stop for the stop action
        self.assertIn("'/api/server/stop'", self.html)

    def test_js_wires_restart_to_endpoint(self):
        # JS must call /api/server/restart for the restart action
        self.assertIn("'/api/server/restart'", self.html)

    def test_confirm_button_rechecks_typed_word(self):
        # The confirm handler must re-verify the typed word before firing
        self.assertIn("typed !== confirmWord", self.html)


if __name__ == "__main__":
    unittest.main()
