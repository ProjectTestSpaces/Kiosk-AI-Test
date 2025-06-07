# from pydantic import BaseModel, condecimal, constr
# from uuid import UUID
# from datetime import date, datetime
# from typing import Optional

# class DiscountCampaignCreate(BaseModel):
#     shop_id: UUID
#     campaign_name: constr(max_length=100)
#     campaign_description: Optional[str]
#     discount_type: str  # "percentage" or "flat"
#     discount_value: condecimal(max_digits=10, decimal_places=2)
#     start_date: date
#     end_date: date
#     usage_limit: Optional[int] = 0
#     notes: Optional[str]

# class DiscountCampaignUpdate(BaseModel):
#     campaign_name: Optional[str]
#     campaign_description: Optional[str]
#     discount_type: Optional[str]
#     discount_value: Optional[condecimal(max_digits=10, decimal_places=2)]
#     start_date: Optional[date]
#     end_date: Optional[date]
#     usage_limit: Optional[int]
#     status: Optional[str]
#     notes: Optional[str]

# class DiscountCampaignOut(BaseModel):
#     campaign_id: UUID
#     shop_id: UUID
#     campaign_name: str
#     discount_type: str
#     discount_value: float
#     start_date: date
#     end_date: date
#     usage_limit: int
#     used_count: int
#     status: str
#     created_at: datetime
#     updated_at: datetime
#     campaign_description: Optional[str]
#     notes: Optional[str]



from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

class DiscountCampaignCreate(BaseModel):
    shop_id: UUID
    campaign_name: str = Field(..., max_length=100)
    campaign_description: Optional[str] = None
    discount_type: str = Field(..., pattern="^(percentage|flat)$")  # "percentage" or "flat"
    discount_value: Decimal = Field(..., max_digits=10, decimal_places=2, gt=0)
    start_date: date
    end_date: date
    usage_limit: Optional[int] = Field(default=0, ge=0)
    # notes: Optional[str] = None

class DiscountCampaignUpdate(BaseModel):
    campaign_name: Optional[str] = Field(None, max_length=100)
    campaign_description: Optional[str] = None
    discount_type: Optional[str] = Field(None, pattern="^(percentage|flat)$")
    discount_value: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2, gt=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    usage_limit: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|inactive|expired)$")
    # notes: Optional[str] = None

class DiscountCampaignOut(BaseModel):
    campaign_id: UUID
    shop_id: UUID
    campaign_name: str
    discount_type: str
    discount_value: float
    start_date: date
    end_date: date
    usage_limit: int
    used_count: int
    status: str
    created_at: datetime
    updated_at: datetime
    campaign_description: Optional[str] = None
    # notes: Optional[str] = None