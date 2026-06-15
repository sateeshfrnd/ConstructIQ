import streamlit as st
import pandas as pd
from datetime import date

from utils.constants import (
    DATE_FORMAT,
    CONSTRUCTION_STAGES,
    PAYMENT_MODES,
    ELECTRIC_CATEGORY
)
from services.api_client import add_electric_expenses_entry,get_electric_expenses_entry

def render_electric_entry_form():
    # with st.form("electric_form", clear_on_submit=True):
    with st.container(border=True):
        st.subheader("Add Electric Expense")

        col1, col2 = st.columns(2)

        with col1:
            expense_date = st.date_input("📅 Date", value=date.today(), format=DATE_FORMAT)
            category = st.selectbox("⚡ Category",ELECTRIC_CATEGORY)
            construction_stage = st.selectbox("🏗️ Construnction Stage",CONSTRUCTION_STAGES)

        with col2:
            vendor = st.text_input("👷 Vendor / Electrician")
            amount = st.number_input("💰 Amount", min_value=0, step=500)
            payment_mode = st.selectbox("💳 Payment Mode", PAYMENT_MODES)

        description = st.text_area("📝 Description")
        
        if st.button("Add electric Entry"):
            if not category.strip():
                st.error("⚠️ category is required")
            elif amount == 0:
                st.error("Amount cannot be zero")
                return None
            else :
                electric_expenses_entry={
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
    st.subheader("Expense History") 
    data = get_electric_expenses_entry()
    if data:
        df = pd.DataFrame(data=data)
        st.dataframe(data=df, use_container_width=True,  hide_index=True)
    else:
        st.info("No expenses added yet.")

             
   

def render_electric_expenses():
    st.title("⚡ Electric Expenses")
    st.write("Track electrical costs during construction—from wiring and fittings to temporary power and labor—with clear visibility into your expenses.")  
   
    # Add Labour Entry Form
    render_electric_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
   
    render_expenses_history()
