from models.steel_expenses import Steel_Expenses
from sqlalchemy import func

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

def get_steel_expenses_service(db):
    return db.query(Steel_Expenses).all()

def get_steel_metrics(db, start_date=None, end_date=None, stage=None, vendor=None):
    # Base filters
    def apply_filters(q):
        if start_date:
            q = q.filter(Steel_Expenses.delivery_date >= start_date)
        if end_date:
            q = q.filter(Steel_Expenses.delivery_date <= end_date)
        if stage and stage != "All":
            q = q.filter(Steel_Expenses.construction_stage == stage)
        if vendor:
            q = q.filter(Steel_Expenses.vendor_name.ilike(f"%{vendor}%"))
        return q

    # Overall totals
    overall_query = apply_filters(db.query(
        func.coalesce(func.sum(Steel_Expenses.total_amount), 0).label("total_spend"),
        func.coalesce(func.sum(Steel_Expenses.payment_amount), 0).label("total_paid"),
        func.coalesce(
            func.sum(Steel_Expenses.total_amount - func.coalesce(Steel_Expenses.payment_amount, 0)),
            0
        ).label("outstanding_amount")
    ))
    overall = overall_query.one()

    # Binding Wire totals (steel_type = 'BINDING_WIRE')
    wire_query = apply_filters(db.query(
        func.coalesce(func.sum(Steel_Expenses.num_bundles), 0).label("bundles"),
        func.coalesce(func.sum(Steel_Expenses.total_amount), 0).label("cost")
    ).filter(Steel_Expenses.steel_type == "BINDING_WIRE"))
    wire = wire_query.one()

    # Steel breakdown by size (steel_type = 'STEEL')
    size_query = apply_filters(db.query(
        Steel_Expenses.size,
        func.coalesce(func.sum(Steel_Expenses.num_bundles), 0).label("bundles"),
        func.coalesce(func.sum(Steel_Expenses.total_weight), 0).label("weight"),
        func.coalesce(func.sum(Steel_Expenses.total_amount), 0).label("cost")
    ).filter(Steel_Expenses.steel_type == "STEEL"))
    size_results = size_query.group_by(Steel_Expenses.size).all()

    steel_size_breakdown = {
        r.size: {
            "bundles": int(r.bundles), 
            # "weight": float(r.weight), 
            "cost": float(r.cost)
            }
        for r in size_results if r.size
    }

    # Steel totals for avg cost/kg
    steel_totals_query = apply_filters(db.query(
        func.coalesce(func.sum(Steel_Expenses.total_weight), 0).label("total_weight"),
        func.coalesce(func.sum(Steel_Expenses.total_amount), 0).label("total_cost")
    ).filter(Steel_Expenses.steel_type == "STEEL"))
    steel_totals = steel_totals_query.one()
    avg_cost_per_kg = (
        float(steel_totals.total_cost) / float(steel_totals.total_weight)
        if float(steel_totals.total_weight) > 0 else 0.0
    )

    return {
        "total_spend": float(overall.total_spend),
        "total_paid": float(overall.total_paid),
        "outstanding_amount": float(overall.outstanding_amount),
        "binding_wire": {
            "bundles": int(wire.bundles),
            "cost": float(wire.cost)
        },
        "steel_size_breakdown": steel_size_breakdown,
        "avg_cost_per_kg": round(avg_cost_per_kg, 2)
    }