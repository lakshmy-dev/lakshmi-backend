from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    title = Column(String, nullable=False)  # e.g., "Retirement at 60", "Buy iPhone on EMI"
    description = Column(String, nullable=True)
    type = Column(String, nullable=False)  # e.g., "retirement", "purchase", "goal", etc.

    inputs = Column(JSON, nullable=True)  # user assumptions for the scenario
    projections = Column(JSON, nullable=True)  # financial outputs (e.g., corpus, timeline, cost diff)
    gpt_summary = Column(Text, nullable=True)  # ✅ NEW: GPT summary field

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserProfile", back_populates="scenarios")
