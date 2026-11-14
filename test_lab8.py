from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct

supplier = Supplier("S001", "ABC Supplies", "abc@example.com")

physical = PhysicalProduct("P001", "Laptop", 1200.0, 10, 2.5, supplier)
digital = DigitalProduct("D001", "Software", 50.0, 100, 500.0, supplier)

print("Physical Product Supplier:")
physical.supplier.display_information()

print("\nDigital Product Supplier:")
digital.supplier.display_information()

del supplier

print("\nAfter deleting supplier variable:")
physical.supplier.display_information()
digital.supplier.display_information()


from inventory import Inventory

print("\n--- Aggregation Test ---")

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(physical)

print("\nProduct in Inventory A:")
print(inventory_a.find_product("P001") is physical)

inventory_a.remove_product("P001")

print("\nProduct removed from Inventory A:")
print(inventory_a.find_product("P001") is None)

print("\nProduct still exists:")
physical.display_information()

inventory_b.add_product(physical)

print("\nSame Product in Inventory B:")
print(inventory_b.find_product("P001") is physical)


from order import Order

print("\n--- Composition Test ---")

order_a = Order("O001")
order_b = Order("O002")

order_a.add_order_line(physical, 2)
order_a.add_order_line(digital, 1)

print("\nOrder A:")
for line in order_a.order_lines:
    print(line.product.get_name(), "Quantity:", line.quantity,
          "Subtotal:", line.calculate_subtotal())

print("Order A Total:", order_a.calculate_total())

order_b.add_order_line(physical, 1)

print("\nOrder B:")
for line in order_b.order_lines:
    print(line.product.get_name(), "Quantity:", line.quantity,
          "Subtotal:", line.calculate_subtotal())

print("Order B Total:", order_b.calculate_total())

print("\nSame Product object:")
print(order_a.order_lines[0].product is order_b.order_lines[0].product)

print("\nDifferent OrderLine objects:")
print(order_a.order_lines[0] is not order_b.order_lines[0])

del order_b
print("\nOrder B removed; original Product still exists:")
physical.display_information()


print("\n--- LSP Test ---")

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

show_product_details(physical)
show_product_details(digital)

inventory_lsp = Inventory()
inventory_lsp.add_product(physical)
inventory_lsp.add_product(digital)

inventory_lsp.display_all()

print("\n--- Polymorphism Test ---")

for product in inventory_lsp.get_all_products():
    product.display_information()
    print(product.get_fulfilment_info())


from discount import BulkDiscount, PercentageDiscount

print("\n--- Lab 9 Strategy Test ---")

discount_order = Order("O003", BulkDiscount(200, 20))
discount_order.add_order_line(digital, 5)

print("Bulk discount total:", discount_order.calculate_total())

discount_order.set_discount(PercentageDiscount(10))
print("Percentage discount total:", discount_order.calculate_total())
