from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserProfileBase(BaseModel):
    name: str
    age: Optional[int]
    income: Optional[float]
    location: Optional[str]
    language_preference: Optional[str] = "English"
    savings: Optional[float]

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
