from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.item import Item
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def list_items(self, page: int = 1, page_size: int = 20) -> tuple[list[Item], int]:
        skip = (page - 1) * page_size
        return self.repo.get_all(skip=skip, limit=page_size)

    def get_item(self, item_id: int) -> Item:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise NotFoundException("Item", item_id)
        return item

    def create_item(self, payload: ItemCreate) -> Item:
        return self.repo.create(payload)

    def update_item(self, item_id: int, payload: ItemUpdate) -> Item:
        item = self.get_item(item_id)
        return self.repo.update(item, payload)

    def delete_item(self, item_id: int) -> None:
        item = self.get_item(item_id)
        self.repo.delete(item)
