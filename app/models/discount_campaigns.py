# from sqlalchemy import Table, Column, String, DateTime, Text
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.sql import func
# from app.db import metadata
# import uuid

# discount_campaigns = Table(
#     "discount_campaigns",
#     metadata,
#     Column()    
# )


from sqlalchemy import (
    Table, Column, String, Text, Date, DateTime, Integer, Numeric, MetaData,
    CheckConstraint, Index, func
)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

discount_campaigns = Table(
    "discount_campaigns",
    metadata,
    Column("campaign_id", UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()),
    Column("shop_id", UUID(as_uuid=True), nullable=False),
    Column("campaign_name", String(100), nullable=False),
    Column("campaign_description", Text),
    Column("discount_type", String(20), nullable=False),
    Column("discount_value", Numeric(10, 2), nullable=False),
    Column("start_date", Date, nullable=False),
    Column("end_date", Date, nullable=False),
    Column("usage_limit", Integer, server_default="0"),
    Column("used_count", Integer, server_default="0"),
    Column("status", String(20), server_default="active"),
    Column("created_at", DateTime, server_default=func.current_timestamp()),
    Column("updated_at", DateTime, server_default=func.current_timestamp()),

    # Constraints
    CheckConstraint("discount_type IN ('percentage', 'flat')", name="discount_type_check"),
    CheckConstraint("status IN ('active', 'expired', 'cancelled')", name="status_check")
)

# Optional: helpful indexes for filtering
Index("idx_discount_campaigns_shop", discount_campaigns.c.shop_id)
Index("idx_discount_campaigns_status", discount_campaigns.c.status)
Index("idx_discount_campaigns_dates", discount_campaigns.c.start_date, discount_campaigns.c.end_date)
