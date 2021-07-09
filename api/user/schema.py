from pydantic import BaseModel, SecretStr, validator, EmailStr
from fastapi import HTTPException
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


class UserInfoModel(BaseModel):
    id: int
    login: EmailStr
    real_name: str
    register_date: datetime
    status: str
    role: str


class PhotoId(BaseModel):
    photo_id: int
