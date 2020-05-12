import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    round = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    win = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    now = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    kush = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    match = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("game.id"))
    game = orm.relation('Game')
