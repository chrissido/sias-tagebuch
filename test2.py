#!/usr/bin/env python3
"""Test-Server mit anderem Port"""
import http.server, json, socketserver

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True}).encode())
    def log_message(self, format, *args):
        pass

PORT = 9999
with socketserver.ThreadingTCPServer(('', PORT), Handler) as s:
    s.allow_reuse_address = True
    print(f"Server auf Port {PORT}")
    s.serve_forever()
