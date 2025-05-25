from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_profile import UserProfile as UserProfileModel
from app.schemas.user_profile import UserProfile, UserProfileCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserProfile)
def create_user(user: UserProfileCreate, db: Session = Depends(get_db)):
    db_user = UserProfileModel(**user.dict())  # ✅ use model, not schema
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserProfile)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
