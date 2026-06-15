from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.labour_expenses_schema import LabourExpenses
from services.labour_expenses_service import add_labour_expenses_service

router = APIRouter(prefix="/labour_expenses", tags=["labour_expenses"])

@router.post("/")
def add_labour_expenses(
        request: LabourExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_labour_expenses={request}')
    return add_labour_expenses_service(db, request)
