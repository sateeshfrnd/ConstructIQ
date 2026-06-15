from models.site_expenses import Site_Expenses

def add_site_expenses_service(db, request):
    print(f'Service:add_site_expenses_service = {request}')
    new_expense = Site_Expenses(
        expenses_date=request.expenses_date,
        expense_type=request.expense_type,
        expense_category=request.expense_category,
        amount=request.amount,
        construction_stage=request.construction_stage,
        payment_mode=request.payment_mode,
        description=request.description,
        notes=request.notes
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


def get_site_expenses_service(db):
    return db.query(Site_Expenses).all()
