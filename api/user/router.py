from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from sqlalchemy.orm import Session
from typing import List

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
async def upload_avatar(file: UploadFile = File(...), auth: schema.Auth = Depends(),db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    if await crud.get_user_photos_count(user_id, db) == 10:
        raise HTTPException(status_code=400, detail='You have max avatars count')
    return await crud.upload_photo(user_id, file, db)


@router.post('/users/get_all_photos_ids')
async def get_all_photos_ids(auth: schema.Auth, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token.get_secret_value(), db)
    return await crud.get_all_photos_ids(user_id, db)


@router.get('/users/get_photo/{owner_id}/{photo_id}')
async def get_photo(token: str, owner_id: int, photo_id: int, db: Session = Depends(get_db)):
    user_id = await cryptoUtils.get_user_id_by_token(token, db)
    return StreamingResponse(io.BytesIO(await crud.get_photo(photo_id, owner_id, db)), media_type='image/png')


