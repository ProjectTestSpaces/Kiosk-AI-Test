from sqlalchemy import Table , Column, String, Time, Boolean ,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func 
from app.db import metadata

store_operating_hours = Table(
    "store_operating_hours",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()),
    Column("shop_id", UUID(as_uuid=True), nullable=False),
    Column("day_of_week", String(9), nullable=False),
    Column("open_time", Time, nullable=False),
    Column("close_time", Time, nullable=False),
    Column("is_closed", Boolean, default=False),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_default=func.current_timestamp())
)