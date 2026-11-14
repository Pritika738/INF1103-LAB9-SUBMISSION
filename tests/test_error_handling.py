
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO

from main import get_positive_float, load_products
from inventory import Inventory
from supplier import Supplier


class TestErrorHandling(unittest.TestCase):

    def test_invalid_user_input(self):
        output = StringIO()

        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with redirect_stdout(output):
                result = get_positive_float("Enter price: ")

        self.assertEqual(result, 12.5)
        self.assertIn("Please enter a valid number", output.getvalue())
        self.assertIn("Please enter a number greater than zero", output.getvalue())

    def test_missing_file(self):
        import tempfile
        from pathlib import Path

        inventory = Inventory()
        supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
        output = StringIO()

        with tempfile.TemporaryDirectory() as folder:
            missing_path = str(Path(folder) / "products.csv")

            with redirect_stdout(output):
                load_products(missing_path, inventory, supplier)

        self.assertIn("Products file not found:", output.getvalue())
        self.assertIn("Load attempt finished.", output.getvalue())

    def test_invalid_csv_rows(self):
        inventory = Inventory()
        supplier = Supplier("S001", "ABC Supplies", "abc@example.com")
        output = StringIO()

        with redirect_stdout(output):
            load_products("products.csv", inventory, supplier)

        self.assertEqual(len(inventory.get_all_products()), 3)
        self.assertIn("Skipped row 4", output.getvalue())
        self.assertIn("Skipped row 5", output.getvalue())
        self.assertIn("3 products loaded.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
