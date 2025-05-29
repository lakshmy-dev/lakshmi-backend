import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../lib')))
from app.services.gpt_service import GPTService

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.scenario import Scenario as ScenarioModel
from app.models.user_profile import UserProfile as UserProfileModel
from app.schemas.scenario import Scenario, ScenarioCreate
from app.logic.scenario_engine import goal_retirement
from app.utils.lakshmi_prompt_builder import build_lakshmi_prompt

router = APIRouter(prefix="/scenarios", tags=["Scenarios"])

@router.post("/", response_model=Scenario)
def create_scenario(scenario: ScenarioCreate, db: Session = Depends(get_db)):
    data = scenario.dict()
    inputs = data.get("inputs", {})
    user_id = data.get("user_id")

    # ✅ Pull user tags for tone + personalization
    tags = {}
    user = db.query(UserProfileModel).filter(UserProfileModel.id == user_id).first()
    if user:
        tags = {
            "risk_appetite": getattr(user, "risk_appetite", "Moderate Risk-Taker"),
            "goal_orientation": getattr(user, "goal_orientation", "Long-Term Builder"),
            "savings_habit": getattr(user, "savings_habit", "Regular Saver"),
            "financial_dependency": getattr(user, "financial_dependency", "Self-Supported"),
            "tone_preference": getattr(user, "tone_preference", "Straightforward"),
        }

    # ✅ Logic engine for retirement
    if data.get("type") == "goal_retirement":
        projections = goal_retirement(inputs, tags)
        data["projections"] = projections

        # 🧠 Pull values with fallback
        age = inputs.get("current_age", 30)
        retirement_age = inputs.get("retirement_age", 60)
        current_savings = inputs.get("current_savings", 0)
        monthly_savings = inputs.get("monthly_savings", 10000)
        expected_corpus = inputs.get("expected_corpus", 10000000)

        # 🧾 Construct enriched message for GPT with assumptions
        enriched_message = (
            f"I'm currently {age} and plan to retire by {retirement_age}. "
            f"I have ₹{current_savings:,} saved and save ₹{monthly_savings:,} monthly. "
            f"My target retirement corpus is ₹{expected_corpus:,}. "
            "If you're using any assumptions, let me know so I can update them. "
            "Can you summarize how I'm doing and what I could improve?"
        )

        # 🧠 GPT summary using Lakshmi prompt layer
        try:
            prompt_data = build_lakshmi_prompt(
                messages=[{
                    "role": "user",
                    "content": enriched_message,
                }],
                tags=tags,
                emotions={},  # Add later if available
                user_name="You",
                scenario_type=data.get("type"),
                inputs=inputs
            )

            gpt = GPTService()
            summary = gpt.generate(prompt_data)
            data["gpt_summary"] = summary
        except Exception as e:
            print("GPT Summary Error:", e)
            data["gpt_summary"] = "Summary unavailable due to internal error."

    # ✅ Save scenario
    db_scenario = ScenarioModel(**data)
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario

@router.get("/{scenario_id}", response_model=Scenario)
def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    scenario = db.query(ScenarioModel).filter(ScenarioModel.id == scenario_id).first()
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario
