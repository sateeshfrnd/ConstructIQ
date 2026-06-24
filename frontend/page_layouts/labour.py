import streamlit as st
import pandas as pd
from datetime import datetime

from utils.constants import (
    CONSTRUCTION_STAGES,
    DATE_FORMAT,
    LABOUR_TYPE
)
from services.api_client import (
    add_labour_expenses_entry, get_labour_expenses_entry, get_labour_expenses_metrics)
from components.metric_cards import render_data_metrics_style3

def sample_data():
    return {
        "total_paid": 270000.0,
        "total_entries": 18,
        "type_breakdown": {
            "Steel Bending": 85000.0,
            "Civil": 120000.0,
            "Concrete Gang": 65000.0
        }
    }

def render_labour_type_metrics(data):
    """Render labour expenses breakdown vertically grouped by type."""
    type_breakdown = data.get("type_breakdown", {})
    with st.container(border=True):
        st.markdown("**👷 Expenses by Labour Type**")
        if type_breakdown:
            for labour_type, amount in type_breakdown.items():
                st.markdown(f"**{labour_type}**")
                st.metric("Cost", f"₹ {amount:,.0f}")
                st.divider()
        else:
            st.info("No labour expenses yet")


def render_labour_entry_form():
    with st.container(border=True):
        st.subheader("Add Labour Entry")

        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Payment Date", value='today', format=DATE_FORMAT)
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="construction_stage")
            labour_type = st.selectbox("Labour Type", LABOUR_TYPE)

        with col2:
            person = st.text_input("Paid To (Optional)")
            payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Bank Transfer"])
            amount = st.number_input("Payment Amount", min_value=0.0)

        description = st.text_area("Description / Reason")
        reference = st.text_input("Transaction Reference (Optional)")

        st.metric("Final Amount", f"₹{amount:,.0f}")

        if st.button("Add Labour Entry"):
            if not labour_type.strip():
                st.error("⚠️ labour type is required")
            else:
                labour_expenses_entry = {
                    "payment_date": str(date),
                    "construction_stage": construction_stage,
                    "labour_type": labour_type,
                    "paid_to": person,
                    "description": description,
                    "reference": reference,
                    "payment_amount": amount,
                    "payment_mode": payment_mode
                }
                st.write(labour_expenses_entry)
                add_labour_expenses_entry(labour_expenses_entry)


def render_expenses_history():
    data = get_labour_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "labour")


def render_labour():
    st.title("👷 Labour Management")
    st.write("Track and manage your labour costs effectively. Add new labour entries, view expense history, and gain insights into your labour expenses.")

    # Row 1: Overall summary across full width
    data = get_labour_expenses_metrics(params=None)
    summary_metrics = {
        "Total Paid": f"₹ {data['total_paid']:,.0f}",
        "Total Entries": f"{data['total_entries']}",
    }
    render_data_metrics_style3(dict_datametrics=summary_metrics)

    st.write("")

    # Side-by-side: Entry Form (left) | Type Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_labour_entry_form()

    with right_col:
        render_labour_type_metrics(data)

    st.divider()
    render_expenses_history()
