import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Inf(SqlAlchemyBase):
    __tablename__ = 'inf'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    now = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    valid = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    town = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    town_inf = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    quest = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    quest_ans = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    melody = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    melody_inf = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    inst = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("view.id"))
    view = orm.relation('View')
