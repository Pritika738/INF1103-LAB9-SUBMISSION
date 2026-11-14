
import unittest

from product_factory import ProductFactory
from order_line import OrderLine
from supplier import Supplier


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "S001", "ABC Supplies", "abc@example.com"
        )

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "digital", "D001", "Software",
                -10.0, 10, self.supplier
            )

    def test_negative_stock(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "digital", "D001", "Software",
                50.0, -5, self.supplier
            )

    def test_invalid_order_quantity(self):
        product = ProductFactory.create(
            "digital", "D001", "Software",
            50.0, 10, self.supplier
        )

        with self.assertRaises(ValueError):
            OrderLine(product, 0)

    def test_invalid_stock_update(self):
        product = ProductFactory.create(
            "digital", "D001", "Software",
            50.0, 10, self.supplier
        )

        with self.assertRaises(ValueError):
            product.update_stock(-5)


if __name__ == "__main__":
    unittest.main()
