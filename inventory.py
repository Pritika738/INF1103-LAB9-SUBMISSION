
from product import Product, PhysicalProduct, DigitalProduct


class Inventory:
    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if self.find_product(product.get_product_id()) is not None:
            print("Product ID already exists.")
            return

        self.__products.append(product)
        print("Product added successfully!")

    def remove_product(self, product_id: str) -> None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                self.__products.remove(product)
                return

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product

        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def display_all(self) -> None:
        if not self.__products:
            print("Inventory is empty.")
            return

        for product in self.__products:
            product.display_information()

    def get_all_products(self) -> list[Product]:
        return self.__products.copy()

