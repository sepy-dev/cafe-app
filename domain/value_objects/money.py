class Money:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("مبلغ نمی‌تواند منفی باشد")
        self.amount = amount

    def __add__(self, other: 'Money') -> 'Money':
        return Money(self.amount + other.amount)

    def __sub__(self, other: 'Money') -> 'Money':
        return Money(max(0, self.amount - other.amount))

    def __mul__(self, factor: int) -> 'Money':
        return Money(self.amount * factor)

    def __str__(self) -> str:
        return f"{self.amount:,} تومان"

    def __eq__(self, other: 'Money') -> bool:
        return self.amount == other.amount

    def __lt__(self, other: 'Money') -> bool:
        return self.amount < other.amount

    def __le__(self, other: 'Money') -> bool:
        return self.amount <= other.amount

    def __gt__(self, other: 'Money') -> bool:
        return self.amount > other.amount

    def __ge__(self, other: 'Money') -> bool:
        return self.amount >= other.amount
