from models.bricks_expenses import Bricks_Expenses

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
