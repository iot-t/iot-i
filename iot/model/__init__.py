from pecan import conf  # noqa
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

Session = scoped_session(sessionmaker())
metadata = MetaData()

def _engine_from_config(config):
    config = dict(config)
    url = config.pop('url')
    return create_engine(url, **config)

def init_model():
    """
    This is a stub method which is called at application startup time.

    If you need to bind to a parsed database configuration, set up tables or
    ORM classes, or perform any database initialization, this is the
    recommended place to do it.

    For more information working with databases, and some common recipes,
    see https://pecan.readthedocs.io/en/latest/databases.html
    """
    conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)

def start():
    Session.bind = conf.sqlalchemy.engine
    metadata.bind = Session.bind

def commit():
    Session.commit()

def rollback():
    Session.rollback()

def clear():
    Session.remove()

def get_current_session():
    # This will return thread local session
    return Session()

