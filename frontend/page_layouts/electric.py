import streamlit as st
import pandas as pd
from datetime import date

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    ELECTRIC_CATEGORY
)
from services.api_client import (
    add_electric_expenses_entry, get_electric_expenses_entry, get_electric_expenses_metrics)
from components.metric_cards import render_data_metrics_style3


def sample_data():
    return {
        "total_spend": 63000.0,
        "total_entries": 10,
        "category_breakdown": {
            "Wiring": 22000.0,
            "Fittings": 18000.0,
            "Temporary EB": 8000.0,
            "Labor": 15000.0
        }
    }

def render_electric_category_metrics(data):
    """Render electric expenses breakdown vertically grouped by category."""
    category_breakdown = data.get("category_breakdown", {})
    with st.container(border=True):
        st.markdown("**⚡ Expenses by Category**")
        if category_breakdown:
            for category, amount in category_breakdown.items():
                st.markdown(f"**{category}**")
                st.metric("Cost", f"₹ {amount:,.0f}")
                st.divider()
        else:
            st.info("No electric expenses yet")


def render_electric_entry_form():
    with st.container(border=True):
        st.subheader("Add Electric Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category", ELECTRIC_CATEGORY)
            construction_stage = st.selectbox("🏗️ Construction Stage", CONSTRUCTION_STAGES)

        with col2:
            vendor = st.text_input("👷 Vendor / Electrician")
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            payment_mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description")

        if st.button("Add Electric Entry"):
            if not category.strip():
                st.error("⚠️ category is required")
            elif amount == 0:
                st.error("Amount cannot be zero")
                return None
            else:
                electric_expenses_entry = {
                    "expense_date": str(expense_date),
                    "category": category,
                    "construction_stage": construction_stage,
                    "vendor": vendor,
                    "amount": amount,
                    "payment_mode": payment_mode,
                    "description": description
                }
                st.write(electric_expenses_entry)
                add_electric_expenses_entry(electric_expenses_entry)


def render_expenses_history():
    data = get_electric_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "electric")


def render_electric_expenses():
    st.title("⚡ Electric Expenses")
    st.write("Track electrical costs during construction—from wiring and fittings to temporary power and labor—with clear visibility into your expenses.")

    # Row 1: Overall summary across full width
    data = get_electric_expenses_metrics(params=None)
    summary_metrics = {
        "Total Spend": f"₹ {data['total_spend']:,.0f}",
        "Total Entries": f"{data['total_entries']}",
    }
    render_data_metrics_style3(dict_datametrics=summary_metrics)

    st.write("")

    # Side-by-side: Entry Form (left) | Category Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_electric_entry_form()

    with right_col:
        render_electric_category_metrics(data)

    st.divider()
    render_expenses_history()
