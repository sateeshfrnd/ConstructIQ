import streamlit as st
from datetime import date

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    MISCELLANEOUS_EXPENSE_CATEGORIES
)

def render_site_entry_form():
    with st.form("site_form", clear_on_submit=True):
        st.subheader("Add Site Expenses")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Expense Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category",list(MISCELLANEOUS_EXPENSE_CATEGORIES.keys()))
            stage = st.selectbox("🏗️ Construnction Stage",CONSTRUCTION_STAGES)

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
                return {
                    "date": str(expense_date),
                    "category": category,
                    "stage": stage,
                    "type": expense_type,
                    "amount": amount,
                    "mode": mode,
                    "description": description,
                    "notes": notes
                }

    return None


def render_site_expenses():
    st.title("📦 Site Expenses Entry ")
    st.caption("Track all your construction-related miscellaneous and setup expenses in one place.")
    
    # Add Labour Entry Form
    render_site_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
    st.subheader("Expense History") 
    st.info("No site expense data available")

