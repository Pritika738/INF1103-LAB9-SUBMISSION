
import unittest

from discount import (
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount
)
from order import Order
from product import DigitalProduct
from supplier import Supplier


class TestStrategy(unittest.TestCase):

    def test_discounts(self):
        self.assertEqual(NoDiscount().apply(250), 250)
        self.assertEqual(PercentageDiscount(10).apply(250), 225)
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(StudentDiscount().apply(250), 237.5)

    def test_order_discount_change(self):
        supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
        product = DigitalProduct(
            "D001", "Software", 50.0, 10, 100.0, supplier
        )

        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(product, 5)

        self.assertEqual(order.calculate_total(), 230)

        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)

    def test_default_discount(self):
        order = Order("O002")
        self.assertEqual(order.calculate_total(), 0)


if __name__ == "__main__":
    unittest.main()
