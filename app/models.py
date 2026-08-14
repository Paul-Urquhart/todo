from .db import Base
from sqlalchemy import Column, Integer, Boolean, String, Date, ForeignKey

class Todo(Base):
    __tablename__ = "todo_list"
        
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    done = Column(Boolean)
    due_date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # NULLABLE temporarily

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
