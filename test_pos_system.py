import unittest
from pos_system import PointOfSale


class TestPOS(unittest.TestCase):
    def test_checkout_total(self):
        pos = PointOfSale()
        pos.add_product_to_inventory('001', 'Apple', 0.5, 10)
        pos.scan('001', 2)
        total = pos.checkout()
        self.assertEqual(total, 1.0)


if __name__ == '__main__':
    unittest.main()
