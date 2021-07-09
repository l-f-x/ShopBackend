from pydantic import BaseModel, Field, EmailStr, SecretStr, validator


class UserBase(BaseModel):
    email: EmailStr
    realname: str = Field(..., example="Ivan Ivanov")

    @validator('realname')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('Fullname must contain a space')
        return v


class UserCreate(UserBase):
    password: SecretStr = Field(..., example="password")

    @validator('password')
    def password_size(cls, v):
        if len(v) < 6:
            raise ValueError('Password must contain 6+ symbols')
        return v


class UserLogout(BaseModel):
    token: SecretStr
