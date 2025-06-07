from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import time, datetime

class StoreHourCreate(BaseModel):
    shop_id: UUID
    day_of_week: str = Field(..., pattern="^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)$")
    open_time: time
    close_time: time
    is_closed: Optional[bool] = False

class StoreHourUpdate(BaseModel):
    open_time: Optional[time]
    close_time: Optional[time]
    is_closed: Optional[bool]

class StoreHourOut(BaseModel):
    id: UUID
    shop_id: UUID
    day_of_week: str
    open_time: time
    close_time: time
    is_closed: bool
    created_at: datetime
    updated_at: datetime
