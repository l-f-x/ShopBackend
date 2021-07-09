from pydantic import BaseModel, Field


class NewProduct(BaseModel):
    product_name: str = Field(..., example='Хлеб белый. Батон')
    product_description: str = Field(..., example='Свежий белый хлеб компании azizo')
    product_price: int = Field(..., example=50)
    is_in_stock: bool = Field(True, example=True)
    has_sale: bool = Field(False, example=False)
    price_on_sale: int = Field(100, example=35)
    product_weight: int = Field(None, example=300)
