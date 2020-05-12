import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class View(SqlAlchemyBase):
    __tablename__ = 'view'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    rounds = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)


