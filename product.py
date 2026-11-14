
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.supplier: Supplier = supplier

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        if stock < 0:
            raise ValueError("Stock cannot be negative.")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock


    def update_stock(self, quantity: int) -> bool:
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        self.__stock = quantity
        print("Stock updated successfully!")
        return True


    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")
        print("--------------------")

    def to_dict(self) -> dict[str, str | float | int]:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, weight: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print("Weight:", self.weight, "kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        return self.weight * 5


CanBeShipped.register(PhysicalProduct)


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, download_size: float, supplier: Supplier):
        super().__init__(product_id, name, price, stock, supplier)
        self.download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print("Download size:", self.download_size, "MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

