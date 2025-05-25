from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class UserInput(Base):
    __tablename__ = "user_inputs"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    assistant_response = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
