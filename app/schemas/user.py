from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class UserStatusUpdate(BaseModel):
    user_id: UUID
    new_status: str  # Should be 'active', 'banned', or 'restricted'
