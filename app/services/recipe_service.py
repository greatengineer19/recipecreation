from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.recipe import Recipe
from app.repositories.recipe_repository import RecipeRepository
from app.schemas.recipe import RecipeCreate, RecipeUpdate


class RecipeService:
    def __init__(self, db: Session):
        self.repo = RecipeRepository(db)

    def list_recipes(self, page: int = 1, page_size: int = 999999999) -> list[Recipe]:
        skip = (page - 1) * page_size
        return self.repo.get_all(skip=skip, limit=page_size)

    def get_recipe(self, recipe_id: int) -> Recipe:
        recipe = self.repo.get_by_id(recipe_id)
        if not recipe:
            raise NotFoundException("Recipe", recipe_id)
        return recipe

    def create_recipe(self, payload: RecipeCreate) -> Recipe:
        return self.repo.create(payload)

    def update_recipe(self, recipe_id: int, payload: RecipeUpdate) -> Recipe:
        recipe = self.get_recipe(recipe_id)
        return self.repo.update(recipe, payload)

    def delete_recipe(self, recipe_id: int) -> None:
        recipe = self.get_recipe(recipe_id)
        self.repo.delete(recipe)
