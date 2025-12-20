from sqlalchemy import Column, Integer, String, Boolean

from infrastructure.database.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String, default="GENERAL")
    is_active = Column(Boolean, default=True)
