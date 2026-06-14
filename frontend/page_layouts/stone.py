import streamlit as st
from datetime import date
from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_STONE_VENDOR,
    STONES_TYPES_COST,
    DATE_FORMAT
)

from services.api_client import add_stone_expenses_entry
def render_add_stone_entry_form():
    with st.container(border=True):
        st.subheader("Add Stone Purchase")

        col1, col2 = st.columns(2)
        with col1:
            delivery_date = st.date_input("Date", key="stone_date", value=date.today(), format=DATE_FORMAT)
            stone_type = st.selectbox("Stone Type", list(STONES_TYPES_COST.keys()))
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_STONE_VENDOR, key="stone_vendor_name")
            driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True, key="stone_driver_payment")
                
        with col2:
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="stone_construction_stage")
            cost_per_truck = st.number_input("Cost Per Truck", value=STONES_TYPES_COST[stone_type], step=100.00)
            no_of_trucks = st.number_input("Number of Trucks", min_value=0, key="stone_no_of_trucks", step=1)
            if driver_payment == "Yes":
                driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
            else :
                driver_amount = st.number_input("Driver Amount", value=0, disabled=True)

        # Total Amount Calculation        
        total_amount = (no_of_trucks * cost_per_truck) + driver_amount
        st.metric("Total Amount ", f"₹{total_amount:,.2f}")   

        # 
        col6, col7 = st.columns(2)
        with col6:
            paid_date = st.date_input("Payment Date", key="paid_date",value=date.today(), format=DATE_FORMAT)
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Bank Transfer", "UPI"], key="sand_payment_mode")
        with col7:
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)


        if st.button("Add Stone Entry"):
            if not vendor_name.strip():
                st.error("⚠️ Vendor name is required")
            elif cost_per_truck<=0:
                st.error(" cost_per_truck is required greater than 0")
            elif no_of_trucks<=0:
                st.error("no_of_truck is required greater than 0")    
            elif driver_payment == "Yes" and driver_amount <= 0:
                st.error("⚠️ Driver amount must be greater than 0")
            elif payment_amount <= 0:
                st.error("⚠️ Payment Amount must be greater than 0")
                return None
            else:
                stone_entry={  
                "delivery_date": str(delivery_date),
                "construction_stage": construction_stage ,
                "stone_type":stone_type,
                "cost_per_truck":cost_per_truck,
                "vendor_name":vendor_name,
                "no_of_trucks": int(no_of_trucks),
                "driver_amount": driver_amount,
                "total_amount":total_amount,
                "payment_amount":payment_amount,
                "payment_mode": payment_mode, 
                "payment_date": str(paid_date),   
                }
                st.write(stone_entry)
                result = add_stone_expenses_entry(stone_entry)
                if isinstance(result, dict) and result.get("error"):
                    st.error(result["error"])
                else:
                    st.success("Stone entry submitted successfully")

def render_stone():
    st.title("🪨 Stone (Jelly) Management")
    st.write("Track and manage your stone materials efficiently. Keep records of purchases, usage in construction, and maintain clear visibility of stock levels.")
    
    render_add_stone_entry_form()

    st.divider()
    #  Expense History
    st.subheader("Purchase History")
    st.info("No records yet")

    

   

    