from models.sand_expenses import Sand_Expenses

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