import os
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

# Database setup
DATABASE_URL =  os.getenv("database_url")
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocomit=False,autoflush=False,bind=engine)

# SQLAlchemy base model
Base = declarative_base()