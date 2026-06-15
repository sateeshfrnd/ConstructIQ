from models.plumbing_expenses import Plumbing_Expenses

def add_plumbing_expenses_service(db, request):
    print(f'Service:add_plumbing_expenses_service = {request}')
    new_expense = Plumbing_Expenses(
        expense_date = request.expense_date,
        category=request.category,
        construction_stage = request.construction_stage,
        vendor = request.vendor,
        amount = request.amount,
        payment_mode = request.payment_mode,
        description = request.description,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense




