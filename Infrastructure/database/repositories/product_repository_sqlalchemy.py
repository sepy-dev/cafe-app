from sqlalchemy.orm import Session
from typing import List, Optional
from domain.entities.product import Product
from domain.repository.product_repository import ProductRepository
from infrastructure.database.models.product_model import ProductModel


class ProductRepositorySQLAlchemy(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> int:
        product_model = ProductModel(
            name=product.name,
            price=product.price,
            category=product.category,
            is_active=product.is_active
        )
        self.session.add(product_model)
        self.session.commit()
        return product_model.id

    def get_by_id(self, product_id: int) -> Optional[Product]:
        product_model = self.session.get(ProductModel, product_id)
        if not product_model:
            return None

        return Product(
            id=product_model.id,
            name=product_model.name,
            price=product_model.price,
            category=product_model.category,
            is_active=product_model.is_active
        )

    def get_all(self) -> List[Product]:
        """دریافت همه محصولات (فعال و غیرفعال)"""
        product_models = self.session.query(ProductModel).all()

        return [
            Product(
                id=model.id,
                name=model.name,
                price=model.price,
                category=model.category,
                is_active=model.is_active
            )
            for model in product_models
        ]

    def get_all_active(self) -> List[Product]:
        product_models = (
            self.session.query(ProductModel)
            .filter_by(is_active=True)
            .all()
        )

        return [
            Product(
                id=model.id,
                name=model.name,
                price=model.price,
                category=model.category,
                is_active=model.is_active
            )
            for model in product_models
        ]

    def get_by_category(self, category: str) -> List[Product]:
        product_models = (
            self.session.query(ProductModel)
            .filter_by(category=category, is_active=True)
            .all()
        )

        return [
            Product(
                id=model.id,
                name=model.name,
                price=model.price,
                category=model.category,
                is_active=model.is_active
            )
            for model in product_models
        ]

    def update(self, product: Product) -> None:
        product_model = self.session.get(ProductModel, product.id)
        if product_model:
            product_model.name = product.name
            product_model.price = product.price
            product_model.category = product.category
            product_model.is_active = product.is_active
            self.session.commit()

    def delete(self, product_id: int) -> None:
        product_model = self.session.get(ProductModel, product_id)
        if product_model:
            product_model.is_active = False
            self.session.commit()
