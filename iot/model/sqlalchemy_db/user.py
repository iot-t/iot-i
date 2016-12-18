import datetime
import sqlalchemy as sa

from iot.model.sqlalchemy_db.base import Base

class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(20), nullable=False)
    passwd = sa.Column(sa.String(64), nullable=False)
    salt = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(50), nullable=False)
    create_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    actived = sa.Column(sa.Boolean, default=False)
