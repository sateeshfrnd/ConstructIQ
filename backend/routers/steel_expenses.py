from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.steel_expenses_schema import SteelExpenses
from services.steel_expenses_service import add_steel_expenses_service

router = APIRouter(prefix="/steel_expenses", tags=["steel_expenses"])

@router.post("/")
def add_steel_expenses(
        request: SteelExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_steel_expenses={request}')
    return add_steel_expenses_service(db, request)
