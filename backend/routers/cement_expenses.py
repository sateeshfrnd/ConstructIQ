from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.cement_expenses_schema import CementExpenses
from services.cement_expenses_service import (
    add_cement_expenses_service,
    get_cement_expenses_service,
    get_cement_metrics
)

router = APIRouter(prefix="/cement_expenses", tags=["cement_expenses"])

@router.post("/")
def add_steel_expenses(
        request: CementExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_cement_expenses={request}')
    return add_cement_expenses_service(db, request)

@router.get("/")
def get_cement_expenses(
     db : Session = Depends(get_db)
):
    return get_cement_expenses_service(db=db)

@router.get("/metrics")
def get_cement_metrics_api(
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    stage: str = Query(default=None),
    vendor: str = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_cement_metrics(
        db=db,
        start_date=start_date,
        end_date=end_date,
        stage=stage,
        vendor=vendor
    )

