import os
from datetime import datetime

from inflection import pluralize, underscore
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class BaseEntity:

    @declared_attr
    def __tablename__(self):
        return pluralize(underscore(self.__name__)).lower()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.now)

    def update(self, model):
        columns = [column.key for column in self.__table__.columns]

        for column in columns:
            column_value = getattr(model, column)

            if column_value:
                setattr(self, column, column_value)

        return self

    def __repr__(self) -> str:
        type_name = type(self).__name__
        fields = ', '.join(f'{field}={value}' for field, value in vars(self).items())

        return f'<{type_name}({fields})>'


Base = declarative_base(cls=BaseEntity)
