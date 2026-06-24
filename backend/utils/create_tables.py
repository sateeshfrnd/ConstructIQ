from database.db import engine, Base

# 👇 IMPORTANT: import all models so SQLAlchemy knows them
from models.user import User  

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")