from sqlalchemy import text
from database import SessionLocal

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))
    print("✅ Database connection successful!")
except Exception as e:
    print("❌ Database connection failed:")
    print(e)
finally:
    db.close()
