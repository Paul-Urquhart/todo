from app.db import Base, engine
from app.models import Todo

Base.metadata.create_all(engine)

print("Database created.")