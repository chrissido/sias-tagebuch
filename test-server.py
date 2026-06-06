#!/usr/bin/env python3
"""Einfacher Test-Server"""
import http.server
import json

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'path': self.path}).encode())
    def log_message(self, format, *args):
        print(f"[TEST] {args[0]}" if args else "")

if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', 8899), Handler)
    print("Test-Server läuft auf Port 8899")
    server.serve_forever()
