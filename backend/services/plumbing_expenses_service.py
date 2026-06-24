from models.plumbing_expenses import Plumbing_Expenses
from sqlalchemy import func

def add_plumbing_expenses_service(db, request):
    print(f'Service:add_plumbing_expenses_service = {request}')
    new_expense = Plumbing_Expenses(
        expense_date = request.expense_date,
        category=request.category,
        construction_stage = request.construction_stage,
        vendor = request.vendor,
        amount = request.amount,
        payment_mode = request.payment_mode,
        description = request.description,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


def get_plumbing_expenses_service(db):
    return db.query(Plumbing_Expenses).all()

def get_plumbing_metrics(db, start_date=None, end_date=None, stage=None, category=None):
    query = db.query(
        func.coalesce(func.sum(Plumbing_Expenses.amount), 0).label("total_spend"),
        func.count(Plumbing_Expenses.id).label("total_entries"),
    )

    if start_date:
        query = query.filter(Plumbing_Expenses.expense_date >= start_date)
    if end_date:
        query = query.filter(Plumbing_Expenses.expense_date <= end_date)
    if stage and stage != "All":
        query = query.filter(Plumbing_Expenses.construction_stage == stage)
    if category and category != "All":
        query = query.filter(Plumbing_Expenses.category == category)

    result = query.one()

    # Get breakdown by category
    cat_query = db.query(
        Plumbing_Expenses.category,
        func.coalesce(func.sum(Plumbing_Expenses.amount), 0).label("amount")
    )
    if start_date:
        cat_query = cat_query.filter(Plumbing_Expenses.expense_date >= start_date)
    if end_date:
        cat_query = cat_query.filter(Plumbing_Expenses.expense_date <= end_date)
    if stage and stage != "All":
        cat_query = cat_query.filter(Plumbing_Expenses.construction_stage == stage)

    cat_results = cat_query.group_by(Plumbing_Expenses.category).all()
    category_breakdown = {r.category: float(r.amount) for r in cat_results}

    return {
        "total_spend": float(result.total_spend),
        "total_entries": int(result.total_entries),
        "category_breakdown": category_breakdown
    }

