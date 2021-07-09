import asyncpg.exceptions
from pydantic import SecretStr
from fastapi import HTTPException
from api.auth.schema import UserCreate
from api.utils import cryptoUtils
from sqlalchemy.orm import Session
from api.utils import orm_schema, models
from api.utils.dbUtils import get_db


async def is_user_exist(email: str, db: Session):
    return db.query(models.User).filter(models.User.login == email).first()


async def add_user(user: orm_schema.UserCreate, db: Session):
    print(user)
    db_user = models.User(
        login=user.login,
        password=cryptoUtils.hash_password(user.password),
        real_name=user.real_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def add_token_to_blacklist(token: SecretStr, db):
    query = 'insert into blacklisted_tokens values(:token)'
    # try:
    #     return await database.execute(query,
    #                                   values={'token': token.get_secret_value()})
    # except asyncpg.exceptions.UniqueViolationError:
    #     raise HTTPException(status_code=400, detail='This token already destroyed')


async def is_token_blacklisted(token: SecretStr, db):
    query = 'select * from blacklisted_tokens where token=:token'
    # return await database.fetch_one(query,
    #                                 values={'token': token.get_secret_value()})
