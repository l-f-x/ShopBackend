from pydantic import BaseModel, SecretStr, validator, EmailStr
from fastapi import HTTPException
from api.utils import orm_schema
from pydantic.datetime_parse import datetime


class Auth(BaseModel):
    token: SecretStr


class ChangeRealname(BaseModel):
    realname: str

    @validator('realname')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise HTTPException(status_code=400, detail='Fullname must contain a space')
        return v


class PhotoId(orm_schema.Photo):
    photo_id: int
