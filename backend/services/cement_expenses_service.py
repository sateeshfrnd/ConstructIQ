from models.cement_expenses import Cement_Expenses

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
