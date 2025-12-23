from domain.entities.product import Product


class MenuService:
    def __init__(self):
        # فعلاً تستی — بعداً از DB میاد
        self._products = [
            Product(1, "قهوه", 50000, "HOT"),
            Product(2, "لاته", 65000, "HOT"),
            Product(3, "چای", 30000, "HOT"),
            Product(4, "کیک شکلاتی", 70000, "CAKE"),
        ]

    def get_active_products(self):
        return [p for p in self._products if p.is_active]

    def get_product_by_id(self, product_id: int) -> Product:
        for p in self._products:
            if p.id == product_id:
                return p
        raise Exception("Product not found")
