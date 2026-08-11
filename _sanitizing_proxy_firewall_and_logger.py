# NOTE: This file is a supporting utility, NOT part of the llama-monitor project itself.
# Files beginning with underscore (_) are user-side tools that support project development
# but are not part of the core application codebase.
#
# KNOWN COMMENT ISSUES (audit 9kf.20):
# 1. Line ~21: "Let http.server handle the chunking naturally, avoid double-chunking headers"
#    -> Misleading. The code strips transfer-encoding, which breaks HTTP chunked transfer.
#       The proxy re-buffers the full response instead of streaming it.
# 2. Line ~26: "Read and write in chunks to support SSE (Server-Sent Events) streaming"
#    -> Wrong. By stripping transfer-encoding, SSE streaming doesn't work. The 4096-byte
#       chunks are just internal read buffers, not real HTTP streaming.
# 3. Lines ~57-58: "Llama.cpp leaks its secret media marker in /props. If fed back to itself,
#    it crashes. Scrub it completely from the payload before llama.cpp ever sees it."
#    -> Dramatic overstatement. The <__media_...__> marker is a special internal token that
#       can cause issues if echoed back. Scrubbing is reasonable, but calling it a "secret
#       media marker" and "crash fix" is misleading.
# These issues are documented but not fixed, as the file may not be in active use.

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

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def _forward_and_stream(self, req):
        """Helper to forward the request and stream the response back chunk-by-chunk"""
        try:
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for k, v in response.headers.items():
                    # Let http.server handle the chunking naturally, avoid double-chunking headers
                    if k.lower() not in ['transfer-encoding']:
                        self.send_header(k, v)
                self.end_headers()
                
                # Read and write in chunks to support SSE (Server-Sent Events) streaming
                while True:
                    chunk = response.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
                    
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ['transfer-encoding']:
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            print(f"Error connecting to llama.cpp: {e}")
            self.send_error(502, "Bad Gateway")

    def do_GET(self):
        # Forward GET requests (like /slots, /metrics, /props) transparently
        headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host']}
        req = urllib.request.Request(LLAMA_URL + self.path, headers=headers, method="GET")
        self._forward_and_stream(req)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        # --- SANITIZER CRASH FIX ---
        body_str = body.decode('utf-8', errors='replace')
        # Llama.cpp leaks its secret media marker in /props. If fed back to itself, it crashes.
        # Scrub it completely from the payload before llama.cpp ever sees it.
        body_str = re.sub(r'<__media_[a-zA-Z0-9]+__>', '[MEDIA_MARKER_SCRUBBED]', body_str)
        body = body_str.encode('utf-8')
        # ---------------------------

        # 1. Log the exact JSON request to a file (if enabled)
        if "/v1/chat/completions" in self.path:
            if ENABLE_LOGGING:
                with open("crash_log.txt", "a", encoding="utf-8") as f:
                    f.write("\n" + "="*50 + "\n")
                    f.write(f"ENDPOINT: {self.path}\n")
                    try:
                        # Pretty-print the JSON if possible
                        parsed_json = json.loads(body)
                        f.write(json.dumps(parsed_json, indent=2))
                    except Exception:
                        # Fallback to raw text
                        f.write(body.decode('utf-8', errors='replace'))
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
with ThreadedTCPServer(("", LISTEN_PORT), ProxyHTTPRequestHandler) as httpd:
    print(f"Multi-Threaded Proxy Logger is running on port {LISTEN_PORT}...")
    print(f"Point OpenCode to http://127.0.0.1:{LISTEN_PORT}")
    print(f"Make sure llama.cpp is running on {LLAMA_URL}")
    httpd.serve_forever()