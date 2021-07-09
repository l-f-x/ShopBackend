import io

from api.user import schema
from fastapi import HTTPException, UploadFile
from api.utils.dbUtils import database


# from api.utils.photoUtils import bytes_to_file

async def get_user_info(user_id: int):
    query = "select * from users where id=:user_id"
    return schema.UserInfoModel(**(await database.fetch_one(query, values={
        'user_id': user_id
    })))


async def change_user_realname(body: schema.ChangeRealname, user_id: int):
    try:
        query = 'update users set real_name=:realname where id=:user_id'
        await database.execute(query, values={
            'realname': body.realname,
            'user_id': user_id
        }
                               )
        return 'Realname changed successfully'
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Something went wrong')


async def delete_account(user_id: int):
    query = 'delete from users where id=:user_id'
    await database.execute(query, values={
        'user_id': user_id
    })
    return 'User deleted successfully'


async def upload_photo(owner_id: int, file: UploadFile):
    query = "insert into photos values(nextval('photo_id_sequence'), :owner_id, now() at time zone 'UTC', :b_photo)"
    await database.execute(query, values={
        'owner_id': owner_id,
        'b_photo': await file.read()
    })
    return 'Photo successfully uploaded'


async def get_all_photos_ids(owner_id: int):
    query = 'select photo_id from photos where owner_id=:owner_id order by upload_date'
    return await database.fetch_all(query, values={
        'owner_id': owner_id
    })


async def get_photo(photo_id: int, user_id: int):
    query = 'select owner_id, photo from photos where photo_id=:photo_id'
    data = await database.fetch_one(query, values={'photo_id': photo_id})
    if not user_id == data.get('owner_id'):
        raise HTTPException(status_code=403, detail="You haven't access to this photo")
    else:
        return data.get('photo')
