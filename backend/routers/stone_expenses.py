from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.stone_expenses_schema import StoneExpenses
from services.stone_expenses_service import add_stone_expenses_service

router = APIRouter(prefix="/stone_expenses", tags=["stone_expenses"])

@router.post("/")
def add_stone_expenses(
        request: StoneExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_stone_expenses={request}')
    return add_stone_expenses_service(db, request)
