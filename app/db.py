from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

engine = create_engine(
    DB_CONNECTION_STRING
)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass