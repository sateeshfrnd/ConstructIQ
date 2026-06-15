import streamlit as st
from datetime import date
import pandas as pd

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    PAINTING_CATEGORY
)
from services.api_client import (
    add_painting_expenses_entry,get_painting_expenses_entry)

def render_painting_entry_form():
    with st.form("painting_form", clear_on_submit=True):
        st.subheader("Add Painting Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category",PAINTING_CATEGORY)
            construction_stage = st.selectbox("🏗️ Construnction Stage",CONSTRUCTION_STAGES)

        with col2:
            vendor = st.text_input("👷 Painter / Vendor")
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description")
        submitted = st.form_submit_button("✅ Save Expense")
        if submitted:
            if amount == 0:
                st.error("Amount cannot be zero")
                return None
            painting_expense_entry={
                "expense_date": str(expense_date),
                "category": category,
                "construction_stage": construction_stage,
                "vendor": vendor,
                "amount": amount,
                "mode": mode,
                "description": description
                }
            st.write(painting_expense_entry)
            add_painting_expenses_entry(painting_expense_entry)

def render_expenses_history():
    st.subheader("Expense History") 
    data = get_painting_expenses_entry()
    if data:
        df = pd.DataFrame(data=data)
        st.dataframe(data=df, use_container_width=True,  hide_index=True)
    else:
        st.info("No expenses added yet.")

def render_painting_expenses():
    st.title("🎨 Painting Expenses")
    st.caption(
        "Track and manage painting expenses during construction. "
        "Record costs for paints, materials, labor, and finishing work."
    )
    
    # Add Labour Entry Form
    render_painting_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
    render_expenses_history()
