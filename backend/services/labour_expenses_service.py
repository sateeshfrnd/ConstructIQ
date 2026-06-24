from models.labour_expenses import Labour_Expenses
from sqlalchemy import func

def add_labour_expenses_service(db, request):
    print(f'Service:add_labour_expenses_service = {request}')
    new_expense = Labour_Expenses(
        payment_date = request.payment_date,
        construction_stage = request.construction_stage,
        labour_type = request.labour_type,
        paid_to = request.paid_to,
        payment_mode = request.payment_mode,
        payment_amount = request.payment_amount,
        description = request.description,
        reference= request.reference
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def get_labour_expenses_service(db):
    return db.query(Labour_Expenses).all()

def get_labour_metrics(db, start_date=None, end_date=None, stage=None, labour_type=None):
    query = db.query(
        func.coalesce(func.sum(Labour_Expenses.payment_amount), 0).label("total_paid"),
        func.count(Labour_Expenses.id).label("total_entries"),
    )

    if start_date:
        query = query.filter(Labour_Expenses.payment_date >= start_date)
    if end_date:
        query = query.filter(Labour_Expenses.payment_date <= end_date)
    if stage and stage != "All":
        query = query.filter(Labour_Expenses.construction_stage == stage)
    if labour_type and labour_type != "All":
        query = query.filter(Labour_Expenses.labour_type == labour_type)

    result = query.one()

    # Get breakdown by labour type
    type_query = db.query(
        Labour_Expenses.labour_type,
        func.coalesce(func.sum(Labour_Expenses.payment_amount), 0).label("amount")
    )
    if start_date:
        type_query = type_query.filter(Labour_Expenses.payment_date >= start_date)
    if end_date:
        type_query = type_query.filter(Labour_Expenses.payment_date <= end_date)
    if stage and stage != "All":
        type_query = type_query.filter(Labour_Expenses.construction_stage == stage)

    type_results = type_query.group_by(Labour_Expenses.labour_type).all()
    type_breakdown = {r.labour_type: float(r.amount) for r in type_results}

    return {
        "total_paid": float(result.total_paid),
        "total_entries": int(result.total_entries),
        "type_breakdown": type_breakdown
    }






