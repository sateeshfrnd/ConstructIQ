import streamlit as st

from utils.constants import (
    CONSTRUCTION_STAGES,
    DEFAULT_BRICK_VENDOR,
    PAYMENT_MODES,
    BRICK_SIZE_COST,
    DATE_FORMAT
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
            payment = st.number_input("Payment Amount", min_value=0.0)
            paid_date = st.date_input("Payment Date", key="paid_date")
            

        with col2:            
            stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES) 
            # Safe lookup with fallback to the first defined cost
            default_price = float(next(iter(BRICK_SIZE_COST.values())))
            price_per_brick = st.number_input(
                "Price Per Brick",
                min_value=0.0,
                value=float(BRICK_SIZE_COST.get(brick_type, default_price)),
                step=5.0,
            )
            no_of_blocks = st.number_input("Quantity (bricks)", min_value=0, step=5)
            payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES)
            total_cost = price_per_brick * no_of_blocks
            st.metric("Total Cost", f"₹{total_cost:,.2f}")

        if st.button("Add Entry"):
            st.success("Brick expense added successfully!")

def render_bricks():
    st.title("🧱 Brick Management")
    st.write("Track and manage your brick inventory efficiently. Record purchases, monitor usage across construction stages, and stay on top of your brick consumption.")
 
    # Add Brick Expense
    render_add_bricks_entry_form()

    st.divider()

    # Expense History
    st.subheader("Expense History")
    st.info("No records yet ")