from sqlalchemy import Table, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db import metadata
import uuid

shop_admins = Table(
    "shop_admins",
    metadata,
    Column("admin_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("username", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("role", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("status", String, default="active"),
    Column("notes", Text, nullable=True),
)
