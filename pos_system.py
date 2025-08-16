from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int = 0


@dataclass
class Inventory:
    products: Dict[str, Product] = field(default_factory=dict)

    def add_product(self, product: Product) -> None:
        """Add a new product to the inventory."""
        if product.id in self.products:
            raise ValueError("Product ID already exists.")
        self.products[product.id] = product

    def list_products(self):
        """Return a list of all products."""
        return list(self.products.values())

    def get(self, product_id: str) -> Product:
        """Retrieve a product by ID."""
        return self.products[product_id]


@dataclass
class CartItem:
    product: Product
    quantity: int


@dataclass
class Cart:
    items: Dict[str, CartItem] = field(default_factory=dict)

    def add_item(self, product: Product, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if product.stock < quantity:
            raise ValueError("Not enough stock for product")
        if product.id in self.items:
            self.items[product.id].quantity += quantity
        else:
            self.items[product.id] = CartItem(product, quantity)
        product.stock -= quantity

    def total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items.values())


class PointOfSale:
    """Simple point-of-sale system."""

    def __init__(self) -> None:
        self.inventory = Inventory()
        self.cart = Cart()

    def add_product_to_inventory(self, id: str, name: str, price: float, stock: int) -> None:
        self.inventory.add_product(Product(id=id, name=name, price=price, stock=stock))

    def scan(self, product_id: str, quantity: int = 1) -> None:
        product = self.inventory.get(product_id)
        self.cart.add_item(product, quantity)

    def checkout(self) -> float:
        total = self.cart.total()
        self.cart = Cart()  # reset cart after checkout
        return total


def main() -> None:
    pos = PointOfSale()
    menu = (
        "\n1. Add product\n"
        "2. List products\n"
        "3. Scan item\n"
        "4. View cart total\n"
        "5. Checkout\n"
        "6. Exit\n"
    )
    while True:
        choice = input(f"{menu}Choose an option: ").strip()
        if choice == "1":
            pid = input("Product id: ").strip()
            name = input("Name: ").strip()
            price = float(input("Price: ").strip())
            stock = int(input("Stock: ").strip())
            pos.add_product_to_inventory(pid, name, price, stock)
            print("Product added")
        elif choice == "2":
            for p in pos.inventory.list_products():
                print(f"{p.id}: {p.name} - ${p.price:.2f} ({p.stock} in stock)")
        elif choice == "3":
            pid = input("Product id: ").strip()
            qty = int(input("Quantity: ").strip())
            pos.scan(pid, qty)
            print("Item added to cart")
        elif choice == "4":
            print(f"Cart total: ${pos.cart.total():.2f}")
        elif choice == "5":
            print(f"Total due: ${pos.checkout():.2f}")
        elif choice == "6":
            print("Goodbye")
            break
        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
