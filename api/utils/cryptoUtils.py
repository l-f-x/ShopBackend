from passlib.context import CryptContext
from pydantic import SecretStr
import jwt
from sqlalchemy.orm import Session
from api.exceptions.auth_exception import *
from api.auth.crud import is_token_blacklisted
from api.utils import consts, schema
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=['bcrypt'])


def hash_password(password: SecretStr):
    return pwd_context.hash(password.get_secret_value())


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(*, data: dict, expire_delta: timedelta = None):
    encoded_data = data.copy()
    if expire_delta:
        expire_in = datetime.utcnow() + expire_delta
    else:
        expire_in = datetime.utcnow() + timedelta(weeks=consts.DEFAULT_EXPIRE_DATE_IN_WEEKS)
    encoded_data.update({'exp': expire_in})
    token = jwt.encode(encoded_data, key=consts.SECRET_KEY, algorithm=consts.CRYPTO_ALGORITHM)
    return {
        'access_token': token,
        'token_type': 'Bearer',
        'expire_in': expire_in
    }


async def get_user_id_by_token(token: str, db: Session):
    if await is_token_blacklisted(token, db):
        raise InvalidTokenException
    try:
        data = jwt.decode(token, consts.SECRET_KEY, algorithms=consts.CRYPTO_ALGORITHM)
    except jwt.exceptions.DecodeError:
        raise TokenExpireException
    return schema.UserToken(**data).owner_id
