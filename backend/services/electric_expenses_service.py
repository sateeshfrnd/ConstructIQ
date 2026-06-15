from models.electric_expenses import Electric_Expenses

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




