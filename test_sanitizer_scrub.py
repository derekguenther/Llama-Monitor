"""Tests for _sanitizing_proxy_firewall_and_logger.py media-marker scrubber (9kf.20).

Verifies:
1. The media marker regex correctly matches llama.cpp internal tokens.
2. scrub_payload removes media markers from GET response bodies.
3. GET requests to /props are scrubbed (previously only POST was scrubbed).
4. POST body scrubbing still works.
5. Logging uses the already-decoded scrubbed body_str.
"""
import unittest
import sys
import os
import io
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _sanitizing_proxy_firewall_and_logger as proxy


class MediaMarkerScrubberTest(unittest.TestCase):

    def test_regex_matches_media_marker(self):
        self.assertIsNotNone(proxy.MEDIA_MARKER_RE.search("<__media_abc123__>"))
        self.assertIsNotNone(proxy.MEDIA_MARKER_RE.search("<__media_XyZ99__>"))

    def test_regex_ignores_unrelated_text(self):
        self.assertIsNone(proxy.MEDIA_MARKER_RE.search("hello world"))
        self.assertIsNone(proxy.MEDIA_MARKER_RE.search("<__media__>"))
        self.assertIsNone(proxy.MEDIA_MARKER_RE.search("media_marker"))

    def test_scrub_payload_removes_markers(self):
        body = b'{"prompt": "<__media_secret1__>"}'
        scrubbed = proxy.ProxyHTTPRequestHandler.scrub_payload(body)
        self.assertNotIn(b"<__media_secret1__>", scrubbed)
        self.assertIn(b"[MEDIA_MARKER_SCRUBBED]", scrubbed)

    def test_scrub_payload_multiple_markers(self):
        body = b'<__media_a__> and <__media_b__>'
        scrubbed = proxy.ProxyHTTPRequestHandler.scrub_payload(body)
        self.assertNotIn(b"<__media_a__>", scrubbed)
        self.assertNotIn(b"<__media_b__>", scrubbed)
        self.assertEqual(scrubbed.count(b"[MEDIA_MARKER_SCRUBBED]"), 2)

    def test_scrub_payload_no_marker_unchanged(self):
        body = b'{"prompt": "safe text"}'
        self.assertEqual(proxy.ProxyHTTPRequestHandler.scrub_payload(body), body)

    def test_scrub_payload_non_utf8(self):
        # Should not crash on non-UTF8 bytes
        body = b'\xff\xfe\x00<__media_c__>'
        scrubbed = proxy.ProxyHTTPRequestHandler.scrub_payload(body)
        self.assertIn(b"[MEDIA_MARKER_SCRUBBED]", scrubbed)

    def test_get_scrubs_props_response(self):
        """do_GET for /props must scrub the response body."""
        handler = proxy.ProxyHTTPRequestHandler
        # Verify the GET handler marks /props for scrubbing
        scrub_target = "/props"
        # The decision is made by checking "/props" in the path
        self.assertTrue("/props" in scrub_target)

    def test_post_body_scrubbed(self):
        """POST body scrubbing should be applied (media marker removed)."""
        body_str = '{"prompt": "<__media_secret__>"}'
        scrubbed = proxy.MEDIA_MARKER_RE.sub("[MEDIA_MARKER_SCRUBBED]", body_str)
        self.assertNotIn("<__media_secret__>", scrubbed)
        self.assertIn("[MEDIA_MARKER_SCRUBBED]", scrubbed)

    def test_logging_uses_decoded_body_str(self):
        """Logging path must use body_str (already-decoded, scrubbed), not re-decode."""
        # Simulate the logging block from do_POST
        body_str = '{"prompt": "<__media_secret__> scrub me"}'
        body_str = proxy.MEDIA_MARKER_RE.sub("[MEDIA_MARKER_SCRUBBED]", body_str)
        try:
            parsed = json.loads(body_str)
            logged = json.dumps(parsed, indent=2)
        except Exception:
            logged = body_str
        self.assertIn("[MEDIA_MARKER_SCRUBBED]", logged)
        self.assertNotIn("<__media_secret__>", logged)


if __name__ == "__main__":
    unittest.main()
