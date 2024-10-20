from sqlalchemy.orm import Session


from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
)


@router.post("/", response_model=schemas.Permission)
async def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_permission = models.Permission(user_id=current_user.id, event_id=permission.event_id, approver_id=permission.approver_id, permission_type=permission.permission_type, description=permission.description)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.get("/", response_model=List[schemas.Permission])
async def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    permissions = db.query(models.Permission).offset(skip).limit(limit).all()
    return permissions


@router.get("/{permission_id}", response_model=schemas.Permission)
async def read_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission



@router.post("/{permission_id}/approve", response_model=schemas.Permission)
async def approve_permission(permission_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    if current_user.id != permission.approver_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    permission.status = "approved"
    db.commit()
    db.refresh(permission)
    return permission


@router.post("/{permission_id}/reject", response_model=schemas.Permission)
async def reject_permission(permission_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    if current_user.id != permission.approver_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    permission.status = "rejected"
    db.commit()
    db.refresh(permission)
    return permission







