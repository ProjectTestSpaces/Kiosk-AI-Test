from sqlalchemy import Table, Column, String, JSON, DateTime, MetaData
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

cms_activity_logs = Table(
    "cms_activity_logs",
    metadata,
    Column("log_id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", UUID(as_uuid=True)),
    Column("activity_type", String(50)),
    Column("payload", JSON),
    Column("timestamp", DateTime)
)
