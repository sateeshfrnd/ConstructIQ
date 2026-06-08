from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.auth import LoginRequest, TokenResponse
from services.auth_service import create_user

router = APIRouter(prefix="/signup", tags=["signup"])


class SignupRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(db, request.email, request.password)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))