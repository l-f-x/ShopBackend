import sqlalchemy.exc
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import Session
from api.exceptions import product_exceptions
from api.product import schema
from api.utils import orm_schema
from api.utils import models


async def add_product(data: orm_schema.ProductCreate, photo: bytes, db: Session):
    db_product = models.Product(
        photo=photo,
        product_name=data.product_name,
        product_description=data.product_description,
        product_price=data.product_price,
        product_weight=data.product_weight,
        is_in_stock=data.is_in_stock,
        has_sale=data.has_sale,
        price_on_sale=data.price_on_sale
    )
    db.add(db_product)
    db.commit()
    return 'Product successfully added'


async def get_product(product_id: int, db: Session):
    product = db.query(models.Product).filter(models.Product.id == product_id)
    req = product.filter(models.Product.id == product_id)
    product = product.one()
    actual_product_views = product.product_views
    req.update({models.Product.product_views: actual_product_views + 1})
    db.commit()
    return product


async def get_product_by_views(count: int, offset: int, db: Session):
    return db.query(models.Product).order_by(desc(models.Product.product_views)).limit(count).offset(offset).all()


async def add_product_to_cart(user_id: int, product_id, count: int, db: Session):
    product_duplicate = await is_product_exits_in_cart(user_id, product_id, db)
    if product_duplicate:
        count_in_cart_now = product_duplicate.count
        db.query(models.Cart).filter(models.User.id == user_id, models.Cart.product_id == product_id).update(
            {models.Cart.count: count_in_cart_now + 1}, synchronize_session='fetch'
        )
        db.commit()
    else:
        db_cart = models.Cart(
            user_id=user_id,
            product_id=product_id,
            count=count
        )
        db.add(db_cart)

        try:
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=400, detail='Product not found')
    return 'ok'


async def is_product_exits_in_cart(user_id: int, product_id: int, db: Session):
    return db.query(models.Cart).filter(models.User.id == user_id, models.Cart.product_id == product_id).first()


async def get_user_cart(user_id: int, db: Session):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def search_product(query: str, db: Session):
    return db.query(models.Product).filter(models.Product.product_name.like('%' + query + '%')).limit(30).all()


async def get_product_photo(product_id: int, db: Session):
    return db.query(models.Product).filter(models.Product.id == product_id).first().photo
