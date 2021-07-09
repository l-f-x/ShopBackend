from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response
from api.user import crud, schema
from starlette.responses import StreamingResponse
from api.utils import cryptoUtils
from api.auth import crud as auth_crud
import io

router = APIRouter()


@router.put('/user/update_realname')
async def update_realname(auth: schema.Auth = Depends(), body: schema.ChangeRealname = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    return await crud.change_user_realname(body, user_id)


@router.delete('/user/delete_account')
async def delete_account(auth: schema.Auth = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    await auth_crud.add_token_to_blacklist(auth.token)
    return await crud.delete_account(user_id)


@router.post('/users/get_self_info')
async def get_self_info(auth: schema.Auth = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    return await crud.get_user_info(user_id)


@router.post('/users/upload_avatar')
async def upload_avatar(file: UploadFile = File(...), auth: schema.Auth = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    return await crud.upload_photo(user_id, file)


#   return StreamingResponse(io.BytesIO(await crud.upload_photo(user_id, file)), media_type='image/png')
#    return Response(content=await file.read(), media_type='image/png')

@router.post('/users/get_all_photos_ids')
async def get_all_photos_ids(auth: schema.Auth = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    return await crud.get_all_photos_ids(user_id)


@router.post('/users/get_photo')
# переделать на get запрос типа /user/get_photo/{user_id}_{photo_id}?token=':token'
async def get_photo(auth: schema.Auth = Depends(), body: schema.PhotoId = Depends()):
    user_id = await cryptoUtils.get_user_id_by_token(auth.token)
    return StreamingResponse(io.BytesIO(await crud.get_photo(body.photo_id, user_id)), media_type='image/png')
