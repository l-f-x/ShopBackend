from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.exceptions.user_exceptions import *
from api.exceptions.auth_exception import *
from api.utils import cryptoUtils, orm_schema
from api.auth import crud, schema
from api.utils.dbUtils import SessionLocal

router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/auth/register", response_model=orm_schema.UserBase)
async def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    # check if user exist
    result = await crud.is_user_exist(user.login, db)
    if result:
        raise HTTPException(status_code=400, detail='user exist')
    # add new user if not
    await crud.add_user(user, db)
    return orm_schema.UserBase(**user.dict())


@router.post("/auth/login")
async def login(body: schema.UserLogin, db: Session = Depends(get_db)):
    # check if user exist
    result = await crud.is_user_exist(body.login, db)
    if not result:
        raise HTTPException(status_code=400, detail='User not found')
    # check password
    verification = cryptoUtils.verify_password(body.password.get_secret_value(), result.password)
    if not verification:
        raise HTTPException(status_code=400, detail='Incorrect password')
    response = await cryptoUtils.create_access_token(
        data={'owner_id': result.id}
    )
    return response


@router.post("/auth/logout")
async def logout(body: schema.BlacklistToken, db: Session = Depends(get_db)):
    return await crud.add_token_to_blacklist(body.token, db)
