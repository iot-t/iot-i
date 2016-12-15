import datetime
import sqlalchemy as sa

from iot.model.sqlalchemy.base import Base

class User(Base):
    __table_name__ = 'users'

    id = sa.Column(sa.Interge, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(20), nullable=False),
    passwd = sa.Column(sa.String(50), nullable=False),
    salt = sa.Column(sa.String(50), nullable=False),
    email = sa.Column(sa.String(50), nullable=False),
    create_at = sa.Column(sa.DateTime, defualt=datetime.datetime.utcnow),
    actived = sa.Column(sa.Boolean, defualt=False)
