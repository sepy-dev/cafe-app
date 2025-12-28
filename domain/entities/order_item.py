from domain.value_objects.money import Money

class OrderItem:
    def __init__(self, name: str, price: int, quantity: int):
        self.name = name
        self.unit_price = Money(price)
        self.quantity = quantity

    @property
    def price(self) -> int:
        """برای سازگاری با کدهای قدیمی"""
        return self.unit_price.amount

    def total_price(self) -> Money:
        return self.unit_price * self.quantity
