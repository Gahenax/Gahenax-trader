#!/usr/bin/env python3
"""Public, non-trading health endpoint. Never exposes credentials."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

class Handler(BaseHTTPRequestHandler):
    def _respond(self, body=True):
        path = urlsplit(self.path).path
        if path not in ('/', '/health'):
            self.send_error(404)
            return
        payload = {'service': 'gahenax-trader-testnet', 'mode': 'READ_ONLY', 'orders_enabled': False}
        if path == '/':
            payload['message'] = 'GAHENAX diagnostic service; no trading interface enabled'
        data = json.dumps(payload).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        if body:
            self.wfile.write(data)

    def do_GET(self):
        self._respond()

    def do_HEAD(self):
        self._respond(body=False)

def main():
    HTTPServer(('0.0.0.0', int(os.environ.get('PORT', '10000'))), Handler).serve_forever()

if __name__ == '__main__':
    main()
