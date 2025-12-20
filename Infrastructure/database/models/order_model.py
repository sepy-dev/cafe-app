from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from infrastructure.database.base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    discount = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
