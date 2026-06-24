from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.civil_contract_schema import (
    CivilContractCreate, CivilContractPayment,
    CivilContractStage, CivilContractStagesList
)
from services.civil_contract_service import (
    create_contract, get_contracts, get_contract_by_id,
    add_payment, get_payments, save_stages, get_stages,
    get_contract_summary
)

router = APIRouter(prefix="/civil_contract", tags=["civil_contract"])


@router.post("/")
def create_civil_contract(
    request: CivilContractCreate,
    db: Session = Depends(get_db)
):
    return create_contract(db, request)


@router.get("/")
def list_contracts(db: Session = Depends(get_db)):
    return get_contracts(db)


@router.get("/{contract_id}")
def get_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract


@router.post("/payments")
def add_contract_payment(
    request: CivilContractPayment,
    db: Session = Depends(get_db)
):
    return add_payment(db, request)


@router.get("/{contract_id}/payments")
def get_contract_payments(contract_id: int, db: Session = Depends(get_db)):
    return get_payments(db, contract_id)


@router.post("/{contract_id}/stages")
def save_contract_stages(
    contract_id: int,
    request: CivilContractStagesList,
    db: Session = Depends(get_db)
):
    return save_stages(db, contract_id, request.stages)


@router.get("/{contract_id}/stages")
def get_contract_stages(contract_id: int, db: Session = Depends(get_db)):
    return get_stages(db, contract_id)


@router.get("/{contract_id}/summary")
def get_contract_summary_api(contract_id: int, db: Session = Depends(get_db)):
    summary = get_contract_summary(db, contract_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Contract not found")
    return summary
