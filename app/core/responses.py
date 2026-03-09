from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel
from app.schemas.recipe import RecipeRead, RecipeReadAfterCreate

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: Optional[T] = None

class RecipeReadResponse(BaseModel):
    message: str = "OK"
    recipe: RecipeRead

class RecipeCreateResponse(BaseModel):
    message: str = "OK"
    recipe: RecipeReadAfterCreate

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: list[T]
    total: int
    page: int
    page_size: int

class RecipesResponse(BaseModel, Generic[T]):
    recipes: list[T]

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[Any] = None


def ok(data: Any = None, message: str = "OK") -> dict:
    return SuccessResponse(data=data, message=message).model_dump()


def paginated(data: list, total: int, page: int, page_size: int) -> dict:
    return PaginatedResponse(
        data=data, total=total, page=page, page_size=page_size
    ).model_dump()

def recipe_read(data: Any = None, message: str = "OK") -> dict:
    return RecipeReadResponse(
        recipe=data,
        message=message
    ).model_dump()

def recipe_created(data: Any = None, message: str = "OK") -> dict:
    return RecipeCreateResponse(
        recipe=data,
        message=message
    ).model_dump()

def recipes(data: list) -> dict:
    return RecipesResponse(
        recipes=data
    ).model_dump()
