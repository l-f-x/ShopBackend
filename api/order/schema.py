from pydantic import BaseModel
from pydantic.types import List


class OrderCreate(BaseModel):
    product: int
    count: int
