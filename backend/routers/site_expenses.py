from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.site_expenses_schema import SiteExpenses
from services.site_expenses_service import add_site_expenses_service

router = APIRouter(prefix="/site_expenses", tags=["site_expenses"])

@router.post("/")
def add_site_expenses(
        request: SiteExpenses,
        db : Session = Depends(get_db)
):
    print(f'Router:add_site_expenses={request}')
    return add_site_expenses_service(db, request)
