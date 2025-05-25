from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import database
from models.user_input import UserInput
from schemas.user_input import UserInputCreate
from semantic_api import router as semantic_router
from routes import user_profile, scenario, corpus
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(semantic_router)
app.include_router(user_profile.router)
app.include_router(scenario.router)
app.include_router(corpus.router, prefix="/api/corpus", tags=["Corpus Engine"])

@app.post("/save_input/")
def save_input(user_input: UserInputCreate, db: Session = Depends(get_db)):
    db_input = UserInput(
        user_message=user_input.user_message,
        assistant_response=user_input.assistant_response,
        timestamp=user_input.timestamp,
    )
    db.add(db_input)
    db.commit()
    db.refresh(db_input)
    return {"message": "Input saved successfully!", "id": db_input.id}

@app.get("/get_inputs/")
def get_inputs(db: Session = Depends(get_db)):
    inputs = db.query(UserInput).all()
    return inputs

@app.get("/ping")
def ping():
    return {"status": "Backend is reachable"}
