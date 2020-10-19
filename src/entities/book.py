from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.entities import Base
from src.entities.author_books import author_books_association


class Book(Base):
    title = Column(String(255), nullable=False)
    number_of_pages = Column(Integer, nullable=False)
    authors = relationship('Author', secondary=author_books_association)
