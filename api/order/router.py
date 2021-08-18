from typing import List

from fastapi import APIRouter, Depends
from pydantic import SecretStr
from api.order import schema
from api.utils import cryptoUtils
from api.utils.dbUtils import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post('/orders/new')
async def create_order(token: SecretStr, body: List[schema.OrderCreate], db = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
