from fastapi import APIRouter
from api.product import schema

router = APIRouter()


@router.post("/product/add")
async def add_product(body: schema.NewProduct):
    return body
