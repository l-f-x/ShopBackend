from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql.functions import now

from api.utils.dbUtils import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    login = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    real_name = Column(String(50), nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    register_date = Column(DateTime, nullable=False, default=now())
    status = Column(String(1), default='1', nullable=False)
    role = Column(String(10), default='user', nullable=False)
    photos = relationship("Photo", back_populates="owner")


class TokenBlacklist(Base):
    __tablename__ = 'blacklisted_tokens'
    token = Column(String(256), primary_key=True, nullable=False)


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_name = Column(String(100), nullable=False)
    product_description = Column(String(1000))
    product_price = Column(Integer, nullable=False)
    product_views = Column(Integer, nullable=False, default=0)
    is_in_stock = Column(Boolean, nullable=False, default=True)
    has_sale = Column(Boolean, nullable=False, default=False)
    price_on_sale = Column(Integer, default=100)
    product_weight = Column(Integer)


class Photo(Base):
    __tablename__ = 'photos'
    photo_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    upload_date = Column(DateTime, default=now())
    photo = Column(BYTEA)
    is_selected_avatar = Column(Boolean, nullable=False, default=True)
    owner = relationship("User", back_populates="photos")
