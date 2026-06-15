import streamlit as st
from datetime import date
import pandas as pd
from utils.constants import (
    CONSTRUCTION_STAGES, 
    DEFAULT_CEMENT_VENDOR, 
    DEFAULT_CEMENT_COMPANY, 
    DEFAULT_CEMENT_COST_PER_BAG,
    DATE_FORMAT,
    PAYMENT_MODES
)
from services.api_client import (
add_cement_expenses_entry,get_cement_expenses_entry)

def cement_entry_form():
    with st.container(border=True):
        st.subheader("Add Cement Expense")
        col1, col2 = st.columns(2)
        with col1:
            entry_date = st.date_input("Date", key="purchase_date", value=date.today(), format=DATE_FORMAT)
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_CEMENT_VENDOR)
            price_per_bag = st.number_input("Price Per Bag", value=DEFAULT_CEMENT_COST_PER_BAG, step=5.00)
            driver_payment = st.radio("Driver Payment?", ["No", "Yes"], horizontal=True)
        with col2:            
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES) 
            cement_company_name = st.text_input("Cement Company", value=DEFAULT_CEMENT_COMPANY)
            no_of_bags = st.number_input("Quantity (bags)", min_value=0, step=5)
            if driver_payment == "Yes":
                driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
            else:
                driver_amount = st.number_input("Driver Amount", value=0, disabled=True)

           
        total_amount = (price_per_bag * no_of_bags) + driver_amount
        st.metric("Total Amount",  f"₹{total_amount:,.2f}")

        col1, col2 = st.columns(2)
        with col1:
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)
            paid_date = st.date_input("Payment Date", key="paid_date",value=date.today(), format=DATE_FORMAT)
        with col2 :
            payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES)

        if st.button("Add Entry"):
            if not vendor_name.strip():
                st.error("⚠️ Vendor name is required")
            elif not cement_company_name.strip():
                st.error("⚠️ Vendor name is required")
            elif price_per_bag <= 0:
                st.error("⚠️ Cost of the bag must be greater than 0")
            elif no_of_bags <= 0:
                st.error("⚠️ Number of the bag must be greater than 0")
            elif driver_payment == "Yes" and driver_amount <= 0:
                st.error("⚠️ Driver amount must be greater than 0")
            elif payment_amount <= 0:
                st.error("⚠️ Payment Amount must be greater than 0")
                return None        
            else:                
                cement_expenses_entry =  {
                    "delivery_date": str(entry_date),
                    "construction_stage": construction_stage,
                    "vendor_name":vendor_name,
                    "cement_company_name" : cement_company_name,
                    "price_per_bag" : price_per_bag,
                    "no_of_bags": int(no_of_bags),
                    "driver_amount": driver_amount,
                    "total_amount": total_amount,
                    "payment_amount":payment_amount,
                    "payment_mode": payment_mode,
                    "payment_date":str(paid_date),
                }
                st.write(cement_expenses_entry)
                add_cement_expenses_entry(cement_expenses_entry)
 
def render_expenses_history():
    st.subheader("Expense History") 
    data = get_cement_expenses_entry()
    if data:
        df = pd.DataFrame(data=data)
        st.dataframe(data=df, use_container_width=True,  hide_index=True)
    else:
        st.info("No expenses added yet.")             

def render_cement():
    st.title("Cement Management")
    st.write("Track and manage your cement usage effectively. Monitor purchases, consumption in concrete work, and maintain accurate stock levels.")

    # Form to add new cement expense entry
    cement_entry_form()   
    st.divider()
    # Expense history table (placeholder for now)
    render_expenses_history()