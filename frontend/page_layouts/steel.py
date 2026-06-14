import streamlit as st
from datetime import date
from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_STEEL_VENDOR,
    STEEL_CATEGORIES,
    PAYMENT_MODES,
    STEEL_SIZES_COST,
    DEFAULT_STEEL_COST_PER_KG,
    DEFAULT_BINDING_WIRE_COST_PER_BUNDLE,
    DATE_FORMAT,
)
from services.api_client import add_steel_expenses_entry
def render_add_steel_entry_form():
    with st.container(border=True):
        st.subheader("Add Steel Purchase")
         # Row 1: Date, Stage
        col1, col2 = st.columns(2)                    
        with col1:
            delivery_date = st.date_input("Date", key="steel_purchase_date",value='today', format=DATE_FORMAT) 
            vendor_name = st.text_input("Vendor Name", value= DEFAULT_STEEL_VENDOR)
        with col2:
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="construction_stage")
                
        steel_type = st.segmented_control("", STEEL_CATEGORIES, key="steel_type")
        total_steel_amount = 0.0
        total_bundle_amount = 0.0
        if steel_type == STEEL_CATEGORIES[0]:
            # Show size, bundles, cost per bundle
            col1, col2 = st.columns(2)
            with col1:
                size = st.selectbox("Size (MM)",STEEL_SIZES_COST.keys(), key="steel_size")
                cost_per_kg = st.number_input("Price Per KG", value=DEFAULT_STEEL_COST_PER_KG, key="steel_cost_per_kg",step=5.0)
                driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True)

            with col2:
                bundles = st.number_input("No Of Bundles", min_value=0, key="steel_bundles")
                price_per_bundle = st.number_input("Price Per Bundle", value=float(STEEL_SIZES_COST[size]), key="steel_cost_per_bundle", step=5.0)
                if driver_payment == "Yes":
                    driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
                else :
                    driver_amount = st.number_input("Driver Amount", value=0, disabled=True) 

            # Total Weight and Total Amount Calculation (important feature for quick insights)
            col1,col2=st.columns(2)
            with col1:     
                if bundles > 0 and price_per_bundle > 0:
                    total_weight = bundles * price_per_bundle                    
                    st.metric("Total Weight ", f"{total_weight:.2f} KG")
                        
            with col2:
                if bundles > 0 and price_per_bundle > 0 and cost_per_kg > 0:
                    total_steel_amount = (total_weight * cost_per_kg) + driver_amount
                    st.metric("Total Amount" , f"₹{total_steel_amount:,.2f}")            

        elif steel_type == STEEL_CATEGORIES[1]:
            # Show quantity, price, and vendor for binding wire      
            col1, col2 = st.columns(2)

            with col1:
                bundles = st.number_input("No Of Bundles", min_value=0, step=1, key="binding_wire_bundles")

            with col2:
                price_per_bundle = st.number_input("Price Per Bundle", value=DEFAULT_BINDING_WIRE_COST_PER_BUNDLE, key="binding_wire_cost_per_bundle")

            if bundles > 0 and price_per_bundle > 0:
                total_bundle_amount = bundles * price_per_bundle
                st.metric("Total Amount ", f"₹{total_bundle_amount:,.2f}")  

        if steel_type ==STEEL_CATEGORIES[0]:
            total_amount = total_steel_amount
        elif steel_type == STEEL_CATEGORIES[1]:
            total_amount = total_bundle_amount
            total_weight = 0.0
            driver_amount = 0.0
            size = ""
        else:
            total_amount = 0.0 

        col1, col2 = st.columns(2)
        with col1:            
            payment_amount = st.number_input("Payment Amount", min_value=0.0, value=total_amount)
            paid_date = st.date_input("Payment Date", key="paid_date",value=date.today(), format=DATE_FORMAT)
        with col2 :
            payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES)

        if st.button("Add Entry"):
            if steel_type is None:
                st.error('Select Entry type Steel/BindingWire')
            elif bundles<=0:
                st.error("Number of bundles must be greater than 0")
            elif price_per_bundle<=0:
                st.error("Price per bundle must be greater than 0")
            elif steel_type ==STEEL_CATEGORIES[0] and driver_payment == "Yes" and driver_amount <= 0:
                st.error("⚠️ Driver amount must be greater than 0")
            elif payment_amount <= 0:
                st.error("⚠️ Payment Amount must be greater than 0")   
            else:
                steel_bundle_entry = {
                    "delivery_date" : str(delivery_date),
                    "construction_stage" : construction_stage,
                    "vendor_name" : vendor_name,
                    "steel_type":steel_type,
                    "size": size,
                    "num_bundles" : int(bundles),
                    "price_per_bundle" : price_per_bundle,
                    "total_weight" :  total_weight,
                    "driver_amount": driver_amount,
                    "total_amount": total_amount,
                    "payment_amount":payment_amount,
                    "payment_mode": payment_mode,
                    "payment_date":str(paid_date)
                } 
                st.write(steel_bundle_entry) 
                add_steel_expenses_entry(steel_bundle_entry)
            
def render_steel():
    st.title("Steel & Reinforcement Management")
    st.write("Track and manage your steel inventory with precision. Monitor procurement, usage across activities, and keep control of material costs.")
    
    render_add_steel_entry_form()
    st.divider()
    # 📜 Expense History
    st.subheader("Purchase History")
    st.info("No records yet ")