from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field

# Pydantic v2: decimal_places is not a valid Field constraint — use Annotated + condecimal
PositiveDecimal = Annotated[Decimal, Field(gt=0)]

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: PositiveDecimal
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[PositiveDecimal] = None
    is_active: Optional[bool] = None

class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
