from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, Field, field_serializer

# Pydantic v2: decimal_places is not a valid Field constraint — use Annotated + condecimal
PositiveDecimal = Annotated[Decimal, Field(gt=0)]

class RecipeBase(BaseModel):
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class RecipeReadAfterCreate(RecipeBase):
    id: Optional[int] = None
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

    @field_serializer("created_at", "updated_at")
    def format_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime("%Y-%m-%d %H:%M:%S") if value else None

class RecipeRead(RecipeBase):
    id: Optional[int] = None
    title: str
    making_time: str
    serves: str
    ingredients: str
    cost: int

    model_config = {"from_attributes": True}
