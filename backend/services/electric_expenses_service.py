from models.electric_expenses import Electric_Expenses
from sqlalchemy import func

def add_electric_expenses_service(db, request):
    print(f'Service:add_electric_expenses_service = {request}')
    new_expense = Electric_Expenses(
        expense_date = request.expense_date,
        construction_stage = request.construction_stage,
        vendor = request.vendor,
        category=request.category,
        payment_mode = request.payment_mode,
        amount = request.amount,
        description = request.description,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def get_electric_expenses_service(db):
    return db.query(Electric_Expenses).all()

def get_electric_metrics(db, start_date=None, end_date=None, stage=None, category=None):
    query = db.query(
        func.coalesce(func.sum(Electric_Expenses.amount), 0).label("total_spend"),
        func.count(Electric_Expenses.id).label("total_entries"),
    )

    if start_date:
        query = query.filter(Electric_Expenses.expense_date >= start_date)
    if end_date:
        query = query.filter(Electric_Expenses.expense_date <= end_date)
    if stage and stage != "All":
        query = query.filter(Electric_Expenses.construction_stage == stage)
    if category and category != "All":
        query = query.filter(Electric_Expenses.category == category)

    result = query.one()

    # Get breakdown by category
    cat_query = db.query(
        Electric_Expenses.category,
        func.coalesce(func.sum(Electric_Expenses.amount), 0).label("amount")
    )
    if start_date:
        cat_query = cat_query.filter(Electric_Expenses.expense_date >= start_date)
    if end_date:
        cat_query = cat_query.filter(Electric_Expenses.expense_date <= end_date)
    if stage and stage != "All":
        cat_query = cat_query.filter(Electric_Expenses.construction_stage == stage)

    cat_results = cat_query.group_by(Electric_Expenses.category).all()
    category_breakdown = {r.category: float(r.amount) for r in cat_results}

    return {
        "total_spend": float(result.total_spend),
        "total_entries": int(result.total_entries),
        "category_breakdown": category_breakdown
    }




