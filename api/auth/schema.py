from pydantic import BaseModel, Field, EmailStr, SecretStr, validator


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(..., example="password")
    realname: str = Field(..., example="Ivan Ivanov")

    @validator('password')
    def password_size(cls, v):
        if len(v) < 6:
            raise ValueError('Password must contain 6+ symbols')
        return v

    @validator('realname')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('Fullname must contain a space')
        return v


# class UserPassword(BaseModel):
#     password: SecretStr


class UserLogout(BaseModel):
    token: SecretStr
