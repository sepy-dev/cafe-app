from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.base import Base

DATABASE_URL = "sqlite:///cafe.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def init_db():
    Base.metadata.create_all(engine)
