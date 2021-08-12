import io
from typing import List

from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import File
from pydantic import SecretStr, validator
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from api.product import schema
from api.exceptions.user_exceptions import *
from api.product import crud
from api.user import schema as user_schema
from api.user.crud import get_user_role
from api.utils import orm_schema, cryptoUtils
from api.utils.dbUtils import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/product/add")
async def add_product(body: orm_schema.ProductCreate = Depends(),
                      auth: user_schema.Auth = Depends(),
                      db: Session = Depends(get_db), photo: bytes = File(...)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    if await get_user_role(user_id, db) == 'admin':
        return await crud.add_product(body, photo, db)
    else:
        raise AccessDeniedException


@router.get("/product/get/{product_id}", response_model=orm_schema.PreProduct)
async def get_product(product_id: int, token: SecretStr, db: Session = Depends(get_db)):
    await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return await crud.get_product(product_id, db)


@router.get("/product/feed/", response_model=List[orm_schema.PreProduct])
async def get_feed(count: int, offset: int, token: SecretStr, db: Session = Depends(get_db)):
    await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return await crud.get_product_by_views(count, offset, db)


@router.post("/product/add_to_cart")
async def add_to_cart(auth: user_schema.Auth, body: schema.AddToCart, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    return await crud.add_product_to_cart(user_id, body.product_id, body.count, db)


@router.get("/product/cart")
async def get_cart(token: SecretStr, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return (await crud.get_user_cart(user_id, db))


@router.post("/product/search", response_model=List[orm_schema.PreProduct])
async def search(token: SecretStr, query: str, db: Session = Depends(get_db)):
    await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return await crud.search_product(query, db)


@router.get("/product/photo/{product_id}")
async def provide_product_photo(token: SecretStr, product_id: int, db: Session = Depends(get_db)):
    await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return StreamingResponse(io.BytesIO(await crud.get_product_photo(product_id, db)), media_type='image/png')


@router.get('/product/get_preview/{product_id}')
async def get_preview(token: SecretStr, product_id: int, db: Session = Depends(get_db)):
    await cryptoUtils.get_user_id_by_token(token.get_secret_value(), db)
    return await crud.get_product_preview(product_id, db)

