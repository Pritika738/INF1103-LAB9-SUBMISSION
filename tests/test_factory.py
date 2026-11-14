
import unittest

from product_factory import ProductFactory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier


class TestFactory(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier(
            "S001", "ABC Supplies", "abc@example.com"
        )

    def test_physical_product(self):
        product = ProductFactory.create(
            "physical", "P001", "Laptop",
            1200.0, 10, self.supplier, weight=2.5
        )
        self.assertIsInstance(product, PhysicalProduct)

    def test_digital_product(self):
        product = ProductFactory.create(
            "digital", "D001", "Software",
            50.0, 100, self.supplier, download_size=500.0
        )
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_product_type(self):
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service", "S001", "Installation",
                30.0, 5, self.supplier
            )


if __name__ == "__main__":
    unittest.main()
