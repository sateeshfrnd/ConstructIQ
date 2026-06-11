import streamlit as st
from utils.constants import (
    CONSTRUCTION_STAGES, 
    DEFAULT_CEMENT_VENDOR, 
    DEFAULT_CEMENT_COMPANY, 
    DEFAULT_CEMENT_COST_PER_BAG,
    DATE_FORMAT
)

def cement_entry_form():
    with st.container(border=True):
        st.subheader("Add Cement Expense")
        col1, col2 = st.columns(2)
        with col1:
            purchase_date = st.date_input("Date", key="purchase_date", value='today', format=DATE_FORMAT)            
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_CEMENT_VENDOR)
            cost_per_bag = st.number_input("Price Per Bag", value=DEFAULT_CEMENT_COST_PER_BAG, step=5.00)
            driver_payment = st.radio("Driver Payment?", ["No", "Yes"], horizontal=True)
            

        with col2:            
            stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES) 
            company_name = st.text_input("Cement Company", value=DEFAULT_CEMENT_COMPANY)
            no_of_bags = st.number_input("Quantity (bags)", min_value=0, step=5)
            if driver_payment == "Yes":
                amount = st.number_input("Driver Amount", min_value=50, step=50)
            else :
                amount = st.number_input("Driver Amount", value=0, disabled=True)

        total_amount = (cost_per_bag * no_of_bags) + amount
        st.metric("Total Amount",  f"₹{total_amount:,.2f}")

        if st.button("Add Entry"):
            st.success("Brick expense added successfully!")

def render_cement():
    st.title("Cement Management")
    st.write("Track and manage your cement usage effectively. Monitor purchases, consumption in concrete work, and maintain accurate stock levels.")

    # Form to add new cement expense entry
    cement_entry_form()   
    st.divider()
    # Expense history table (placeholder for now)
    st.subheader("Expense History") 
    st.info("No records yet ")