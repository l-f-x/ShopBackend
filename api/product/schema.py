from pydantic import BaseModel, Field, SecretStr

from api.utils.orm_schema import PreProduct


class AddToCart(BaseModel):
    product_id: int
    count: int = 1

class CartItem(BaseModel):
    count: int
    product: PreProduct