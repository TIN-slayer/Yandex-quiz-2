import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    round = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("view.id"))
    set = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    end = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    contin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    players = orm.relation('Player')
    view = orm.relation('View')
