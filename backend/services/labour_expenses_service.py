from models.labour_expenses import Labour_Expenses

def add_labour_expenses_service(db, request):
    print(f'Service:add_labour_expenses_service = {request}')
    new_expense = Labour_Expenses(
        payment_date = request.payment_date,
        construction_stage = request.construction_stage,
        labour_type = request.labour_type,
        paid_to = request.paid_to,
        payment_mode = request.payment_mode,
        payment_amount = request.payment_amount,
        description = request.description,
        reference= request.reference
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense




