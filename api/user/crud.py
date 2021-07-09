import io

from sqlalchemy.orm import Session

from api.user import schema
from fastapi import HTTPException, UploadFile
# from api.utils.photoUtils import bytes_to_file
from api.utils import models, orm_schema


async def get_user_info(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()
    # return schema.UserInfoModel(**(await database.fetch_one(query, values={
    #     'user_id': user_id
    # })))


async def change_user_realname(body: schema.ChangeRealname, user_id: int, db: Session):
    db.query(models.User).filter(models.User.id == user_id).update({models.User.real_name: body.realname})
    db.commit()
    return 'Realname changed successfully'


async def delete_account(user_id: int, db: Session):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return 'User deleted successfully'


async def upload_photo(oid: int, file: UploadFile, db: Session):
    db_photo = models.Photo(
        owner_id=oid,
        photo=await file.read()
    )
    db.add(db_photo)
    db.commit()
    return 'Photo successfully uploaded'


async def get_all_photos_ids(owner_id: int, db: Session):
    current_user = db.query(models.User).filter(models.User.id == owner_id).first()
    ans = []
    for photo in current_user.photos:
        ans.append(photo.photo_id)
    return ans


async def get_photo(photo_id: int, user_id: int, db: Session):
    data = db.query(models.Photo).filter(models.Photo.photo_id == photo_id).first()
    if data.owner_id == user_id:
        return data.photo
    else:
        raise HTTPException(status_code=403, detail="You haven't access to this photo")


async def get_user_photos_count(owner_id: int, db: Session):
    return len(db.query(models.User).filter(models.User.id == owner_id).first().photos)
