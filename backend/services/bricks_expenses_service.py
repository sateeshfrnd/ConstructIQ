from models.bricks_expenses import Bricks_Expenses
from sqlalchemy import func

def add_bricks_expenses_service(db, request):
    print(f'Service:add_bricks_expenses_service = {request}')
    new_expense = Bricks_Expenses(
        purchase_date = request.purchase_date,
        construction_stage = request.construction_stage,
        vendor_name = request.vendor_name,
        quantity = request.quantity,
        price_per_brick = request.price_per_brick,
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

def get_bricks_expenses_service(db):
    return db.query(Bricks_Expenses).all()

def get_bricks_metrics(db, start_date=None, end_date=None, stage=None, vendor=None):
    query = db.query(
        func.coalesce(func.sum(Bricks_Expenses.total_amount), 0).label("total_spend"),
        func.coalesce(func.sum(Bricks_Expenses.quantity), 0).label("total_purchased"),
        func.coalesce(func.sum(Bricks_Expenses.payment_amount), 0).label("total_paid"),
        func.coalesce(
            func.sum(Bricks_Expenses.total_amount - func.coalesce(Bricks_Expenses.payment_amount, 0)),
            0
        ).label("outstanding_amount")
    )

    if start_date:
        query = query.filter(Bricks_Expenses.purchase_date >= start_date)
    if end_date:
        query = query.filter(Bricks_Expenses.purchase_date <= end_date)
    if stage and stage != "All":
        query = query.filter(Bricks_Expenses.construction_stage == stage)
    if vendor:
        query = query.filter(Bricks_Expenses.vendor_name.ilike(f"%{vendor}%"))

    result = query.one()

    # Breakdown by brick size (quantity and cost per size)
    size_query = db.query(
        Bricks_Expenses.brick_size,
        func.coalesce(func.sum(Bricks_Expenses.quantity), 0).label("quantity"),
        func.coalesce(func.sum(Bricks_Expenses.total_amount), 0).label("cost")
    )
    if start_date:
        size_query = size_query.filter(Bricks_Expenses.purchase_date >= start_date)
    if end_date:
        size_query = size_query.filter(Bricks_Expenses.purchase_date <= end_date)
    if stage and stage != "All":
        size_query = size_query.filter(Bricks_Expenses.construction_stage == stage)
    if vendor:
        size_query = size_query.filter(Bricks_Expenses.vendor_name.ilike(f"%{vendor}%"))

    size_results = size_query.group_by(Bricks_Expenses.brick_size).all()
    size_breakdown = {
        r.brick_size: {"quantity": int(r.quantity), "cost": float(r.cost)}
        for r in size_results if r.brick_size
    }

    return {
        "total_spend": float(result.total_spend),
        "total_purchased": int(result.total_purchased),
        "total_paid": float(result.total_paid),
        "outstanding_amount": float(result.outstanding_amount),
        "size_breakdown": size_breakdown
    }
