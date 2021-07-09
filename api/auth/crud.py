import asyncpg.exceptions
from sqlalchemy.sql.functions import now
from pydantic import SecretStr
from fastapi import HTTPException
from api.utils.dbUtils import database
from api.auth.schema import UserCreate
from api.utils import cryptoUtils


async def is_user_exist(email: str):
    query = "select * from users where status='1' and login=:login"
    return await database.fetch_one(query,
                                    values={
                                        'login': email
                                    }
                                    )


async def add_user(user: UserCreate):
    query = "insert into users values(nextval('user_id_sequence'),:login, :password, :real_name,now() at time zone " \
            "'UTC','1','user') "
    return await database.execute(query,
                                  values={
                                      'login': user.email,
                                      'password': cryptoUtils.hash_password(user.password),
                                      'real_name': user.realname
                                  }
                                  )


async def add_token_to_blacklist(token: SecretStr):
    query = 'insert into blacklisted_tokens values(:token)'
    try:
        return await database.execute(query,
                                      values={'token': token.get_secret_value()})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail='This token already destroyed')


async def is_token_blacklisted(token: SecretStr):
    query = 'select * from blacklisted_tokens where token=:token'
    return await database.fetch_one(query,
                                    values={'token': token.get_secret_value()})
