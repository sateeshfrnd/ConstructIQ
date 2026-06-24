from models.civil_contract import Civil_Contract, Civil_Contract_Payments, Civil_Contract_Stages
from sqlalchemy.orm import Session
from sqlalchemy import func


def create_contract(db: Session, request):
    contract = Civil_Contract(
        vendor_name=request.vendor_name,
        total_sqft=request.total_sqft,
        rate_per_chadara=request.rate_per_chadara,
        no_of_floors=request.no_of_floors,
        total_chadaras=request.total_chadaras,
        total_contract_cost=request.total_contract_cost,
        milestone_percentage=request.milestone_percentage,
        no_of_partitions=request.no_of_partitions,
        cost_per_partition=request.cost_per_partition,
        notes=request.notes
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_contracts(db: Session):
    return db.query(Civil_Contract).all()


def get_contract_by_id(db: Session, contract_id: int):
    return db.query(Civil_Contract).filter(Civil_Contract.id == contract_id).first()


def add_payment(db: Session, request):
    payment = Civil_Contract_Payments(
        contract_id=request.contract_id,
        payment_date=request.payment_date,
        construction_stage=request.construction_stage,
        description=request.description,
        payment_mode=request.payment_mode,
        amount_paid=request.amount_paid
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payments(db: Session, contract_id: int):
    return db.query(Civil_Contract_Payments).filter(
        Civil_Contract_Payments.contract_id == contract_id
    ).all()


def save_stages(db: Session, contract_id: int, stages):
    # Delete existing stages for this contract
    db.query(Civil_Contract_Stages).filter(
        Civil_Contract_Stages.contract_id == contract_id
    ).delete()
    db.commit()

    # Insert new stages
    for stage in stages:
        s = Civil_Contract_Stages(
            contract_id=contract_id,
            stage_name=stage.stage_name,
            stage_type=stage.stage_type,
            expected_amount=stage.expected_amount
        )
        db.add(s)
    db.commit()
    return {"message": f"Saved {len(stages)} stages"}


def get_stages(db: Session, contract_id: int):
    return db.query(Civil_Contract_Stages).filter(
        Civil_Contract_Stages.contract_id == contract_id
    ).all()


def get_contract_summary(db: Session, contract_id: int):
    """Get contract with payment summary and stage-wise actual vs expected."""
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    # Total paid
    total_paid = db.query(
        func.coalesce(func.sum(Civil_Contract_Payments.amount_paid), 0)
    ).filter(Civil_Contract_Payments.contract_id == contract_id).scalar()

    # Stage-wise actual paid
    stage_payments = db.query(
        Civil_Contract_Payments.construction_stage,
        func.coalesce(func.sum(Civil_Contract_Payments.amount_paid), 0).label("actual_paid")
    ).filter(
        Civil_Contract_Payments.contract_id == contract_id
    ).group_by(Civil_Contract_Payments.construction_stage).all()

    stage_actual = {r.construction_stage: float(r.actual_paid) for r in stage_payments}

    # Expected stages
    stages = get_stages(db, contract_id)
    stage_comparison = []
    for s in stages:
        stage_comparison.append({
            "stage_name": s.stage_name,
            "stage_type": s.stage_type,
            "expected": s.expected_amount,
            "actual_paid": stage_actual.get(s.stage_name, 0)
        })

    return {
        "contract": {
            "id": contract.id,
            "vendor_name": contract.vendor_name,
            "total_sqft": contract.total_sqft,
            "rate_per_chadara": contract.rate_per_chadara,
            "no_of_floors": contract.no_of_floors,
            "total_chadaras": contract.total_chadaras,
            "total_contract_cost": contract.total_contract_cost,
            "milestone_percentage": contract.milestone_percentage,
            "no_of_partitions": contract.no_of_partitions,
            "cost_per_partition": contract.cost_per_partition,
        },
        "total_paid": float(total_paid),
        "balance": contract.total_contract_cost - float(total_paid),
        "payment_percentage": round((float(total_paid) / contract.total_contract_cost * 100), 1) if contract.total_contract_cost > 0 else 0,
        "stage_comparison": stage_comparison,
    }
