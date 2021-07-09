from fastapi import HTTPException
from api.utils.dbUtils import database
from api.product import schema


async def add_product(data: schema.NewProduct):
    query = "insert into products values(nextval('product_id_sequence'), :name, :desc, :price, 0, :in_stock, " \
            ":has_sale, :sale_price, :weight ) "
    return await database.execute(query, values={
        "name": data.product_name,
        "desc": data.product_description,
        "price": data.product_price,
        "in_stock": data.is_in_stock,
        "has_sale": data.has_sale,
        "sale_price": data.price_on_sale,
        "weight": data.product_weight
    })
