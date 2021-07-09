from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from sqlalchemy.orm import Session
from typing import List
from api.exceptions.user_exceptions import *
from api.user import crud, schema
from starlette.responses import StreamingResponse
from api.utils import cryptoUtils, orm_schema
from api.auth import crud as auth_crud
import io
from api.utils.dbUtils import SessionLocal

router = APIRouter()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.put('/user/update_realname')
async def update_realname(auth: schema.Auth, body: schema.ChangeRealname = Depends(), db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    return await crud.change_user_realname(body, user_id, db)


@router.delete('/user/delete_account')
async def delete_account(auth: schema.Auth, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    await auth_crud.add_token_to_blacklist(auth.token, db)
    return await crud.delete_account(user_id, db)


@router.post('/users/get_self_info', response_model=orm_schema.User)
async def get_self_info(auth: schema.Auth, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    return await crud.get_user_info(user_id, db)


@router.post('/users/upload_avatar')
# Don't delete auth scheme depends or swagger will be send it all in body as multipart
async def upload_avatar(file: UploadFile = File(...), auth: schema.Auth = Depends(), db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    if await crud.get_user_photos_count(user_id, db) == 10:
        raise HTTPException(status_code=400, detail='You have max avatars count')
    return await crud.upload_photo(user_id, file, db)


@router.post('/users/get_all_photos_ids')
async def get_all_photos_ids(auth: schema.Auth, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    return await crud.get_all_photos_ids(user_id, db)


@router.get('/users/get_photo/{photo_id}')
async def get_photo(token: str, photo_id: int, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token, db)
    return StreamingResponse(io.BytesIO(await crud.get_photo(photo_id, user_id, db)), media_type='image/png')


@router.get('/users/selected_avatar/{owner_id}')
async def get_selected_avatar(token: str, owner_id: int, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token, db)
    if user_id == owner_id:
        return StreamingResponse(io.BytesIO((await crud.get_avatar(owner_id, db)).first().photo), media_type='image/png')
    else:
        raise AccessDeniedException


@router.get('/users/balance')
async def get_balance(token: str, db: Session= Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token, db)
    return await crud.get_balance(user_id, db)


@router.post('/users/add_to_balance')
async def add_balance(auth: schema.Auth, body: schema.AddBalance, db: Session= Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    if (await crud.get_user_role(user_id, db)) == 'admin':
        if await crud.is_user_exits(body.user_to_add, db):
            return await crud.add_to_balance(body, db)
        else:
            raise UserNotFoundException
    else:
        raise AccessDeniedException

