from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.auth import schema
from api.utils import cryptoUtils
from api.auth import crud

router = APIRouter()


@router.post("/auth/register")
async def register(user: schema.UserCreate):
    # check if user exist
    result = await crud.is_user_exist(user.email)
    if result:
        raise HTTPException(status_code=400, detail='This email already exist')
    # add new user if not
    await crud.add_user(user)
    return {**user.dict()}


@router.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # check if user exist
    result = await crud.is_user_exist(form.username)
    print(result.get('id'))
    if not result:
        raise HTTPException(status_code=400, detail='User not found')
    # check password
    verification = cryptoUtils.verify_password(form.password, result.get('password'))
    if not verification:
        raise HTTPException(status_code=400, detail='Incorrect password')
    response = await cryptoUtils.create_access_token(
        data={'owner_id': result.get('id')}
    )
    return response


@router.post("/auth/logout")
async def logout(body: schema.UserLogout):
    return await crud.add_token_to_blacklist(body.token)
