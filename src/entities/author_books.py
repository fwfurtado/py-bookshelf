from sqlalchemy import Table, Column, Integer, ForeignKey

from src.entities import Base

author_books_association = Table('author_books', Base.metadata,
                                 Column('author_id', Integer, ForeignKey('authors.id')),
                                 Column('book_id', Integer, ForeignKey('books.id'))
                                 )
