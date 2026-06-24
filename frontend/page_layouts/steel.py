import streamlit as st
from datetime import date
import pandas as pd

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
from services.api_client import (
    add_steel_expenses_entry, get_steel_expenses_entry, get_steel_expenses_metrics)
from components.metric_cards import render_data_metrics_style3


def render_steel_category_metrics(data):
    """Render Binding Wire and Steel metrics vertically grouped by category."""
    # Binding Wire Section
    wire = data.get("binding_wire", {})
    with st.container(border=True):
        st.markdown("**🔗 Binding Wire**")
        if wire.get("bundles", 0) > 0:
            st.metric("Bundles", f"{wire['bundles']}")
            st.metric("Total Cost", f"₹ {wire['cost']:,.0f}")
        else:
            st.info("No binding wire purchases yet")

    st.write("")

    # Steel by Size Section
    size_breakdown = data.get("steel_size_breakdown", {})
    with st.container(border=True):
        st.markdown("**🏗️ Steel (by Size)**")
        if size_breakdown:
            for size, info in size_breakdown.items():
                st.markdown(f"**{size}**")
                # col_a, col_b, col_c = st.columns(3)
                col_a, col_c = st.columns(2)
                col_a.metric("Bundles", f"{info['bundles']}")
                # col_b.metric("Weight", f"{info['weight']:,.1f} KG")
                col_c.metric("Cost", f"₹ {info['cost']:,.0f}")
                st.divider()
        else:
            st.info("No steel purchases yet")


def render_add_steel_entry_form():
    with st.container(border=True):
        st.subheader("Add Steel Purchase")
        col1, col2 = st.columns(2)
        with col1:
            delivery_date = st.date_input("Date", key="steel_purchase_date", value='today', format=DATE_FORMAT)
            vendor_name = st.text_input("Vendor Name", value=DEFAULT_STEEL_VENDOR)
        with col2:
            construction_stage = st.selectbox("Construction Stage", CONSTRUCTION_STAGES, key="construction_stage")

        steel_type = st.segmented_control("", STEEL_CATEGORIES, key="steel_type")
        total_steel_amount = 0.0
        total_bundle_amount = 0.0
        if steel_type == STEEL_CATEGORIES[0]:
            col1, col2 = st.columns(2)
            with col1:
                size = st.selectbox("Size (MM)", STEEL_SIZES_COST.keys(), key="steel_size")
                cost_per_kg = st.number_input("Price Per KG", value=DEFAULT_STEEL_COST_PER_KG, key="steel_cost_per_kg", step=5.0)
                driver_payment = st.radio("Driver Payment", ["No", "Yes"], horizontal=True)
            with col2:
                bundles = st.number_input("No Of Bundles", min_value=0, key="steel_bundles")
                price_per_bundle = st.number_input("Price Per Bundle", value=float(STEEL_SIZES_COST[size]), key="steel_cost_per_bundle", step=5.0)
                if driver_payment == "Yes":
                    driver_amount = st.number_input("Driver Amount", min_value=50, step=50)
                else:
                    driver_amount = st.number_input("Driver Amount", value=0, disabled=True)

            col1, col2 = st.columns(2)
            with col1:
                if bundles > 0 and price_per_bundle > 0:
                    total_weight = bundles * price_per_bundle
                    st.metric("Total Weight", f"{total_weight:.2f} KG")
            with col2:
                if bundles > 0 and price_per_bundle > 0 and cost_per_kg > 0:
                    total_steel_amount = (total_weight * cost_per_kg) + driver_amount
                    st.metric("Total Amount", f"₹{total_steel_amount:,.2f}")

        elif steel_type == STEEL_CATEGORIES[1]:
            col1, col2 = st.columns(2)
            with col1:
                bundles = st.number_input("No Of Bundles", min_value=0, step=1, key="binding_wire_bundles")
            with col2:
                price_per_bundle = st.number_input("Price Per Bundle", value=DEFAULT_BINDING_WIRE_COST_PER_BUNDLE, key="binding_wire_cost_per_bundle")
            if bundles > 0 and price_per_bundle > 0:
                total_bundle_amount = bundles * price_per_bundle
                st.metric("Total Amount", f"₹{total_bundle_amount:,.2f}")

        if steel_type == STEEL_CATEGORIES[0]:
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
            paid_date = st.date_input("Payment Date", key="paid_date", value=date.today(), format=DATE_FORMAT)
        with col2:
            payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES)

        if st.button("Add Entry"):
            if steel_type is None:
                st.error('Select Entry type Steel/BindingWire')
            elif bundles <= 0:
                st.error("Number of bundles must be greater than 0")
            elif price_per_bundle <= 0:
                st.error("Price per bundle must be greater than 0")
            elif steel_type == STEEL_CATEGORIES[0] and driver_payment == "Yes" and driver_amount <= 0:
                st.error("⚠️ Driver amount must be greater than 0")
            elif payment_amount <= 0:
                st.error("⚠️ Payment Amount must be greater than 0")
            else:
                steel_bundle_entry = {
                    "delivery_date": str(delivery_date),
                    "construction_stage": construction_stage,
                    "vendor_name": vendor_name,
                    "steel_type": steel_type,
                    "size": size,
                    "num_bundles": int(bundles),
                    "price_per_bundle": price_per_bundle,
                    "total_weight": total_weight,
                    "driver_amount": driver_amount,
                    "total_amount": total_amount,
                    "payment_amount": payment_amount,
                    "payment_mode": payment_mode,
                    "payment_date": str(paid_date)
                }
                st.write(steel_bundle_entry)
                add_steel_expenses_entry(steel_bundle_entry)


def render_expenses_history():
    data = get_steel_expenses_entry()
    from components.editable_table import render_editable_history
    render_editable_history(data, "steel")


def render_steel():
    st.title("Steel & Reinforcement Management")
    st.write("Track and manage your steel inventory with precision. Monitor procurement, usage across activities, and keep control of material costs.")

    # Row 1: Overall summary across full width
    data = get_steel_expenses_metrics(params=None)
    # st.write(data)
    if isinstance(data, dict) and data.get("detail") == "Not Found":
        st.info("No steel expense metrics available yet.")
    elif isinstance(data, dict) and data.get("error"):
        st.error(data["error"])
    else:
        summary_metrics = {
            "Total Spend": f"₹ {data['total_spend']:,.0f}",
            "Total Paid": f"₹ {data['total_paid']:,.0f}",
            "Outstanding": f"₹ {data['outstanding_amount']:,.0f}",
            "Avg Cost/KG": f"₹ {data['avg_cost_per_kg']:,.2f}"
        }
        render_data_metrics_style3(dict_datametrics=summary_metrics)

    # Side-by-side: Entry Form (left) | Category Metrics (right)
    left_col, right_col = st.columns([3, 2])

    with left_col:
        render_add_steel_entry_form()

    with right_col:
        render_steel_category_metrics(data)

    st.divider()
    render_expenses_history()
