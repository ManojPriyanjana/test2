import json
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
import server

class TestServer(unittest.TestCase):
    def setUp(self):
        self.temp_db = Path(tempfile.mkstemp()[1])
        self.temp_db.unlink()  # allow init_db to create the database
        server.DB_PATH = self.temp_db
        self.port = 8765
        self.thread = threading.Thread(target=server.run, kwargs={'port': self.port}, daemon=True)
        self.thread.start()
        time.sleep(0.5)  # wait for server to start

    def tearDown(self):
        if self.temp_db.exists():
            self.temp_db.unlink()

    def test_products_and_checkout(self):
        with urllib.request.urlopen(f'http://localhost:{self.port}/products') as resp:
            products = json.loads(resp.read().decode())
            self.assertTrue(len(products) > 0)
            first = products[0]
        data = json.dumps({'items': [{'id': first['id'], 'quantity': 2}]}).encode()
        req = urllib.request.Request(f'http://localhost:{self.port}/checkout', data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            self.assertAlmostEqual(result['total'], first['price'] * 2)

if __name__ == '__main__':
    unittest.main()
