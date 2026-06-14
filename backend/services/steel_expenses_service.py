from models.steel_expenses import Steel_Expenses

def add_steel_expenses_service(db, request):
    print(f'Service:add_steel_expenses_service = {request}')
    new_expense = Steel_Expenses(
        delivery_date = request.delivery_date,
        construction_stage = request.construction_stage,
        vendor_name = request.vendor_name,
        steel_type = request.steel_type,
        size = request.size,
        num_bundles = request.num_bundles,
        price_per_bundle = request.price_per_bundle,
        total_weight= request.total_weight,
        driver_amount = request.driver_amount,
        total_amount = request.total_amount,
        payment_amount = request.payment_amount,
        payment_mode = request.payment_mode,
        payment_date = request.payment_date
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense
