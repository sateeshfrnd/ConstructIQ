from models.stone_expenses import Stone_Expenses
from sqlalchemy import func

def add_stone_expenses_service(db, request):
    print(f'Service:add_sand_expenses_service = {request}')
    new_expense = Stone_Expenses(
        delivery_date = request.delivery_date,
        construction_stage = request.construction_stage,
        vendor_name = request.vendor_name,    
        stone_type = request.stone_type,    
        cost_per_trucks = request.cost_per_truck,
        num_of_trucks = request.no_of_trucks,
        driver_amount = request.driver_amount,
        total_amount= request.total_amount,
        payment_amount = request.payment_amount,
        payment_mode = request.payment_mode,
        payment_date = request.payment_date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

def get_stone_expenses_service(db):
    return db.query(Stone_Expenses).all()

def get_stone_metrics(db, start_date=None, end_date=None, stage=None, vendor=None):
    query = db.query(
        func.coalesce(func.sum(Stone_Expenses.total_amount), 0).label("total_spend"),
        func.coalesce(func.sum(Stone_Expenses.num_of_trucks), 0).label("total_trucks"),
        func.coalesce(func.sum(Stone_Expenses.payment_amount), 0).label("total_paid"),
        func.coalesce(
            func.sum(Stone_Expenses.total_amount - func.coalesce(Stone_Expenses.payment_amount, 0)),
            0
        ).label("outstanding_amount")
    )

    if start_date:
        query = query.filter(Stone_Expenses.delivery_date >= start_date)
    if end_date:
        query = query.filter(Stone_Expenses.delivery_date <= end_date)
    if stage and stage != "All":
        query = query.filter(Stone_Expenses.construction_stage == stage)
    if vendor:
        query = query.filter(Stone_Expenses.vendor_name.ilike(f"%{vendor}%"))

    result = query.one()

    # Breakdown by stone type (loads and cost per type)
    type_query = db.query(
        Stone_Expenses.stone_type,
        func.coalesce(func.sum(Stone_Expenses.num_of_trucks), 0).label("loads"),
        func.coalesce(func.sum(Stone_Expenses.total_amount), 0).label("cost")
    )
    if start_date:
        type_query = type_query.filter(Stone_Expenses.delivery_date >= start_date)
    if end_date:
        type_query = type_query.filter(Stone_Expenses.delivery_date <= end_date)
    if stage and stage != "All":
        type_query = type_query.filter(Stone_Expenses.construction_stage == stage)
    if vendor:
        type_query = type_query.filter(Stone_Expenses.vendor_name.ilike(f"%{vendor}%"))

    type_results = type_query.group_by(Stone_Expenses.stone_type).all()
    type_breakdown = {
        r.stone_type: {"loads": int(r.loads), "cost": float(r.cost)}
        for r in type_results if r.stone_type
    }

    return {
        "total_spend": float(result.total_spend),
        "total_trucks": int(result.total_trucks),
        "total_paid": float(result.total_paid),
        "outstanding_amount": float(result.outstanding_amount),
        "type_breakdown": type_breakdown
    }