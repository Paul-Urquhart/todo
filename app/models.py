from .db import Base
from sqlalchemy import Column, Integer, Boolean, String

class Todo(Base):
    __tablename__ = "todo_list"
        
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    done = Column(Boolean)

todos = []
for word in "hello world from my todo app".split():
    hello = Todo(task=word, done=False)
    todos.append(hello)

for blah in todos:
    print(blah.task, end=" ")
print()