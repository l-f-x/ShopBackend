from pydantic import BaseModel, Field, SecretStr


class AddToCart(BaseModel):
    product_id: int
    count: int = 1

