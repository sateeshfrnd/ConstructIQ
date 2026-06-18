from models.cement_expenses import Cement_Expenses
from sqlalchemy import func

def add_cement_expenses_service(db, request):
    print(f'Service:add_steel_expenses_service = {request}')
    new_expense = Cement_Expenses(
        delivery_date = request.delivery_date,
        construction_stage = request.construction_stage,
        vendor_name = request.vendor_name,
        cement_company_name = request.cement_company_name,
        price_per_bag = request.price_per_bag,
        no_of_bags = request.no_of_bags,
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

def get_cement_expenses_service(db):
    return db.query(Cement_Expenses).all()

def get_cement_metrics(db, start_date=None, end_date=None, stage=None, vendor=None):
    query = db.query(
        func.coalesce(func.sum(Cement_Expenses.total_amount), 0).label("total_spend"),
        func.coalesce(func.sum(Cement_Expenses.no_of_bags), 0).label("total_purchased"),
        func.coalesce(func.sum(Cement_Expenses.payment_amount), 0).label("total_paid"),
        func.coalesce(
            func.sum(Cement_Expenses.total_amount - func.coalesce(Cement_Expenses.payment_amount, 0)), 
            0
        ).label("outstanding_amount")
    )

    if start_date:
        query = query.filter(Cement_Expenses.delivery_date >= start_date)

    if end_date:
        query = query.filter(Cement_Expenses.delivery_date <= end_date)

    if stage and stage != "All":
        query = query.filter(Cement_Expenses.construction_stage == stage)

    if vendor:
        query = query.filter(Cement_Expenses.vendor_name.ilike(f"%{vendor}%"))

    result = query.one()

    return {
        "total_spend": float(result.total_spend),
        "total_purchased": int(result.total_purchased),
        "total_paid": float(result.total_paid),
        "outstanding_amount": float(result.outstanding_amount)
    }