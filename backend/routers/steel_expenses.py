from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.steel_expenses_schema import SteelExpenses
from services.steel_expenses_service import (
    add_steel_expenses_service,
    get_steel_expenses_service,
    get_steel_metrics,
)

router = APIRouter(prefix="/steel_expenses", tags=["steel_expenses"])

@router.post("/")
def add_steel_expenses(
        request: SteelExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_steel_expenses={request}')
    return add_steel_expenses_service(db, request)

@router.get("/")
def get_steel_expenses(
     db : Session = Depends(get_db)
):
    return get_steel_expenses_service(db=db)

@router.get("/metrics")
def get_steel_metrics_api(
    start_date: str = None,
    end_date: str = None,
    stage: str = None,
    vendor: str = None,
    db: Session = Depends(get_db)
):
    return get_steel_metrics(
        db=db,
        start_date=start_date,
        end_date=end_date,
        stage=stage,
        vendor=vendor,
    )