from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.cement_expenses_schema import CementExpenses
from services.cement_expenses_service import add_cement_expenses_service

router = APIRouter(prefix="/cement_expenses", tags=["cement_expenses"])

@router.post("/")
def add_steel_expenses(
        request: CementExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_site_expenses={request}')
    return add_cement_expenses_service(db, request)
