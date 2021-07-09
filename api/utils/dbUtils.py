import databases
import sqlalchemy
from functools import lru_cache

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api import config


@lru_cache()
def settings():
    return config.Settings()


def database_pgsql_url_config():
    return str(settings().DB_CONNECTION +
               '://' +
               settings().DB_USERNAME +
               ':' +
               settings().DB_PASSWORD +
               '@' +
               settings().DB_HOST +
               ':' +
               settings().DB_PORT +
               '/' +
               settings().DB_DATABASE)


# database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# metadata.create_all(engine)
