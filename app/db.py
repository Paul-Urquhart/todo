from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DB_CONNECTION_STRING = f"postgresql://todo_user:{DATABASE_PASSWORD}@{DATABASE_HOST}:5432/todo_db"

os.getenv("DB_CONNECTION_STRING")

engine = create_engine(
    DB_CONNECTION_STRING
)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass