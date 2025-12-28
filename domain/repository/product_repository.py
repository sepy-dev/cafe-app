from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.product import Product


class ProductRepository(ABC):

    @abstractmethod
    def save(self, product: Product) -> int:
        """ذخیره محصول جدید و برگرداندن ID"""
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """دریافت محصول بر اساس ID"""
        pass

    @abstractmethod
    def get_all_active(self) -> List[Product]:
        """دریافت تمام محصولات فعال"""
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """دریافت محصولات بر اساس دسته‌بندی"""
        pass

    @abstractmethod
    def update(self, product: Product) -> None:
        """به‌روزرسانی محصول"""
        pass

    @abstractmethod
    def delete(self, product_id: int) -> None:
        """حذف محصول (غیرفعال کردن)"""
        pass
