from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok, recipe_read, recipes, recipe_created
from app.schemas.recipe import RecipeCreate, RecipeRead, RecipeUpdate, RecipeReadAfterCreate
from app.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipes", tags=["Recipes"])

def get_service(db: Session = Depends(get_db)) -> RecipeService:
    return RecipeService(db)

# ── GET /recipes ─────────────────────────────────────────────────────────────
@router.get("", status_code=status.HTTP_200_OK, summary="List recipes")
def list_recipes(
    page: int = Query(1, ge=1),
    page_size: int = Query(99999999, ge=1, le=99999999),
    svc: RecipeService = Depends(get_service),
):
    result_recipes = svc.list_recipes(page=page, page_size=page_size)
    return recipes(
        data=[RecipeRead.model_validate(recipe).model_dump() for recipe in result_recipes]
    )

# ── GET /recipes/{id} ────────────────────────────────────────────────────────
@router.get("/{recipe_id}", status_code=status.HTTP_200_OK, summary="Get recipe")
def get_recipe(recipe_id: int, svc: RecipeService = Depends(get_service)):
    recipe = svc.get_recipe(recipe_id)
    return recipe_read(message="Recipe details by id", data=RecipeRead.model_validate(recipe).model_dump())

# ── POST /recipes ─────────────────────────────────────────────────────────────
# We accept a raw Request so we can return 200 + failure message when fields
# are missing, instead of FastAPI's default 422.
@router.post("", status_code=status.HTTP_200_OK, summary="Create recipe")
async def create_recipe(request: Request, svc: RecipeService = Depends(get_service)):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=200,
            content={"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}
        )

    try:
        payload = RecipeCreate(**body)
    except Exception:
        return JSONResponse(
            status_code=200,
            content={"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}
        )

    recipe = svc.create_recipe(payload)
    return recipe_created(message="Recipe successfully created!", data=RecipeReadAfterCreate.model_validate(recipe))

# ── PATCH /recipes/{id} ───────────────────────────────────────────────────────
@router.patch("/{recipe_id}", status_code=status.HTTP_200_OK, summary="Update recipe")
def update_recipe(
    recipe_id: int, payload: RecipeUpdate, svc: RecipeService = Depends(get_service)
):
    recipe = svc.update_recipe(recipe_id, payload)
    return recipe_read(message="Recipe successfully updated!", data=RecipeRead.model_validate(recipe))

# ── DELETE /recipes/{id} ──────────────────────────────────────────────────────
@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK, summary="Delete recipe")
def delete_recipe(recipe_id: int, svc: RecipeService = Depends(get_service)):
    svc.delete_recipe(recipe_id)
    return {"message": "Recipe successfully removed!"}
