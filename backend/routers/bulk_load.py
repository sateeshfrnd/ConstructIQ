from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from typing import List, Dict, Any

from models.cement_expenses import Cement_Expenses
from models.bricks_expenses import Bricks_Expenses
from models.steel_expenses import Steel_Expenses
from models.sand_expenses import Sand_Expenses
from models.stone_expenses import Stone_Expenses
from models.labour_expenses import Labour_Expenses
from models.electric_expenses import Electric_Expenses
from models.plumbing_expenses import Plumbing_Expenses
from models.painting_expenses import Painting_Expenses
from models.site_expenses import Site_Expenses

router = APIRouter(prefix="/bulk_load", tags=["bulk_load"])

# Expected columns per category
CATEGORY_SCHEMA = {
    "cement": [
        "delivery_date", "construction_stage", "vendor_name",
        "cement_company_name", "price_per_bag", "no_of_bags",
        "driver_amount", "total_amount", "payment_amount",
        "payment_mode", "payment_date"
    ],
    "bricks": [
        "purchase_date", "construction_stage", "vendor_name",
        "brick_size", "quantity", "price_per_brick",
        "driver_amount", "total_amount", "payment_amount",
        "payment_mode", "payment_date"
    ],
    "steel": [
        "delivery_date", "construction_stage", "vendor_name",
        "steel_type", "size", "num_bundles", "price_per_bundle",
        "total_weight", "driver_amount", "total_amount",
        "payment_amount", "payment_mode", "payment_date"
    ],
    "sand": [
        "delivery_date", "construction_stage", "sand_type",
        "vendor_name", "cost_per_truck", "no_of_trucks",
        "driver_amount", "total_amount", "payment_amount",
        "payment_mode", "payment_date"
    ],
    "stone": [
        "delivery_date", "construction_stage", "vendor_name",
        "stone_type", "cost_per_truck", "no_of_trucks",
        "driver_amount", "total_amount", "payment_amount",
        "payment_mode", "payment_date"
    ],
    "labour": [
        "payment_date", "construction_stage", "labour_type",
        "paid_to", "description", "reference",
        "payment_amount", "payment_mode"
    ],
    "electric": [
        "expense_date", "construction_stage", "category",
        "vendor", "amount", "payment_mode", "description"
    ],
    "plumbing": [
        "expense_date", "category", "construction_stage",
        "vendor", "amount", "payment_mode", "description"
    ],
    "painting": [
        "expense_date", "category", "construction_stage",
        "vendor", "amount", "mode", "description"
    ],
    "site_expenses": [
        "expenses_date", "expense_type", "expense_category",
        "amount", "construction_stage", "payment_mode",
        "description", "notes"
    ],
}

CATEGORY_MODEL_MAP = {
    "cement": Cement_Expenses,
    "bricks": Bricks_Expenses,
    "steel": Steel_Expenses,
    "sand": Sand_Expenses,
    "stone": Stone_Expenses,
    "labour": Labour_Expenses,
    "electric": Electric_Expenses,
    "plumbing": Plumbing_Expenses,
    "painting": Painting_Expenses,
    "site_expenses": Site_Expenses,
}


@router.get("/schema/{category}")
def get_category_schema(category: str):
    """Return expected columns for a category."""
    if category not in CATEGORY_SCHEMA:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    return {"category": category, "columns": CATEGORY_SCHEMA[category]}


@router.post("/{category}")
def bulk_load_data(
    category: str,
    records: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Bulk insert records for a given category."""
    if category not in CATEGORY_SCHEMA:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    expected_columns = set(CATEGORY_SCHEMA[category])
    model_class = CATEGORY_MODEL_MAP[category]

    # Validate all records have the expected columns
    errors = []
    for i, record in enumerate(records):
        record_cols = set(record.keys())
        missing = expected_columns - record_cols
        extra = record_cols - expected_columns
        if missing:
            errors.append(f"Row {i+1}: missing columns {missing}")
        if extra:
            errors.append(f"Row {i+1}: unexpected columns {extra}")

    if errors:
        raise HTTPException(status_code=422, detail=errors)

    # Insert all records
    inserted = 0
    try:
        for record in records:
            # Filter only expected columns
            filtered = {k: v for k, v in record.items() if k in expected_columns}
            obj = model_class(**filtered)
            db.add(obj)
            inserted += 1
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": f"Successfully loaded {inserted} records into {category}"}
