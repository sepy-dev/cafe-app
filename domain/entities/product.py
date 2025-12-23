class Product:
    def __init__(self, id: int, name: str, price: int, category: str, is_active: bool = True):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.is_active = is_active
