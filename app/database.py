import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Load .env variables
load_dotenv()

# ✅ Read DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Fallback or fail-safe error if not set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set. Check your .env file.")

# ✅ Create engine + session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

from app import models

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
