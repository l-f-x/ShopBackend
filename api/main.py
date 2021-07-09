from starlette.requests import Request

from api.auth import router as auth_router
from api.user import router as user_router
from api.product import router as products_router
from names import *
from fastapi import FastAPI, status, Response, HTTPException
from fastapi.logger import logger
import logging
from api.utils.dbUtils import engine, SessionLocal
from api.utils import models
from api.exceptions.user_exceptions import *
from api.exceptions.auth_exception import *
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


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=400, detail='User not found')


@app.exception_handler(AccessDeniedException)
async def access_denied_exception_handler(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=403, detail="Access denied")


@app.exception_handler(InvalidPasswordException)
async def invalid_password_exception_handler(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=401, detail="Invalid password")


@app.exception_handler(InvalidTokenException)
async def invalid_token_exception_handler(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=401, detail="Invalid token")


@app.exception_handler(EmailUsedException)
async def email_user_exception_handler(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=400, detail="Email already used")


@app.exception_handler(TokenExpireException)
async def token_expire__exception_handler(request: Request, exc: UserNotFoundException):
    raise HTTPException(status_code=401, detail="Token expire")