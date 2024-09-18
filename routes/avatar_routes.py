from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.avatar_schemas import AvatarCreate
from services.avatar_service import create_avatar
from utils.utils import get_db

router = APIRouter()

@router.post("/create-avatar/")
def create_new_avatar(avatar: AvatarCreate, db: Session = Depends(get_db)):
    if not avatar.height or not avatar.weight or not avatar.gender:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    return create_avatar(db, avatar)
