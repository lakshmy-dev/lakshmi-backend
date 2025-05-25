from pydantic import BaseModel
from datetime import datetime

class UserInputCreate(BaseModel):
    user_message: str
    assistant_response: str
    timestamp: datetime
