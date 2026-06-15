from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.electric_expenses_schema import ElectricExpenses
from services.electric_expenses_service import (
    add_electric_expenses_service,
    get_electric_expenses_service
)

router = APIRouter(prefix="/electric_expenses", tags=["electric_expenses"])

@router.post("/")
def add_electric_expenses(
        request: ElectricExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_electric_expenses={request}')
    return add_electric_expenses_service(db, request)

@router.get("/")
def get_electric_expenses(
     db : Session = Depends(get_db)
):
    return get_electric_expenses_service(db=db)