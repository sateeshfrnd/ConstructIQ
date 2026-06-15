import streamlit as st
from datetime import date
import pandas as pd
from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_BRICK_VENDOR,
    PAYMENT_MODES,
    BRICK_SIZE_COST,
    DATE_FORMAT
)
from services.api_client import (
    add_bricks_expenses_entry,get_bricks_expenses_entry
)
def render_add_bricks_entry_form():
    with st.container(border=True):
        st.subheader("Add Sand Purchase")
        col1, col2 = st.columns(2)
        with col1:
            purchase_date = st.date_input("Date", key="purchase_date", value='today', format=DATE_FORMAT)
            # Choose a brick size (default to first available)
            brick_type = st.selectbox("Brick Size 🧱", list(BRICK_SIZE_COST.keys()), index=0, key="brick_type")
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_BRICK_VENDOR)            
            driver_payment = st.radio("Driver Payment?", ["No", "Yes"], horizontal=True)

            

        with col2:            
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES) 
            # Safe lookup with fallback to the first defined cost
            default_price = float(next(iter(BRICK_SIZE_COST.values())))
            price_per_brick = st.number_input(
                "Price Per Brick",
                min_value=0.0,
                value=float(BRICK_SIZE_COST.get(brick_type, default_price)),
                step=5.0,
            )
            no_of_blocks = st.number_input("Quantity (bricks)", min_value=0, step=5)
            if driver_payment == "Yes":
                driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
            else:
                driver_amount = st.number_input("Driver Amount", value=0, disabled=True)
            
        total_cost = (price_per_brick * no_of_blocks) + driver_amount
        st.metric("Total Cost", f"₹{total_cost:,.2f}")

        col1, col2 = st.columns(2)
        with col1:    
            paid_date = st.date_input("Payment Date", key="paid_date",value=date.today(), format=DATE_FORMAT)       
            payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES)         
        with col2 :            
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_cost)

   


        if st.button("Add Entry"):
            if not vendor_name.strip():
                st.error("⚠️ Vendor name is required")
            elif not brick_type.strip():
                st.error("⚠️ brick_type is required")   
            elif price_per_brick <= 0:
                st.error("⚠️ Price per brick  must be greater than 0")
            elif no_of_blocks <= 0:
                st.error("⚠️ Quantity must be greater than 0")
            elif price_per_brick <= 0:
                st.error("⚠️ Cost of the bag must be greater than 0")
            elif driver_payment == "Yes" and driver_amount <= 0:
                st.error("⚠️ Driver amount must be greater than 0")
            else :
                bricks_entry = {
                          "purchase_date" : str(purchase_date),
                          "construction_stage": construction_stage,
                          "vendor_name":vendor_name,
                          "brick_size":brick_type,
                          "quantity":no_of_blocks,
                          "price_per_brick" : price_per_brick,
                          "driver_amount": driver_amount,
                          "total_amount":total_cost,
                          "payment_amount":payment_amount,
                          "payment_mode": payment_mode,
                          "payment_date":str(paid_date),
                }
                st.write(bricks_entry)      
                add_bricks_expenses_entry(bricks_entry)

def render_expenses_history():
    st.subheader("Expense History") 
    data = get_bricks_expenses_entry()
    if data:
        df = pd.DataFrame(data=data)
        st.dataframe(data=df, use_container_width=True,  hide_index=True)
    else:
        st.info("No expenses added yet.")                

def render_bricks():
    st.title("🧱 Brick Management")
    st.write("Track and manage your brick inventory efficiently. Record purchases, monitor usage across construction stages, and stay on top of your brick consumption.")
 
    # Add Brick Expense
    render_add_bricks_entry_form()

    st.divider()

    # Expense History
    render_expenses_history()