import json
import sqlite3
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, HTTPServer

DB_PATH = Path(__file__).with_name('pos.db')
SCHEMA = Path(__file__).with_name('schema.sql')

def init_db():
    first_time = not DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    if first_time:
        with open(SCHEMA) as f:
            conn.executescript(f.read())
    conn.close()

class POSHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/products':
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            rows = conn.execute('SELECT id, name, price FROM products').fetchall()
            conn.close()
            data = [dict(r) for r in rows]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/checkout':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body or '{}')
            items = data.get('items', [])
            conn = sqlite3.connect(DB_PATH)
            total = 0.0
            for item in items:
                pid = item['id']
                qty = item.get('quantity', 1)
                row = conn.execute('SELECT price FROM products WHERE id=?', (pid,)).fetchone()
                if row:
                    total += row[0] * qty
            conn.close()
            resp = json.dumps({'total': total}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()

def run(port=8000):
    init_db()
    server_address = ('', port)
    httpd = HTTPServer(server_address, POSHandler)
    print(f'Serving on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
