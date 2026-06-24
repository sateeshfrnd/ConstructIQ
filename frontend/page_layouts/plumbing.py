import streamlit as st
from datetime import date 
import pandas as pd

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    PLUMBING_CATEGORY
)
from services.api_client import (
    add_plumbing_expenses_entry, get_plumbing_expenses_entry, get_plumbing_expenses_metrics)
from components.metric_cards import render_data_metrics_style3

def sample_data():
    return {
        "total_spend": 103000.0,
        "total_entries": 12,
        "category_breakdown": {
            "Pipes": 28000.0,
            "Fittings": 15000.0,
            "Sanitary": 42000.0,
            "Labor": 18000.0
        }
    }

def render_plumbing_category_metrics(data):
    """Render plumbing expenses breakdown vertically grouped by category."""
    category_breakdown = data.get("category_breakdown", {})
    with st.container(border=True):
        st.markdown("**🔧 Expenses by Category**")
        if category_breakdown:
            for category, amount in category_breakdown.items():
                st.markdown(f"**{category}**")
                st.metric("Cost", f"₹ {amount:,.0f}")
                st.divider()
        else:
            st.info("No plumbing expenses yet")


def render_plumbing_entry_form():
    with st.form("plumbing_form", clear_on_submit=True):
        st.subheader("Add Plumbing Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category", PLUMBING_CATEGORY)
            construction_stage = st.selectbox("🏗️ Construction Stage", CONSTRUCTION_STAGES)

        with col2:
            vendor = st.text_input("👷 Plumber / Vendor")
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description")
        submitted = st.form_submit_button("✅ Save Expense")
        if submitted:
            if amount == 0:
                st.error("Amount cannot be zero")
                return None
            plumbing_expenses_entry = {
                "expense_date": str(expense_date),
                "category": category,
                "construction_stage": construction_stage,
                "vendor": vendor,
                "amount": amount,
                "payment_mode": mode,
                "description": description
            }
            st.write(plumbing_expenses_entry)
            add_plumbing_expenses_entry(plumbing_expenses_entry)


def render_expenses_history():
    data = get_plumbing_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "plumbing")


def render_plumbing_expenses():
    st.title("🚿 Plumbing Expenses")
    st.caption(
        "Track and manage plumbing expenses during construction. "
        "Record costs for pipes, fittings, sanitary items, and labor."
    )

    # Row 1: Overall summary across full width
    data = get_plumbing_expenses_metrics(params=None)
    summary_metrics = {
        "Total Spend": f"₹ {data['total_spend']:,.0f}",
        "Total Entries": f"{data['total_entries']}",
    }
    render_data_metrics_style3(dict_datametrics=summary_metrics)

    st.write("")

    # Side-by-side: Entry Form (left) | Category Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_plumbing_entry_form()

    with right_col:
        render_plumbing_category_metrics(data)

    st.divider()
    render_expenses_history()
