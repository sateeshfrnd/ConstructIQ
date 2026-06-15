import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

from utils.constants import (
    CONSTRUCTION_STAGES,
    DATE_FORMAT,
    LABOUR_TYPE
)
from services.api_client import add_labour_expenses_entry

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
            payment_mode = st.selectbox(
                "Payment Mode",
                ["Cash", "UPI", "Bank Transfer"]
            )
            amount = st.number_input("Payment Amount", min_value=0.0)

        description = st.text_area("Description / Reason")

        reference = st.text_input("Transaction Reference (Optional)")

        # st.text_input("Final Amount", value=f"₹ {amount:,.0f}", disabled=True)
        st.metric("Final Amount ", f"₹{amount:,.0f}")  

        if st.button("Add Labour Entry"):
            if not labour_type.strip():
                st.error("⚠️ labour type is required")
            
            else:
                labour_expenses_entry ={
                    "payment_date":str(date),
                    "construction_stage":construction_stage,
                    "labour_type":labour_type,
                    "paid_to":person,
                    "description":description,
                    "reference":reference,
                    "payment_amount":amount,
                    "payment_mode":payment_mode
                }
                st.write(labour_expenses_entry)
                add_labour_expenses_entry(labour_expenses_entry)



def render_labour():
    st.title("👷 Labour Management")
    st.write("Track and manage your labour costs effectively. Add new labour entries, view expense history, and gain insights into your labour expenses.")  
   
    # Add Labour Entry Form
    render_labour_entry_form()

    st.divider()
    # Expense history table (placeholder for now)
    st.subheader("Expense History") 
    st.info("No records yet ")
