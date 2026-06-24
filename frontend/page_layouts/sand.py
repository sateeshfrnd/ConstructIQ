import streamlit as st 
import pandas as pd
from datetime import date

from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_SAND_VENDOR,
    SAND_TYPES_COST,
    DATE_FORMAT
)
from services.api_client import (
    add_sand_expenses_entry, get_sand_expenses_entry, get_sand_expenses_metrics)
from components.metric_cards import render_data_metrics_style3

def sample_data():
    return {
        "total_spend": 139500.0,
        "total_trucks": 8,
        "total_paid": 120000.0,
        "outstanding_amount": 19500.0,
        "type_breakdown": {
            "DOUBLE_WASHED": {"loads": 5, "cost": 90000.0},
            "SINGLE_WASHED": {"loads": 3, "cost": 49500.0}
        }
    }
    


def render_sand_type_metrics(data):
    """Render sand type breakdown vertically grouped by category."""
    type_breakdown = data.get("type_breakdown", {})
    with st.container(border=True):
        st.markdown("**🏖️ Sand (by Type)**")
        if type_breakdown:
            for sand_type, info in type_breakdown.items():
                st.markdown(f"**{sand_type}**")
                col_a, col_b = st.columns(2)
                col_a.metric("Loads", f"{info['loads']}")
                col_b.metric("Cost", f"₹ {info['cost']:,.0f}")
                st.divider()
        else:
            st.info("No sand purchases yet")


def render_add_sand_entry_form():
    with st.container(border=True):
        st.subheader("Add Sand Purchase")
        col1, col2 = st.columns(2)
        with col1:
            delivery_date = st.date_input("Date", key="sand_date", value=date.today(), format=DATE_FORMAT)
            sand_type = st.selectbox("Sand Type", list(SAND_TYPES_COST.keys()))
            cost_per_truck = st.number_input(
                "Cost Per Truck",
                value=SAND_TYPES_COST[sand_type],
            )
            driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True, key="sand_driver_payment")

        with col2:
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="sand_construction_stage")
            no_of_trucks = st.number_input("Number of Trucks", min_value=0.0, key="sand_no_of_trucks", step=1.0)
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_SAND_VENDOR, key="sand_vendor_name")
            if driver_payment == "Yes":
                driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
            else:
                driver_amount = st.number_input("Driver Amount", value=0, disabled=True)

        # Total Amount Calculation
        total_amount = (no_of_trucks * cost_per_truck) + driver_amount
        st.metric("Total Amount", f"₹{total_amount:,.2f}")

        col6, col7 = st.columns(2)
        with col6:
            paid_date = st.date_input("Payment Date", key="paid_date", value=date.today(), format=DATE_FORMAT)
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Bank Transfer", "UPI"], key="sand_payment_mode")
        with col7:
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)

        if st.button("Add Sand Entry"):
            if not sand_type.strip():
                st.error("⚠️ sand type is required")
            elif not vendor_name.strip():
                st.error("⚠️ Vendor name is required")
            elif no_of_trucks <= 0:
                st.error("⚠️ number of trucks must be greater than 0")
            else:
                sand_entry = {
                    "delivery_date": str(delivery_date),
                    "construction_stage": construction_stage,
                    "sand_type": sand_type,
                    "vendor_name": vendor_name,
                    "cost_per_truck": cost_per_truck,
                    "no_of_trucks": int(no_of_trucks),
                    "driver_amount": driver_amount,
                    "total_amount": total_amount,
                    "payment_date": str(paid_date),
                    "payment_amount": payment_amount,
                    "payment_mode": payment_mode,
                }
                st.write(sand_entry)
                add_sand_expenses_entry(sand_entry)


def render_expenses_history():
    data = get_sand_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "sand")


def render_sand():
    st.title("Sand Management")
    st.write("Track and manage your sand usage seamlessly. Record deliveries, monitor consumption, and ensure optimal material availability for construction.")

    # Row 1: Overall summary across full width
    data = get_sand_expenses_metrics(params=None)
    summary_metrics = {
        "Total Spend": f"₹ {data['total_spend']:,.0f}",
        "Total Loads": f"{data['total_trucks']}",
        "Total Paid": f"₹ {data['total_paid']:,.0f}",
        "Outstanding": f"₹ {data['outstanding_amount']:,.0f}"
    }
    render_data_metrics_style3(dict_datametrics=summary_metrics)

    st.write("")

    # Side-by-side: Entry Form (left) | Type Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_add_sand_entry_form()

    with right_col:
        render_sand_type_metrics(data)

    st.divider()
    render_expenses_history()
