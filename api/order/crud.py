from typing import List

from sqlalchemy.orm import Session

from api.order import schema

async def new_order(user_id: int, products:List[schema.OrderCreate], db: Session):
    db.add()