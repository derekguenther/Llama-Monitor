#!/usr/bin/env python3
"""Unit tests for web_server settings endpoints."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Set up environment before importing web_server
os.environ['FLASK_ENV'] = 'testing'

from web_server import app, api_get_settings, api_set_settings, api_set_cost_rate, api_reset_settings, get_db, DB_AVAILABLE


class TestSettingsEndpoints(unittest.TestCase):
    """Tests for settings API endpoints."""

    def setUp(self):
        """Create test client and temp database."""
        self.app = app.test_client()
        self.app.testing = True

        # Create temp database
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()

        # Patch get_db to use temp database
        self.patcher = patch('web_server.get_db')
        self.mock_get_db = self.patcher.start()

        from db import Database
        self.db = Database(self.temp_db.name)
        self.mock_get_db.return_value = self.db

    def tearDown(self):
        """Clean up."""
        self.patcher.stop()
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_api_get_settings_returns_default_values(self):
        """Test GET /api/settings returns default values when no settings exist."""
        with self.app:
            response = self.app.get('/api/settings')
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertIn('web_refresh_rate', data)
            self.assertIn('show_cost', data)
            self.assertIn('show_temps', data)
            self.assertIn('cost_rate', data)

            # Check default values
            self.assertEqual(data['web_refresh_rate'], 1)
            self.assertEqual(data['show_cost'], True)
            self.assertEqual(data['show_temps'], True)
            self.assertEqual(data['cost_rate'], 0.12)

    def test_api_get_settings_returns_stored_values(self):
        """Test GET /api/settings returns stored values."""
        with self.db:
            self.db.set_setting('web_refresh_rate', '5')
            self.db.set_setting('show_cost', 'false')
            self.db.set_setting('show_temps', 'true')
            self.db.set_setting('cost_rate_usd_per_kwh', '0.25')

        with self.app:
            response = self.app.get('/api/settings')
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertEqual(data['web_refresh_rate'], 5)
            self.assertEqual(data['show_cost'], False)
            self.assertEqual(data['show_temps'], True)
            self.assertEqual(data['cost_rate'], 0.25)

    def test_api_set_settings_updates_values(self):
        """Test POST /api/settings updates settings."""
        payload = {
            'web_refresh_rate': 10,
            'show_cost': False,
            'show_temps': True,
            'cost_rate': 0.30
        }

        with self.app:
            response = self.app.post(
                '/api/settings',
                json=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertTrue(data['success'])

        # Verify values were stored
        with self.db:
            self.assertEqual(self.db.get_setting('web_refresh_rate'), '10')
            self.assertEqual(self.db.get_setting('show_cost'), 'false')
            self.assertEqual(self.db.get_setting('show_temps'), 'true')
            # Note: 0.30 becomes '0.3' due to string conversion
            self.assertEqual(self.db.get_setting('cost_rate_usd_per_kwh'), '0.3')

    def test_api_set_cost_rate_updates_value(self):
        """Test POST /api/settings/cost_rate updates cost rate."""
        payload = {'cost_rate': 0.28}

        with self.app:
            response = self.app.post(
                '/api/settings/cost_rate',
                json=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(data['message'], 'Cost rate updated')

        # Verify value was stored
        with self.db:
            rate = self.db.get_cost_rate()
            self.assertEqual(rate, 0.28)

    def test_api_set_cost_rate_validates_negative(self):
        """Test POST /api/settings/cost_rate rejects negative values."""
        payload = {'cost_rate': -1.0}

        with self.app:
            response = self.app.post(
                '/api/settings/cost_rate',
                json=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

            data = response.get_json()
            self.assertIn('error', data)
            self.assertIn('non-negative', data['error'])

    def test_api_set_cost_rate_validates_missing(self):
        """Test POST /api/settings/cost_rate rejects missing cost_rate."""
        payload = {'other_field': 'value'}

        with self.app:
            response = self.app.post(
                '/api/settings/cost_rate',
                json=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

            data = response.get_json()
            self.assertIn('error', data)
            self.assertIn('cost_rate', data['error'])

    def test_api_set_cost_rate_validates_invalid(self):
        """Test POST /api/settings/cost_rate rejects invalid values."""
        payload = {'cost_rate': 'not_a_number'}

        with self.app:
            response = self.app.post(
                '/api/settings/cost_rate',
                json=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

            data = response.get_json()
            self.assertIn('error', data)
            self.assertIn('Invalid', data['error'])

    def test_api_reset_settings_clears_all(self):
        """Test POST /api/settings/reset clears all settings."""
        # Set some values
        with self.db:
            self.db.set_setting('web_refresh_rate', '999')
            self.db.set_setting('show_cost', 'false')
            self.db.set_setting('custom_setting', 'custom_value')

        with self.app:
            response = self.app.post('/api/settings/reset')
            self.assertEqual(response.status_code, 200)

            data = response.get_json()
            self.assertTrue(data['success'])

        # Verify all settings are reset to defaults
        with self.app:
            response = self.app.get('/api/settings')
            data = response.get_json()

            self.assertEqual(data['web_refresh_rate'], 1)
            self.assertEqual(data['show_cost'], True)
            self.assertEqual(data['cost_rate'], 0.12)


if __name__ == '__main__':
    unittest.main()
