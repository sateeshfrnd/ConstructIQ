from sqlalchemy.orm import Session
from repositories.user_repo import get_user_by_email
from core.security import hash_password, verify_password, create_access_token
from models.user import User

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    print(user.__dict__)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    if not user:
        return None

    token = create_access_token({"sub": user.email})

    return token


def create_user(db: Session, email: str, password: str):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        raise Exception("User already exists")

    # Hash password
    hashed_password = hash_password(password)

    # Create user
    user = User(
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user