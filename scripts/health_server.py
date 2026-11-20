#!/usr/bin/env python3
"""Minimal non-trading health endpoint. Never exposes credentials."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/health':
            self.send_error(404)
            return
        data = json.dumps({'service':'gahenax-trader-testnet','mode':'READ_ONLY','orders_enabled':False}).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)

HTTPServer(('0.0.0.0', int(os.environ.get('PORT','10000'))), Handler).serve_forever()
