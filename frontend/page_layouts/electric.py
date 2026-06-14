import streamlit as st
from datetime import date

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    ELECTRIC_CATEGORY
)

def render_electric_entry_form():
    with st.form("electric_form", clear_on_submit=True):
        st.subheader("Add Electric Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category",ELECTRIC_CATEGORY)
            stage = st.selectbox("🏗️ Construnction Stage",CONSTRUCTION_STAGES)

        with col2:
            vendor = st.text_input("👷 Vendor / Electrician")
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description")
        submitted = st.form_submit_button("✅ Save Expense")
        if submitted:
            if amount == 0:
                st.error("Amount cannot be zero")
                return None
            return {
                "date": str(expense_date),
                "category": category,
                "stage": stage,
                "vendor": vendor,
                "amount": amount,
                "mode": mode,
                "description": description
            }

    return None


def render_electric_expenses():
    st.title("⚡ Electric Expenses")
    st.write("Track electrical costs during construction—from wiring and fittings to temporary power and labor—with clear visibility into your expenses.")  
   
    # Add Labour Entry Form
    render_electric_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
    st.subheader("Expense History") 
    st.info("No records yet ")

