# File: app/semantic_api.py

import sys
import os

# ✅ Add the lib folder to Python path (relative to /app/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Dict

# ✅ Clean import from lib/middle_layer
from app.middle_layer.semantic_matcher import find_best_tag

router = APIRouter()

class SemanticInput(BaseModel):
    user_input: str
    top_k: int = 5  # default value

@router.post("/semantic/match")
async def match_semantic_tags(payload: SemanticInput):
    try:
        result = find_best_tag(payload.user_input, top_k=payload.top_k, debug=True)
        print("🧪 RETURNING FROM ROUTE:", result)  # ← ADD THIS LINE
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()  # 👈 this will give us full trace
        raise HTTPException(status_code=500, detail=str(e))

