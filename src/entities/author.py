from sqlalchemy import Column, String

from src.entities import Base


class Author(Base):
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)