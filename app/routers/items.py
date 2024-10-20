from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.oauth2 import get_current_user
from app.utils import get_password_hash

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("/", response_model=schemas.InventoryItem)
async def create_item(item: schemas.InventoryItemCreate, db: Session = Depends(get_db)):
    db_item = models.InventoryItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[schemas.InventoryItem])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(models.InventoryItem).offset(skip).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=schemas.InventoryItem)
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/{item_id}/request", response_model=schemas.InventoryRequest)
async def request_item(item_id: int, request: schemas.InventoryRequestCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.quantity_ <= request.quantity_requested:
        raise HTTPException(status_code=400, detail="Item is out of stock")
    db_request = models.InventoryRequest(**request.dict(), item_id=item_id, requester_id=current_user.id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/{item_id}/requests", response_model=List[schemas.InventoryRequest])
async def read_requests(item_id: int, db: Session = Depends(get_db)):
    requests = db.query(models.InventoryRequest).filter(models.InventoryRequest.item_id == item_id).all()

    return requests


@router.post("/{item_id}/restock", response_model=schemas.InventoryItem)
async def restock_item(item_id: int, quantity: int, db: Session = Depends(get_db)):
    db_item = db.query(models.InventoryItem).filter(models.InventoryItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.quantity_ += quantity
    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/{item_id}/{request_id}/approve", response_model=schemas.InventoryRequest)
async def approve_request(item_id: int, request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.InventoryRequest).filter(models.InventoryRequest.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db_request.status = 'approved'
    db.commit()
    db.refresh(db_request)
    return db_request


@router.post("/{item_id}/{request_id}/reject", response_model=schemas.InventoryRequest)
async def reject_request(item_id: int, request_id: int, db: Session = Depends(get_db)):
    db_request = db.query(models.InventoryRequest).filter(models.InventoryRequest.id == request_id).first()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db_request.status = 'rejected'
    db.commit()
    db.refresh(db_request)
    return db_request



