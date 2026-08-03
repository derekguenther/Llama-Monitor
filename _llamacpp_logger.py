import http.server
import socketserver
import urllib.request
import json
import time
import sys

LISTEN_PORT = 8000
LLAMA_URL = "http://127.0.0.1:8001"
ENABLE_LOGGING = True
LOG_FILE = "_llamacpp_logger.log"

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def _log(self, text):
        if ENABLE_LOGGING:
            try:
                # Open with buffering=0 (binary) or force flush immediately so no bytes are cached in RAM
                with open(LOG_FILE, "a", encoding="utf-8", errors="replace") as f:
                    f.write(text)
                    f.flush()
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to write to log file: {e}", file=sys.stderr)

    def _forward_and_stream(self, req):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self._log(f"\n<<< [RESPONSE START - {timestamp}] {req.method} {req.full_url}\n")
        
        try:
            with urllib.request.urlopen(req) as response:
                self.send_response(response.status)
                for k, v in response.headers.items():
                    if k.lower() not in ['transfer-encoding']:
                        self.send_header(k, v)
                self.end_headers()
                
                while True:
                    try:
                        chunk = response.read(4096)
                        if not chunk:
                            break
                        
                        # 1. ALWAYS log the chunk immediately before writing to socket
                        if ENABLE_LOGGING:
                            chunk_str = chunk.decode('utf-8', errors='replace')
                            self._log(chunk_str)

                        # 2. Forward to OpenCode client socket
                        self.wfile.write(chunk)
                        self.wfile.flush()

                    except (BrokenPipeError, ConnectionResetError):
                        # OpenCode closed the connection (common when it detects tool calls and cuts the stream)
                        self._log("\n<<< [CLIENT DISCONNECTED EARLY - STREAM ABORTED BY OPENCODE]\n")
                        break

                self._log("\n<<< [RESPONSE END]\n")

        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for k, v in e.headers.items():
                if k.lower() not in ['transfer-encoding']:
                    self.send_header(k, v)
            self.end_headers()
            err_body = e.read()
            self._log(f"HTTP ERROR {e.code}: {err_body.decode('utf-8', errors='replace')}\n")
            self.wfile.write(err_body)
            
        except Exception as e:
            print(f"Error connecting to llama.cpp: {e}", file=sys.stderr)
            self._log(f"\nGATEWAY / STREAM EXCEPTION: {e}\n")
            try:
                self.send_error(502, "Bad Gateway")
            except Exception:
                pass

    def do_GET(self):
        headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host']}
        req = urllib.request.Request(LLAMA_URL + self.path, headers=headers, method="GET")
        self._forward_and_stream(req)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self._log(f"\n{'='*60}\n>>> [REQUEST START - {timestamp}] {self.path}\n")
        try:
            parsed_json = json.loads(body.decode('utf-8'))
            self._log(json.dumps(parsed_json, indent=2))
        except Exception:
            self._log(body.decode('utf-8', errors='replace'))
        self._log(f"\n>>> [REQUEST END]\n")

        print(f"[{timestamp}] Intercepted POST {self.path} -> Forwarding")

        headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']}
        headers['Content-Length'] = str(len(body))
        req = urllib.request.Request(LLAMA_URL + self.path, data=body, headers=headers, method="POST")
        self._forward_and_stream(req)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

if __name__ == "__main__":
    # Clear old log or append cleanly
    print(f"Passthrough Logger Proxy running on port {LISTEN_PORT}...")
    print(f"Targeting llama.cpp on {LLAMA_URL}")
    print(f"Logging with explicit unbuffered flushes to '{LOG_FILE}'")
    
    with ThreadedTCPServer(("", LISTEN_PORT), ProxyHTTPRequestHandler) as httpd:
        httpd.serve_forever()