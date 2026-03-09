from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.responses import ok, paginated
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])

def get_service(db: Session = Depends(get_db)) -> ItemService:
    return ItemService(db)

@router.get("/", summary="List items")
def list_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    svc: ItemService = Depends(get_service),
):
    items, total = svc.list_items(page=page, page_size=page_size)
    return paginated(
        data=[ItemRead.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
    )

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Create item")
def create_item(payload: ItemCreate, svc: ItemService = Depends(get_service)):
    item = svc.create_item(payload)
    return ok(data=ItemRead.model_validate(item), message="Item created.")

@router.get("/{item_id}", summary="Get item")
def get_item(item_id: int, svc: ItemService = Depends(get_service)):
    item = svc.get_item(item_id)
    return ok(data=ItemRead.model_validate(item))

@router.patch("/{item_id}", summary="Update item")
def update_item(
    item_id: int, payload: ItemUpdate, svc: ItemService = Depends(get_service)
):
    item = svc.update_item(item_id, payload)
    return ok(data=ItemRead.model_validate(item), message="Item updated.")

@router.delete(
    "/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete item"
)
def delete_item(item_id: int, svc: ItemService = Depends(get_service)):
    svc.delete_item(item_id)
