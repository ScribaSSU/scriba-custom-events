import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import db_conf

__log = logging.getLogger('Database')

SQLALCHEMY_DATABASE_URI_MARIA_DB = \
    f"mysql+pymysql://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['db_name']}"

engine = create_engine(SQLALCHEMY_DATABASE_URI_MARIA_DB, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    try:
        __log.info('Import models...')
        import models
        __log.info('Database creating...')
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        __log.error(f'Error occurred during database initialization: {e}')
    __log.info('Database was initialized successfully.')
