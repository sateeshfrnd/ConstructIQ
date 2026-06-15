import streamlit as st
from datetime import date 
import pandas as pd

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    PLUMBING_CATEGORY
)
from services.api_client import add_plumbing_expenses_entry,get_plumbing_expenses_entry  
def render_plumbing_entry_form():
    with st.form("plumbing_form", clear_on_submit=True):
        st.subheader("Add Plumbing Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category",PLUMBING_CATEGORY)
            construction_stage = st.selectbox("🏗️ Construnction Stage",CONSTRUCTION_STAGES)

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
        st.subheader("Expense History") 
        data = get_plumbing_expenses_entry()
        if data:
            df = pd.DataFrame(data=data)
            st.dataframe(data=df, use_container_width=True,  hide_index=True)
        else:
            st.info("No expenses added yet.") 

def render_plumbing_expenses():
    st.title("🚿 Plumbing Expenses")
    st.caption(
        "Track and manage plumbing expenses during construction. "
      "Record costs for pipes, fittings, sanitary items, and labor."
    )
    
    # Add Labour Entry Form
    render_plumbing_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
    render_expenses_history()

