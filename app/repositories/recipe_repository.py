from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate

class RecipeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 999999999) -> list[Recipe]:
        recipes = self.db.query(Recipe).offset(skip).limit(limit).all()
        return recipes

    def get_by_id(self, recipe_id: int) -> Recipe | None:
        return self.db.query(Recipe).filter(Recipe.id == recipe_id).first()

    def create(self, payload: RecipeCreate) -> Recipe:
        recipe = Recipe(**payload.model_dump())
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def update(self, recipe: Recipe, payload: RecipeUpdate) -> Recipe:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(recipe, field, value)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def delete(self, recipe: Recipe) -> None:
        self.db.delete(recipe)
        self.db.commit()
