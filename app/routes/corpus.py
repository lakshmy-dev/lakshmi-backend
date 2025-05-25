import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../lib")))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from middle_layer.corpus_engine import calculate_corpus

router = APIRouter()

class Goal(BaseModel):
    name: str
    cost: float
    year: int
    include: Optional[bool] = True

class IncomeStream(BaseModel):
    name: str
    amount: float
    start_year: int
    end_year: int

class CorpusRequest(BaseModel):
    current_age: int
    retirement_age: int
    life_expectancy: int
    monthly_contribution: float
    expected_return: float
    post_retirement_return: float
    inflation_rate: float
    lifestyle_multiplier: Optional[float] = 1.0
    current_year: Optional[int] = 2025
    retirement_monthly_income: Optional[float] = None
    goals: List[Goal]
    income_streams: Optional[List[IncomeStream]] = []

@router.post("/project")
def get_corpus_projection(data: CorpusRequest):
    try:
        input_dict = data.dict()
        result = calculate_corpus(input_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
