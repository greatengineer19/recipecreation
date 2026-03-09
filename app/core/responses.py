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
    recipe: list[RecipeRead]   # tests assert recipe.be.a('Array')

class RecipeCreateResponse(BaseModel):
    message: str = "OK"
    recipe: list[RecipeReadAfterCreate]  # tests assert recipe.be.a('Array')

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "OK"
    data: list[T]
    total: int
    page: int
    page_size: int

class RecipesResponse(BaseModel, Generic[T]):
    recipes: list[T]   # GET all: tests check res.body.recipes (plural)

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
    # Wrap in list — tests assert res.body.recipe.be.a('Array').length.eql(1)
    return RecipeReadResponse(
        recipe=[data],
        message=message
    ).model_dump()

def recipe_created(data: Any = None, message: str = "OK") -> dict:
    # Wrap in list — tests assert res.body.recipe.be.a('Array').length.eql(1)
    return RecipeCreateResponse(
        recipe=[data],
        message=message
    ).model_dump()

def recipes(data: list) -> dict:
    return RecipesResponse(
        recipes=data
    ).model_dump()
