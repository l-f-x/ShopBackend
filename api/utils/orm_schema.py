from typing import List, Optional
from pydantic.datetime_parse import datetime

from pydantic import BaseModel, EmailStr, SecretStr, validator, Field


class PhotoBase(BaseModel):
    upload_date: datetime
    photo: bytes


class Photo(PhotoBase):
    photo_id: int
    owner_id: int

    class Config:
        orm_mode = True


class PhotoCreate(Photo):
    pass


class UserBase(BaseModel):
    login: EmailStr
    real_name: str = Field(..., example="Ivan Ivanov")

    @validator('real_name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('Realname must contain a space')
        return v


class User(UserBase):
    id: int
    status: str
    role: str
    register_date: datetime
    photos: List[Photo] = []

    class Config:
        orm_mode = True
