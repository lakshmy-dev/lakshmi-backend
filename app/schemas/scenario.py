from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class ScenarioBase(BaseModel):
    title: str
    description: Optional[str]
    type: str
    inputs: Optional[Dict] = {}
    projections: Optional[Dict] = {}
    gpt_summary: Optional[str] = None  # ✅ Added here

class ScenarioCreate(ScenarioBase):
    user_id: int

class Scenario(ScenarioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # ✅ Good for Pydantic v1
