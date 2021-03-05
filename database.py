import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import db_conf

__log = logging.getLogger("Database")

SQLALCHEMY_DATABASE_URI_MARIA_DB = f"mysql+pymysql://{db_conf['user']}:{db_conf['password']}@{db_conf['host']}:{db_conf['port']}/{db_conf['db_name']}"

#TODO: переделать под flask sqlalchemy
def init_db():
    try:
        __log.info("Import models...")
        import models
        __log.info("Database creating...")
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        __log.error(f"Error occurred during database initialization: {e}")
    __log.info("Database was initialized successfully.")
