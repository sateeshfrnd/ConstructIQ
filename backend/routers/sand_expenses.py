from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.sand_expenses_schema import SandExpenses
from services.sand_expenses_service import add_sand_expenses_service

router = APIRouter(prefix="/sand_expenses", tags=["sand_expenses"])

@router.post("/")
def add_send_expenses(
        request: SandExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_sand_expenses={request}')
    return add_sand_expenses_service(db, request)
