from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class UserInput(Base):
    __tablename__ = "user_inputs"  # ✅ Table name

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)  # 🛠️ Add this
    assistant_response = Column(String, nullable=False)  # 🛠️ Add this
    timestamp = Column(DateTime, default=datetime.utcnow)
