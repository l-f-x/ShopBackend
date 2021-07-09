import databases
import sqlalchemy
from functools import lru_cache
from api import config
from api.models import metadata


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


database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)
