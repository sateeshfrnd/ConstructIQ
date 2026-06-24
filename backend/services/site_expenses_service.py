from models.site_expenses import Site_Expenses
from sqlalchemy import func

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


def get_site_metrics(db, start_date=None, end_date=None, stage=None, category=None):
    # Base filters helper
    def apply_filters(q):
        if start_date:
            q = q.filter(Site_Expenses.expenses_date >= start_date)
        if end_date:
            q = q.filter(Site_Expenses.expenses_date <= end_date)
        if stage and stage != "All":
            q = q.filter(Site_Expenses.construction_stage == stage)
        if category and category != "All":
            q = q.filter(Site_Expenses.expense_category == category)
        return q

    # Overall totals
    overall_query = apply_filters(db.query(
        func.coalesce(func.sum(Site_Expenses.amount), 0).label("total_spend"),
        func.count(Site_Expenses.id).label("total_entries"),
    ))
    overall = overall_query.one()

    # Breakdown by category
    cat_query = apply_filters(db.query(
        Site_Expenses.expense_category,
        func.count(Site_Expenses.id).label("entries"),
        func.coalesce(func.sum(Site_Expenses.amount), 0).label("cost")
    ))
    cat_results = cat_query.group_by(Site_Expenses.expense_category).all()
    category_breakdown = {
        r.expense_category: {"entries": int(r.entries), "cost": float(r.cost)}
        for r in cat_results if r.expense_category
    }

    return {
        "total_spend": float(overall.total_spend),
        "total_entries": int(overall.total_entries),
        "category_breakdown": category_breakdown
    }
