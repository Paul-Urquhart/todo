from .db import Base
from sqlalchemy import Column, Integer, Boolean, String, Date

class Todo(Base):
    __tablename__ = "todo_list"
    __table_args__ = {"schema": "todo_db"}
        
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    done = Column(Boolean)
    due_date = Column(Date)
