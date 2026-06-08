# create_user.py

from database.db import SessionLocal
from models.user import User
from passlib.context import CryptContext

db = SessionLocal() 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user = User(
    name="admin710",
    email="admin@example.com",
    hashed_password=pwd_context.hash("admin710"),
    role="admin"
)

db.add(user)
db.commit()
db.close()