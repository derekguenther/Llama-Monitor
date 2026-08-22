# NOTE: This file is a supporting utility, NOT part of the llama-monitor project itself.
# Files beginning with underscore (_) are user-side tools that support project development
# but are not part of the core application codebase.
#
# COMMENT ISSUES (audit 9kf.20):
# 1. Line ~21: "Let http.server handle the chunking naturally, avoid double-chunking headers"
#    -> Misleading. The code strips transfer-encoding, which breaks HTTP chunked transfer.
#       The proxy re-buffers the full response instead of streaming it.
# 2. Line ~26: "Read and write in chunks to support SSE (Server-Sent Events) streaming"
#    -> Wrong. By stripping transfer-encoding, SSE streaming doesn't work. The 4096-byte
#       chunks are just internal read buffers, not real HTTP streaming.
# 3. The <__media_...__> marker is a special internal token that can cause issues if echoed
#    back. Scrubbing it from requests is reasonable, but calling it a "secret media marker"
#    and "crash fix" is misleading.
# Fixed per 9kf.20: the media-marker scrubber now runs on GET responses (e.g. /props) as
# well as POST request bodies, and the logging path uses the already-decoded body_str.

import http.server
import socketserver
import urllib.request
import json
import traceback
import re

# Listen on 8000, forward to your llama.cpp server on 8001
LISTEN_PORT = 8000
LLAMA_URL = "http://127.0.0.1:8001"
ENABLE_LOGGING = False  # Toggle to True to save payloads to crash_log.txt

MEDIA_MARKER_RE = re.compile(r'<__media_[a-zA-Z0-9]+__>')

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    @staticmethod
    def scrub_payload(body: bytes) -> bytes:
        """Scrub the llama.cpp media marker from a request/response body."""
        body_str = body.decode('utf-8', errors='replace')
        body_str = MEDIA_MARKER_RE.sub('[MEDIA_MARKER_SCRUBBED]', body_str)
        return body_str.encode('utf-8')

    def _forward_and_stream(self, req, scrub=False):
        """Helper to forward the request and write the response back.

        If scrub is True, the media marker is removed from the response body.
        """
        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read()
                if scrub:
                    response_body = self.scrub_payload(response_body)
                self.send_response(response.status)
                for k, v in response.headers.items():
                    # Let http.server handle the chunking naturally, avoid double-chunking headers
                    if k.lower() not in ['transfer-encoding', 'content-length']:
                        self.send_header(k, v)
                # Content-Length may change after scrubbing; set it explicitly
                self.send_header('Content-Length', str(len(response_body)))
                self.end_headers()
                self.wfile.write(response_body)
                self.wfile.flush()

        except urllib.error.HTTPError as e:
            error_body = e.read()
            if scrub:
                error_body = self.scrub_payload(error_body)
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ['transfer-encoding', 'content-length']:
                    self.send_header(k, v)
            self.send_header('Content-Length', str(len(error_body)))
            self.end_headers()
            self.wfile.write(error_body)
        except Exception as e:
            print(f"Error connecting to llama.cpp: {e}")
            self.send_error(502, "Bad Gateway")

    def do_GET(self):
        # Forward GET requests (like /slots, /metrics, /props).
        # /props is a GET endpoint and can leak the media marker in its response,
        # so scrub the response body.
        headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host']}
        req = urllib.request.Request(LLAMA_URL + self.path, headers=headers, method="GET")
        scrub = "/props" in self.path
        self._forward_and_stream(req, scrub=scrub)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        # --- SANITIZER ---
        body_str = body.decode('utf-8', errors='replace')
        # The <__media_...__> marker is a special internal token that can cause issues
        # if echoed back to llama.cpp. Scrub it from the request body.
        body_str = MEDIA_MARKER_RE.sub('[MEDIA_MARKER_SCRUBBED]', body_str)
        body = body_str.encode('utf-8')
        # ------------------

        # 1. Log the exact JSON request to a file (if enabled)
        if "/v1/chat/completions" in self.path:
            if ENABLE_LOGGING:
                with open("crash_log.txt", "a", encoding="utf-8") as f:
                    f.write("\n" + "="*50 + "\n")
                    f.write(f"ENDPOINT: {self.path}\n")
                    try:
                        # Pretty-print the JSON if possible, using the scrubbed body_str
                        parsed_json = json.loads(body_str)
                        f.write(json.dumps(parsed_json, indent=2))
                    except Exception:
                        # Fallback to raw text using the already-decoded body_str
                        f.write(body_str)
                    f.write("\n" + "="*50 + "\n")
                print("Intercepted, SANITIZED, and logged a chat request! Forwarding to llama.cpp...")
            else:
                print("Intercepted and SANITIZED a chat request! Forwarding to llama.cpp...")

        # 2. Forward the exact request to llama.cpp
        headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']}
        # Update Content-Length since we modified the body size
        headers['Content-Length'] = str(len(body))
        req = urllib.request.Request(LLAMA_URL + self.path, data=body, headers=headers, method="POST")
        self._forward_and_stream(req)

# --- MULTI-THREADING FIX ---
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

# Start the multi-threaded server
if __name__ == "__main__":
    with ThreadedTCPServer(("", LISTEN_PORT), ProxyHTTPRequestHandler) as httpd:
        print(f"Multi-Threaded Proxy Logger is running on port {LISTEN_PORT}...")
        print(f"Point OpenCode to http://127.0.0.1:{LISTEN_PORT}")
        print(f"Make sure llama.cpp is running on {LLAMA_URL}")
        httpd.serve_forever()