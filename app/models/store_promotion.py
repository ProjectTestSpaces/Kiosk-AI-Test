from sqlalchemy import Table, Column, String, Text, DateTime, Numeric, MetaData
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy

metadata = MetaData()

store_promotions = Table(
    "store_promotions",
    metadata,
    Column("promotion_id", UUID(as_uuid=True), primary_key=True),
    Column("shop_id", UUID(as_uuid=True), nullable=False),
    Column("mall_id", UUID(as_uuid=True), nullable=False),
    Column("title", String(100), nullable=False),
    Column("description", Text),
    Column("discount", Numeric(5,2)),
    Column("start_date", DateTime, nullable=False),
    Column("end_date", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=sqlalchemy.func.now()),
    Column("updated_at", DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now()),
)
