from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.bricks_expenses_schema import BricksExpenses
from services.bricks_expenses_service import (
    add_bricks_expenses_service, get_bricks_expenses_service, get_bricks_metrics)

router = APIRouter(prefix="/bricks_expenses", tags=["bricks_expenses"])

@router.post("/")
def add_bricks_expenses(
        request: BricksExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_site_expenses={request}')
    return add_bricks_expenses_service(db, request)


@router.get("/")
def get_bricks_expenses(
     db : Session = Depends(get_db)
):
    return get_bricks_expenses_service(db=db)

@router.get("/metrics")
def get_bricks_metrics_api(
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    stage: str = Query(default=None),
    vendor: str = Query(default=None),
    db: Session = Depends(get_db)
):
    return get_bricks_metrics(
        db=db, start_date=start_date, end_date=end_date,
        stage=stage, vendor=vendor
    )