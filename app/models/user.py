from sqlalchemy import Table, Column, String, DateTime, MetaData
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String, nullable=False),
    Column("email", String, nullable=False),
    Column("status", String, default="active"),
    Column("created_at", DateTime, server_default=sqlalchemy.func.now()),
    Column("updated_at", DateTime, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now())
)
