from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class StorePromotionBase(BaseModel):
    shop_id: UUID
    mall_id: UUID
    title: str
    description: Optional[str]
    discount: Optional[float]
    start_date: datetime
    end_date: datetime

class StorePromotionCreate(StorePromotionBase):
    pass

class StorePromotionUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    discount: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
