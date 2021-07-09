from api.auth import router as auth_router
from api.user import router as user_router
from api.product import router as products_router
from names import *
from fastapi import FastAPI, status, Response
from fastapi.logger import logger
import logging
from api.utils.dbUtils import engine, SessionLocal
from api.utils import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router.router, tags=['Auth'])
app.include_router(user_router.router, tags=['User'])
app.include_router(products_router.router, tags=['Products'])


logger.setLevel(logging.DEBUG)


@app.get("/", status_code=status.HTTP_404_NOT_FOUND)
async def read_root():
    #  response.status_code=status.HTTP_404_NOT_FOUND
    return NOT_FOUND
