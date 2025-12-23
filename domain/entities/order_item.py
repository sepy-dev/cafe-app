class OrderItem:
    def __init__(self, name: str, price: int, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self) -> int:
        return self.price * self.quantity
