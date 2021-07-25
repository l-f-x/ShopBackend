from pydantic import BaseModel, Field, EmailStr, SecretStr, validator
from api.utils import orm_schema


class UserCreate(orm_schema.UserBase):
    password: SecretStr = Field(..., example="password")

    @validator('password')
    def password_size(cls, v):
        if len(v) < 6:
            raise ValueError('Password must contain 6+ symbols')
        return v


class BlacklistToken(BaseModel):
    token: SecretStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    login: EmailStr
    password: SecretStr
