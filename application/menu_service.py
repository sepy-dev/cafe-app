from domain.entities.product import Product
from infrastructure.database.session import SessionLocal
from infrastructure.database.repositories.product_repository_sqlalchemy import (
    ProductRepositorySQLAlchemy
)
from typing import List


class MenuService:
    def __init__(self):
        self.session = SessionLocal()
        self.product_repo = ProductRepositorySQLAlchemy(self.session)

        # مقداردهی اولیه منو در صورت خالی بودن دیتابیس
        self._initialize_menu_if_empty()

    def _initialize_menu_if_empty(self):
        """مقداردهی اولیه منو با محصولات پایه"""
        if not self.product_repo.get_all_active():
            initial_products = [
                Product(0, "قهوه", 50000, "نوشیدنی گرم"),
                Product(0, "لاته", 65000, "نوشیدنی گرم"),
                Product(0, "چای", 30000, "نوشیدنی گرم"),
                Product(0, "کیک شکلاتی", 70000, "دسر"),
                Product(0, "کیک وانیلی", 65000, "دسر"),
                Product(0, "ساندیچ مرغ", 85000, "غذا"),
                Product(0, "پاستا", 95000, "غذا"),
                Product(0, "آب معدنی", 15000, "نوشیدنی سرد"),
                Product(0, "نوشابه", 20000, "نوشیدنی سرد"),
            ]

            for product in initial_products:
                self.product_repo.save(product)

    def get_active_products(self) -> List[Product]:
        """دریافت تمام محصولات فعال"""
        return self.product_repo.get_all_active()

    def get_products_by_category(self, category: str) -> List[Product]:
        """دریافت محصولات بر اساس دسته‌بندی"""
        return self.product_repo.get_by_category(category)

    def get_product_by_id(self, product_id: int) -> Product:
        """دریافت محصول بر اساس ID"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"محصول با ID {product_id} یافت نشد")
        return product

    def add_product(self, name: str, price: int, category: str) -> int:
        """افزودن محصول جدید"""
        if price <= 0:
            raise ValueError("قیمت باید مثبت باشد")

        product = Product(0, name, price, category)
        return self.product_repo.save(product)

    def update_product(self, product_id: int, name: str = None, price: int = None,
                      category: str = None) -> None:
        """به‌روزرسانی محصول"""
        product = self.get_product_by_id(product_id)

        if name is not None:
            product.name = name
        if price is not None:
            if price <= 0:
                raise ValueError("قیمت باید مثبت باشد")
            product.price = price
        if category is not None:
            product.category = category

        self.product_repo.update(product)

    def delete_product(self, product_id: int) -> None:
        """حذف محصول (غیرفعال کردن)"""
        self.product_repo.delete(product_id)

    def get_categories(self) -> List[str]:
        """دریافت لیست دسته‌بندی‌های موجود"""
        products = self.get_active_products()
        categories = set(product.category for product in products)
        return sorted(list(categories))

    def get_all_products(self) -> List[Product]:
        """دریافت تمام محصولات (فعال و غیرفعال)"""
        return self.product_repo.get_all()

    def update_product_price(self, product_id: int, new_price: int) -> None:
        """به‌روزرسانی قیمت محصول"""
        if new_price <= 0:
            raise ValueError("قیمت باید مثبت باشد")
        product = self.get_product_by_id(product_id)
        product.price = new_price
        self.product_repo.update(product)

    def deactivate_product(self, product_id: int) -> None:
        """غیرفعال کردن محصول"""
        product = self.get_product_by_id(product_id)
        product.is_active = False
        self.product_repo.update(product)

    def activate_product(self, product_id: int) -> None:
        """فعال کردن محصول"""
        product = self.get_product_by_id(product_id)
        product.is_active = True
        self.product_repo.update(product)