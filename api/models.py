from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, Sequence, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, Sequence("user_id_sequence"), nullable=False, primary_key=True, autoincrement=True),
    Column("login", String(100)),
    Column("password", String(100)),
    Column("real_name", String(50)),
    Column("register_date", DateTime),
    Column("status", String(1), default='1'),
    Column("role", String, default='user')
)

token_blacklist = Table(
    'blacklisted_tokens', metadata,
    Column("token", String(256), primary_key=True, nullable=False)
)

products = Table(
    "products", metadata,
    Column("id", Integer, Sequence("product_id_sequence"), nullable=False, primary_key=True, autoincrement=True),
    Column("product_name", String(100), nullable=False),
    Column("product_description", String(1000)),
    Column("product_price", Integer, nullable=False),
    Column("product_views", Integer, nullable=False, default=0),
    Column("is_in_stock", Boolean, nullable=False, default=True),
    Column("has_sale", Boolean, nullable=False, default=False),
    Column("price_on_sale", Integer, nullable=False, default=100),
    Column("product_weight", Integer)
)

photos = Table(
    "photos", metadata,
    Column("photo_id", Integer, Sequence("photo_id_sequence"), nullable=False, primary_key=True, autoincrement=True),
    Column("owner_id", Integer, ForeignKey('users.id'), nullable=False),
    Column("upload_date", DateTime),
    Column("photo", BYTEA)
)
