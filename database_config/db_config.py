import os
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Database setup
DATABASE_URL =  os.getenv("database_url")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# SQLAlchemy base model
Base = declarative_base()
 
# Database Instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()