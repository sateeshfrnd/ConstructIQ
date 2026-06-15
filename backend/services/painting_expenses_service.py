from models.painting_expenses import Painting_Expenses

def add_painting_expenses_service(db, request):
    print(f'Service:add_painting_expenses_service = {request}')
    new_expense = Painting_Expenses(
        expense_date = request.expense_date,
        category=request.category,
        construction_stage = request.construction_stage,
        vendor = request.vendor,
        mode = request.mode,
        amount = request.amount,
        description = request.description,
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense




