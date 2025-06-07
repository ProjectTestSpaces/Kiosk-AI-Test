from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class ShopAdminCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str
    notes: Optional[str] = None

class ShopAdminUpdate(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ShopAdminOut(BaseModel):
    admin_id: UUID
    username: str
    email: str
    role: str
    status: str
    created_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True
