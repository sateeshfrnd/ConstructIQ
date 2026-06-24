from models.sand_expenses import Sand_Expenses
from sqlalchemy import func

def add_sand_expenses_service(db, request):
    print(f'Service:add_sand_expenses_service = {request}')
    new_expense = Sand_Expenses(
        delivery_date = request.delivery_date,
        construction_stage = request.construction_stage,
        vendor_name = request.vendor_name,        
        sand_type = request.sand_type,
        cost_per_truck = request.cost_per_truck,
        no_of_trucks = request.no_of_trucks,
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

def get_sand_expenses_service(db):
    return db.query(Sand_Expenses).all()

def get_sand_metrics(db, start_date=None, end_date=None, stage=None, vendor=None):
    # Base filters helper
    def apply_filters(q):
        if start_date:
            q = q.filter(Sand_Expenses.delivery_date >= start_date)
        if end_date:
            q = q.filter(Sand_Expenses.delivery_date <= end_date)
        if stage and stage != "All":
            q = q.filter(Sand_Expenses.construction_stage == stage)
        if vendor:
            q = q.filter(Sand_Expenses.vendor_name.ilike(f"%{vendor}%"))
        return q

    # Overall totals
    query = apply_filters(db.query(
        func.coalesce(func.sum(Sand_Expenses.total_amount), 0).label("total_spend"),
        func.coalesce(func.sum(Sand_Expenses.no_of_trucks), 0).label("total_trucks"),
        func.coalesce(func.sum(Sand_Expenses.payment_amount), 0).label("total_paid"),
        func.coalesce(
            func.sum(Sand_Expenses.total_amount - func.coalesce(Sand_Expenses.payment_amount, 0)),
            0
        ).label("outstanding_amount")
    ))
    result = query.one()

    # Breakdown by sand type (loads and cost per type)
    type_query = apply_filters(db.query(
        Sand_Expenses.sand_type,
        func.coalesce(func.sum(Sand_Expenses.no_of_trucks), 0).label("loads"),
        func.coalesce(func.sum(Sand_Expenses.total_amount), 0).label("cost")
    ))
    type_results = type_query.group_by(Sand_Expenses.sand_type).all()
    type_breakdown = {
        r.sand_type: {"loads": int(r.loads), "cost": float(r.cost)}
        for r in type_results if r.sand_type
    }

    return {
        "total_spend": float(result.total_spend),
        "total_trucks": int(result.total_trucks),
        "total_paid": float(result.total_paid),
        "outstanding_amount": float(result.outstanding_amount),
        "type_breakdown": type_breakdown
    }