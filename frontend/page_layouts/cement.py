import streamlit as st
from utils.constants import (
    CONSTRUCTION_STAGES, DEFAULT_CEMENT_VENDOR, DEFAULT_CEMENT_COMPANY, 
    DEFAULT_CEMENT_COST_PER_BAG
)

def metric_card(title, value):
    st.markdown(
        f"""
        <div style="
            background-color:#1e293b;
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.3);   
            min-height:120px;                
            display:flex;                 
            flex-direction:column;
            justify-content:center;
            gap:6px;
        ">
            <div style="font-size:14px; color:#94a3b8;">{title}</div>
            <div style="font-size:26px; font-weight:bold; color:#38bdf8;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_cement_metrics():
    # 🔢 Example Data (Replace with DB later)
    total_purchased = 500
    used_in_concrete = 320
    remaining = total_purchased - used_in_concrete
    total_cost = 190000

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Purchased", f"{total_purchased} bags")

    with col2:
        metric_card("Used in Concrete", f"{used_in_concrete} bags")

    with col3:
        metric_card("Remaining", f"{remaining} bags")

    with col4:
        metric_card("Total Cost", f"₹ {total_cost:,}")

def render_cement():
    st.title("Cement Management")

    # Metrics at the top
    render_cement_metrics()   
    st.divider()
    # Form to add new cement expense entry
    cement_entry_form()   
    st.divider()
    # Expense history table (placeholder for now)
    st.subheader("Expense History")    

def cement_entry_form():
    st.subheader("Add Cement Expense")

    # Row 1: Add fields for Date, Construction Stage, Vendor Name
    col1, col2, col3 = st.columns(3)
    with col1:
        purchase_date = st.date_input("Date")

    with col2:
        stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES)        
                
    with col3:       
        vendor_name = st.text_input("Vendor Name", value=DEFAULT_CEMENT_VENDOR)

    # Row 2: Add fields for Cement Company, Cost Per Bag, and Number of Bags
    col4, col5, col6 = st.columns(3)
    with col4:
        company_name = st.text_input("Cement Company", value=DEFAULT_CEMENT_COMPANY)
    with col5:    
        cost_per_bag = st.number_input("Price Per Bag", min_value=0.0, value=DEFAULT_CEMENT_COST_PER_BAG)

    with col6:
        no_of_bags = st.number_input("Quantity (bags)", min_value=0)    

    # Row 3: Add option for driver payment and calculate final total if applicable
    col7, col8, col9 = st.columns(3)

    driver_payment = 0.0

    with col7:
        driver_payment = st.radio("Driver Payment?", ["No", "Yes"], horizontal=True)
        # driver_payment = st.toggle("Driver Payment")

    with col8:
        if driver_payment == "Yes":
            amount = st.number_input("Driver Amount")
        else :
            amount = st.number_input("Driver Amount", value=0.0, disabled=True)

    with col9:
        total_amount = (cost_per_bag * no_of_bags) + amount
        st.metric("Total Amount",  f"₹{total_amount:,.2f}"
    )

    # Row 4: Add a button to submit the form
    if st.button("Add Entry"):
        st.success("Cement expense added successfully!")