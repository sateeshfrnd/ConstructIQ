import streamlit as st

from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_SAND_VENDOR,
    SAND_TYPES_COST,
    DATE_FORMAT
)
from services.api_client import add_sand_expenses_entry

def render_add_sand_entry_form():
    with st.container(border=True):
        st.subheader("Add Sand Purchase")
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", key="sand_date")
            sand_type = st.selectbox("Sand Type", list(SAND_TYPES_COST.keys()))
            cost_per_truck = st.number_input(
                "Cost Per Truck", 
                value=SAND_TYPES_COST[sand_type],
                # key="sand_cost_per_truck_input",
                # on_change=lambda: st.session_state.update({"sand_cost_per_truck": st.session_state.sand_cost_per_truck_input})
            )
            driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True, key="sand_driver_payment")
                
        with col2:
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="sand_construction_stage")
            no_of_trucks = st.number_input("Number of Trucks", min_value=0.0, key="sand_no_of_trucks", step=1.0)
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_SAND_VENDOR, key="sand_vendor_name")
            if driver_payment == "Yes":
                driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
            else :
                driver_amount = st.number_input("Driver Amount", value=0, disabled=True)

        # Total Amount Calculation        
        total_amount = (no_of_trucks * cost_per_truck) + driver_amount
        st.metric("Total Amount ", f"₹{total_amount:,.2f}")  

        col6, col7 = st.columns(2)
        with col6:
            paid_date = st.date_input("Payment Date", key="paid_date",value=date.today(), format=DATE_FORMAT)
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Bank Transfer", "UPI"], key="sand_payment_mode")
        with col7:
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)

        
        if st.button("Add Sand Entry"):
            if not sand_type.strip():
                st.error("⚠️ sand type is required")
            elif not vendor_name.strip():
                st.error("⚠️ Vendor name is required")    
            elif no_of_trucks<= 0:
                st.error("⚠️ number of trucks must be greater than 0")
            else:
                sand_entry ={
                    "delivery_date" : str(date),
                    "construction_stage": construction_stage,
                    "sand_type": sand_type,
                    "vendor_name":vendor_name,
                    "cost_per_truck" : cost_per_truck,
                    "no_of_trucks": int(no_of_trucks),
                    "driver_amount": driver_amount,
                    "total_amount": total_amount,
                    "payment_date": str(paid_date),
                    "payment_amount":payment_amount,
                    "payment_mode": payment_mode,                    
                } 
                st.write(sand_entry) 
                add_sand_expenses_entry(sand_entry)


def render_sand():
    st.title("Sand Management")
    st.write("Track and manage your sand usage seamlessly. Record deliveries, monitor consumption, and ensure optimal material availability for construction.")
    render_add_sand_entry_form()
   
    #  Expense History
    st.subheader("Purchase History")
    st.info("No records yet")