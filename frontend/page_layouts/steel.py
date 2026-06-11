import streamlit as st

from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_STEEL_VENDOR,
    STEEL_CATEGORIES,
    PAYMENT_MODES,
    STEEL_SIZES_COST,
    DEFAULT_STEEL_COST_PER_KG,
    DEFAULT_BINDING_WIRE_COST_PER_BUNDLE,
    DATE_FORMAT
)
def render_add_steel_entry_form():
    with st.container(border=True):
        st.subheader("Add Steel Purchase")
         # Row 1: Date, Stage
        col1, col2 = st.columns(2)                    
        with col1:
            date = st.date_input("Date", key="steel_purchase_date",value='today', format=DATE_FORMAT)                    
        with col2:
            stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="construction_stage")
                
        steel_type = st.segmented_control("", STEEL_CATEGORIES, key="steel_type")
        if steel_type == STEEL_CATEGORIES[0]:
            # Show size, bundles, cost per bundle
            col1, col2 = st.columns(2)
            with col1:
                size = st.selectbox("Size (MM)",STEEL_SIZES_COST.keys(), key="steel_size")
                cost_per_kg = st.number_input("Price Per KG", value=DEFAULT_STEEL_COST_PER_KG, key="steel_cost_per_kg",step=5.0)
                driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True)

            with col2:
                bundles = st.number_input("No Of Bundles", min_value=0, key="steel_bundles")
                cost_per_bundle = st.number_input("Price Per Bundle", value=float(STEEL_SIZES_COST[size]), key="steel_cost_per_bundle", step=5.0)
                if driver_payment == "Yes":
                    driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
                else :
                    driver_amount = st.number_input("Driver Amount", value=50, disabled=True) 

            # Total Weight and Total Amount Calculation (important feature for quick insights)
            col1,col2=st.columns(2)
            with col1:     
                if bundles > 0 and cost_per_bundle > 0:
                    total_weight = bundles * cost_per_bundle                    
                    st.metric("Total Weight ", f"{total_weight:.2f} KG")
                        
            with col2:
                if bundles > 0 and cost_per_bundle > 0 and cost_per_kg > 0:
                    total_amount = (total_weight * cost_per_kg) + driver_amount
                    st.metric("Total Amount" , f"₹{total_amount:,.2f}")

        elif steel_type == STEEL_CATEGORIES[1]:
            # Show quantity, price, and vendor for binding wire      
            col1, col2 = st.columns(2)

            with col1:
                bundles = st.number_input("No Of Bundles", min_value=0, step=1, key="binding_wire_bundles")

            with col2:
                cost_per_bundle = st.number_input("Price Per Bundle", value=DEFAULT_BINDING_WIRE_COST_PER_BUNDLE, key="binding_wire_cost_per_bundle")

            if bundles > 0 and cost_per_bundle > 0:
                total_amount = bundles * cost_per_bundle
                st.metric("Total Amount ", f"₹{total_amount:,.2f}")  

        if st.button("Add Entry"):
            st.success("Steel purchase added successfully!") 

            
def render_steel():
    st.title("Steel & Reinforcement Management")
    st.write("Track and manage your steel inventory with precision. Monitor procurement, usage across activities, and keep control of material costs.")
    

    render_add_steel_entry_form()
    st.divider()

    # 📜 Expense History
    st.subheader("Purchase History")
    st.info("No records yet ")