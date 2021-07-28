from typing import List, Optional
from pydantic.datetime_parse import datetime
from pydantic import BaseModel, EmailStr, SecretStr, validator, Field
from pydantic.schema import Any


class ProductBase(BaseModel):
    product_name: str
    product_description: Optional[str] = None
    product_price: int
    is_in_stock: Optional[bool] = True
    has_sale: Optional[bool] = False
    price_on_sale: Optional[int] = 100
    product_weight: Optional[int] = None

    class Config:
        orm_mode = True


class PreProduct(ProductBase):

    id: int
    product_views: int

    class Config:
        orm_mode = True


class Product(PreProduct):
    photo: bytes

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    pass


class Cart(BaseModel):
    product_id: int
    count: int

    class Config:
        orm_mode = True


class CreatePhoto(BaseModel):
    upload_date: datetime
    photo: bytes
    owner_id: int


class Photo(CreatePhoto):
    photo_id: int

    class Config:
        orm_mode = True


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
    balance: int
    register_date: datetime
    photos: List[Photo] = []
    products: List[Cart] = []

    class Config:
        orm_mode = True
