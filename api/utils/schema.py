from pydantic import BaseModel


class UserToken(BaseModel):
    owner_id: int
