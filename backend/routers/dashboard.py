from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db

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

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get overall project expense summary across all categories."""

    def safe_sum(model, amount_col, paid_col=None):
        total = db.query(
            func.coalesce(func.sum(amount_col), 0)
        ).scalar()
        paid = 0
        if paid_col is not None:
            paid = db.query(
                func.coalesce(func.sum(paid_col), 0)
            ).scalar()
        count = db.query(func.count(model.id)).scalar()
        return {
            "total_amount": float(total),
            "total_paid": float(paid),
            "entries": int(count)
        }

    categories = {
        "Cement": safe_sum(Cement_Expenses, Cement_Expenses.total_amount, Cement_Expenses.payment_amount),
        "Bricks": safe_sum(Bricks_Expenses, Bricks_Expenses.total_amount, Bricks_Expenses.payment_amount),
        "Steel": safe_sum(Steel_Expenses, Steel_Expenses.total_amount, Steel_Expenses.payment_amount),
        "Sand": safe_sum(Sand_Expenses, Sand_Expenses.total_amount, Sand_Expenses.payment_amount),
        "Stone": safe_sum(Stone_Expenses, Stone_Expenses.total_amount, Stone_Expenses.payment_amount),
        "Labour": safe_sum(Labour_Expenses, Labour_Expenses.payment_amount),
        "Electric": safe_sum(Electric_Expenses, Electric_Expenses.amount),
        "Plumbing": safe_sum(Plumbing_Expenses, Plumbing_Expenses.amount),
        "Painting": safe_sum(Painting_Expenses, Painting_Expenses.amount),
        "Site Expenses": safe_sum(Site_Expenses, Site_Expenses.amount),
    }

    grand_total = sum(c["total_amount"] for c in categories.values())
    total_paid = sum(c["total_paid"] for c in categories.values())
    total_entries = sum(c["entries"] for c in categories.values())

    # Stage-wise breakdown (using cement as sample, but aggregate all)
    stage_data = {}
    stage_models = [
        (Cement_Expenses, Cement_Expenses.construction_stage, Cement_Expenses.total_amount),
        (Bricks_Expenses, Bricks_Expenses.construction_stage, Bricks_Expenses.total_amount),
        (Steel_Expenses, Steel_Expenses.construction_stage, Steel_Expenses.total_amount),
        (Sand_Expenses, Sand_Expenses.construction_stage, Sand_Expenses.total_amount),
        (Stone_Expenses, Stone_Expenses.construction_stage, Stone_Expenses.total_amount),
        (Labour_Expenses, Labour_Expenses.construction_stage, Labour_Expenses.payment_amount),
        (Electric_Expenses, Electric_Expenses.construction_stage, Electric_Expenses.amount),
        (Plumbing_Expenses, Plumbing_Expenses.construction_stage, Plumbing_Expenses.amount),
        (Painting_Expenses, Painting_Expenses.construction_stage, Painting_Expenses.amount),
        (Site_Expenses, Site_Expenses.construction_stage, Site_Expenses.amount),
    ]

    for model, stage_col, amount_col in stage_models:
        results = db.query(
            stage_col,
            func.coalesce(func.sum(amount_col), 0).label("amount")
        ).group_by(stage_col).all()
        for r in results:
            if r[0]:
                stage_data[r[0]] = stage_data.get(r[0], 0) + float(r[1])

    # Payment mode breakdown
    payment_modes = {}
    payment_models = [
        (Cement_Expenses, Cement_Expenses.payment_mode, Cement_Expenses.payment_amount),
        (Bricks_Expenses, Bricks_Expenses.payment_mode, Bricks_Expenses.payment_amount),
        (Steel_Expenses, Steel_Expenses.payment_mode, Steel_Expenses.payment_amount),
        (Sand_Expenses, Sand_Expenses.payment_mode, Sand_Expenses.payment_amount),
        (Stone_Expenses, Stone_Expenses.payment_mode, Stone_Expenses.payment_amount),
        (Labour_Expenses, Labour_Expenses.payment_mode, Labour_Expenses.payment_amount),
        (Electric_Expenses, Electric_Expenses.payment_mode, Electric_Expenses.amount),
        (Plumbing_Expenses, Plumbing_Expenses.payment_mode, Plumbing_Expenses.amount),
        (Painting_Expenses, Painting_Expenses.mode, Painting_Expenses.amount),
        (Site_Expenses, Site_Expenses.payment_mode, Site_Expenses.amount),
    ]

    for model, mode_col, amount_col in payment_models:
        results = db.query(
            mode_col,
            func.coalesce(func.sum(amount_col), 0).label("amount")
        ).group_by(mode_col).all()
        for r in results:
            if r[0]:
                payment_modes[r[0]] = payment_modes.get(r[0], 0) + float(r[1])

    return {
        "grand_total": grand_total,
        "total_paid": total_paid,
        "outstanding": grand_total - total_paid,
        "total_entries": total_entries,
        "categories": categories,
        "stage_breakdown": stage_data,
        "payment_modes": payment_modes,
    }
