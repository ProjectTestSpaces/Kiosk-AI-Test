from sqlalchemy import Table, Column, String, Numeric, Text, ARRAY, DateTime, MetaData
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy

metadata = MetaData()

products = Table(
    "products",
    metadata,
    Column("product_id", UUID(as_uuid=True), primary_key=True),
    Column("shop_id", UUID(as_uuid=True)),
    Column("mall_id", UUID(as_uuid=True)),
    Column("product_name", Text, nullable=False),
    Column("category", Text, nullable=False),
    Column("price", Numeric(10, 2), nullable=False),
    Column("currency", String(5), default="INR"),
    Column("description", Text),
    Column("availability_status", String(20), default="in_stock"),
    Column("tags", ARRAY(Text)),
    Column("media_url", Text),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)
