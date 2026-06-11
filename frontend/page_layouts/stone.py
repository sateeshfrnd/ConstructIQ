import streamlit as st
from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_STONE_VENDOR,
    STONES_TYPES_COST,
    DATE_FORMAT
)

def render_add_stone_entry_form():
    with st.container(border=True):
        st.subheader("Add Stone Purchase")

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", key="stone_date",value='today', format=DATE_FORMAT)
            stone_type = st.selectbox("Stone Type", list(STONES_TYPES_COST.keys()))
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_STONE_VENDOR, key="stone_vendor_name")
            driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True, key="stone_driver_payment")
                
        with col2:
            stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="stone_construction_stage")
            cost_per_truck = st.number_input("Cost Per Truck", value=STONES_TYPES_COST[stone_type], step=100.00)
            no_of_trucks = st.number_input("Number of Trucks", min_value=0.0, key="stone_no_of_trucks", step=1.0)
            if driver_payment == "Yes":
                driver_cost = st.number_input("Driver Amount", min_value=50, step=50)
            else :
                driver_cost = st.number_input("Driver Amount", value=0, disabled=True)

        # Total Amount Calculation        
        total_amount = (no_of_trucks * cost_per_truck) + driver_cost
        st.metric("Total Amount ", f"₹{total_amount:,.2f}")   

        # 
        col6, col7 = st.columns(2)
        with col6:
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Bank Transfer", "UPI"], key="stone_payment_mode")
        with col7:
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)

        if st.button("Add Stone Entry"):
            st.success("Stone entry added!")

def render_stone():
    st.title("🪨 Stone (Jelly) Management")
    st.write("Track and manage your stone materials efficiently. Keep records of purchases, usage in construction, and maintain clear visibility of stock levels.")
    
    render_add_stone_entry_form()

    st.divider()
    #  Expense History
    st.subheader("Purchase History")
    st.info("No records yet")

    

   

    