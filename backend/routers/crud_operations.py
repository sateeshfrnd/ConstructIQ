from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from typing import Dict, Any

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

router = APIRouter(prefix="/entries", tags=["crud"])

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


@router.put("/{category}/{entry_id}")
def update_entry(
    category: str,
    entry_id: int,
    updates: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update a single entry by category and ID."""
    if category not in CATEGORY_MODEL_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    model = CATEGORY_MODEL_MAP[category]
    entry = db.query(model).filter(model.id == entry_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")

    # Update only provided fields
    for key, value in updates.items():
        if key == "id":
            continue
        if hasattr(entry, key):
            setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return {"message": f"Entry {entry_id} updated successfully"}


@router.delete("/{category}/{entry_id}")
def delete_entry(
    category: str,
    entry_id: int,
    db: Session = Depends(get_db)
):
    """Delete a single entry by category and ID."""
    if category not in CATEGORY_MODEL_MAP:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

    model = CATEGORY_MODEL_MAP[category]
    entry = db.query(model).filter(model.id == entry_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail=f"Entry {entry_id} not found")

    db.delete(entry)
    db.commit()
    return {"message": f"Entry {entry_id} deleted successfully"}
