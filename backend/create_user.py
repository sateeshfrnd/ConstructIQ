# create_user.py

from database.db import SessionLocal
from models.user import User
from passlib.context import CryptContext


def create_admin_user():
    db = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        existing = db.query(User).filter(User.email == "admin@example.com").first()
        if existing:
            print(f"Admin user already exists: id={existing.id} email={existing.email}")
            return

        user = User(
            name="admin710",
            email="admin@example.com",
            hashed_password=pwd_context.hash("admin710"),
            role="admin"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created admin user id={user.id} email={user.email}")
    except Exception as e:
        print("Error creating admin user:", e)
    finally:
        db.close()

def get_user():
    db = SessionLocal()
    for u in db.query(User).all():
        print(u.id, u.email, u.name, u.role)
    db.close()

if __name__ == "__main__":
    create_admin_user()
    # get_user()