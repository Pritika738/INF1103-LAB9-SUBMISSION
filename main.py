import csv
import json
from pathlib import Path

from product import PhysicalProduct, DigitalProduct
from product_factory import ProductFactory
from inventory import Inventory
from supplier import Supplier


FILE_PATH = Path(__file__).with_name("inventory.json")


def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")

    except FileNotFoundError:
        print(f"Products file not found: {path}")

    else:
        loaded = 0

        with file:
            reader = csv.reader(file)
            next(reader, None)

            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row

                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        name,
                        float(price),
                        int(stock),
                        supplier
                    )

                    inventory.add_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Skipped row {row_number}: {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")


def create_product(item, supplier):
    product_type = item.get("type")

    # Handle products saved in the old Lab 6 format
    if product_type is None:
        print("\nOld product found:", item["name"])
        print("1. Physical product")
        print("2. Digital product")

        while True:
            choice = input("Choose product type (1-2): ")
            if choice in ("1", "2"):
                break
            print("Please enter 1 or 2.")

        product_type = "physical" if choice == "1" else "digital"

    product_id = item["product_id"]
    name = item["name"]
    price = float(item["price"])
    stock = int(item["stock"])

    if product_type == "physical":
        if "weight" in item:
            weight = float(item["weight"])
        else:
            weight = float(input("Enter weight (kg): "))

        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        return ProductFactory.create(
            "physical", product_id, name, price, stock,
            supplier, weight=weight
        )

    elif product_type == "digital":
        if "download_size" in item:
            download_size = float(item["download_size"])
        else:
            download_size = float(input("Enter download size (MB): "))

        if download_size < 0:
            raise ValueError("Download size cannot be negative.")

        return ProductFactory.create(
            "digital", product_id, name, price, stock,
            supplier, download_size=download_size
        )

    else:
        raise ValueError("Unknown product type.")


def load_inventory(inventory, supplier):
    if not FILE_PATH.exists():
        return True

    try:
        with open(FILE_PATH, "r") as file:
            products = json.load(file)

        # Create all objects before adding them to inventory
        loaded_products = []

        for item in products:
            product = create_product(item, supplier)
            loaded_products.append(product)

        for product in loaded_products:
            inventory.add_product(product)

        print("Inventory loaded successfully!")
        return True

    except (OSError, ValueError, KeyError, TypeError) as error:
        print("Could not load inventory.json:", error)
        print("Existing inventory file has not been overwritten.")
        return False


def save_inventory(inventory):
    products = []

    for product in inventory.get_all_products():
        item = product.to_dict()

        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.weight

        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.download_size

        products.append(item)

    try:
        with open(FILE_PATH, "w") as file:
            json.dump(products, file, indent=4)

        print("Inventory saved successfully!")

    except OSError:
        print("Error saving inventory.")


def main():
    inventory = Inventory()
    supplier = Supplier("S001", "ABC Supplies", "abc@example.com")

    if not load_inventory(inventory, supplier):
        return

    while True:
        print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("\nChoose product type:")
            print("1. Physical product")
            print("2. Digital product")

            product_type = input("Enter type (1-2): ")

            if product_type not in ("1", "2"):
                print("Invalid product type.")
                continue

            product_id = input("Enter product ID: ").strip()
            name = input("Enter product name: ").strip()

            try:
                price = get_positive_float("Enter price: ")
                stock = int(input("Enter stock quantity: "))

                if not product_id or not name:
                    print("ID and name cannot be empty.")
                    continue

                if price < 0 or stock < 0:
                    print("Price and stock cannot be negative.")
                    continue

                if product_type == "1":
                    weight = float(input("Enter weight (kg): "))

                    if weight < 0:
                        print("Weight cannot be negative.")
                        continue

                    product = ProductFactory.create(
                        "physical", product_id, name, price, stock,
                        supplier, weight=weight
                    )

                else:
                    download_size = float(
                        input("Enter download size (MB): ")
                    )

                    if download_size < 0:
                        print("Download size cannot be negative.")
                        continue

                    product = ProductFactory.create(
                        "digital", product_id, name, price, stock,
                        supplier, download_size=download_size
                    )

                inventory.add_product(product)

            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "3":
            product_id = input("Enter product ID: ").strip()
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
            else:
                try:
                    quantity = int(input("Enter new stock: "))
                    product.update_stock(quantity)
                except ValueError:
                    print("Please enter a valid whole number.")

        elif choice == "4":
            product_id = input("Enter product ID: ").strip()
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
            else:
                product.display_information()

        elif choice == "5":
            save_inventory(inventory)

        elif choice == "6":
            save_inventory(inventory)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()
