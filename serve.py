#!/usr/bin/env python3
"""Static file server for local development that defeats browser caching.

The stock `python3 -m http.server` sends Last-Modified but no Cache-Control, so
browsers fall back to heuristic freshness and a normal refresh can quietly reuse
a stale stylesheet — which makes edits look like they never applied. This sends
explicit no-store headers so every reload fetches the real file.

Usage: python3 serve.py [port]
"""

import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        # Keep the log to one terse line per request.
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4321
    print(f"serving {sys.path[0] or '.'} on http://localhost:{port} (no-cache)")
    ThreadingHTTPServer(("", port), NoCacheHandler).serve_forever()
