import streamlit as st
from datetime import date
import pandas as pd

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    MISCELLANEOUS_EXPENSE_CATEGORIES
)

from services.api_client import (
    add_site_expenses_entry, get_site_expenses_entry, get_site_expenses_metrics)
from components.metric_cards import render_data_metrics_style3

def get_sample_data():
    return {
            "total_spend": 169500.0,
            "total_entries": 14,
            "category_breakdown": {
                "Architect Fee": {"entries": 3, "cost": 45000.0},
                "Excavation": {"entries": 2, "cost": 32000.0},
                "Readymix Concrete": {"entries": 4, "cost": 80000.0},
                "Miscellaneous": {"entries": 5, "cost": 12500.0}
            }
        }


def render_site_category_metrics(data):
    """Render site expenses breakdown vertically grouped by category."""
    category_breakdown = data.get("category_breakdown", {})
    with st.container(border=True):
        st.markdown("**� Expenses by Category**")
        if category_breakdown:
            for category, info in category_breakdown.items():
                st.markdown(f"**{category}**")
                col_a, col_b = st.columns(2)
                col_a.metric("Entries", f"{info['entries']}")
                col_b.metric("Cost", f"₹ {info['cost']:,.0f}")
                st.divider()
        else:
            st.info("No site expenses yet")


def render_site_entry_form():
    with st.form("site_form", clear_on_submit=True):
        st.subheader("Add Site Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Expense Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category", list(MISCELLANEOUS_EXPENSE_CATEGORIES.keys()))
            stage = st.selectbox("🏗️ Construction Stage", CONSTRUCTION_STAGES)

        with col2:
            expense_type = st.selectbox("📌 Type", MISCELLANEOUS_EXPENSE_CATEGORIES[category])
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description", placeholder="Enter details about the expense...")
        notes = st.text_input("📎 Notes (Optional)", placeholder="Any extra info...")
        submitted = st.form_submit_button("✅ Save Expense")
        if submitted:
            if amount <= 0:
                st.error("⚠️ Amount must be greater than 0")
                return None
            elif not description.strip():
                st.error("⚠️ Description is required")
            else:
                site_expenses_entry = {
                    "expenses_date": str(expense_date),
                    "expense_category": category,
                    "construction_stage": stage,
                    "expense_type": expense_type,
                    "amount": amount,
                    "payment_mode": mode,
                    "description": description,
                    "notes": notes
                }
                add_site_expenses_entry(site_expenses_entry)
                return site_expenses_entry

    return None


def render_expenses_history():
    data = get_site_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "site_expenses")


def render_site_expenses():
    st.title("📦 Site Expenses")
    st.caption("Track all your construction-related miscellaneous and setup expenses in one place.")

    # Row 1: Overall summary across full width
    data = get_site_expenses_metrics(params=None)
    summary_metrics = {
        "Total Spend": f"₹ {data['total_spend']:,.0f}",
        "Total Entries": f"{data['total_entries']}",
    }
    render_data_metrics_style3(dict_datametrics=summary_metrics)

    st.write("")

    # Side-by-side: Entry Form (left) | Category Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_site_entry_form()

    with right_col:
        render_site_category_metrics(data)

    st.divider()
    render_expenses_history()
