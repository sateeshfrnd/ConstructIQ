import streamlit as st
import pandas as pd
from datetime import date

from utils.constants import DATE_FORMAT, PAYMENT_MODES
from services.api_client import (
    create_civil_contract, get_civil_contracts,
    add_civil_contract_payment, get_civil_contract_payments,
    save_civil_contract_stages, get_civil_contract_summary
)
from components.metric_cards import render_data_metrics_style3

CIVIL_STAGES = [
    "Pre_Construction", "Foundation", "GroundFloor_Strct",
    "FirstFloor_Strct", "SecondFloor_Strct", "ThirdFloor_Strct",
    "TopRoof", "Plastering", "Finishing"
]

STAGE_TYPES = ["structure", "plastering", "additional"]


def render_contract_setup():
    """Contract configuration form."""
    with st.container(border=True):
        st.subheader("📝 New Civil Contract")

        col1, col2 = st.columns(2)
        with col1:
            vendor_name = st.text_input("Vendor / Contractor Name", value="Rayappa")
            total_sqft = st.number_input("Total Square Feet", min_value=0.0, value=925.0, step=25.0)
            rate_per_chadara = st.number_input("Rate Per Chadara (₹)", min_value=0.0, value=31500.0, step=500.0)

        with col2:
            no_of_floors = st.number_input("No. of Floors", min_value=1, value=5, step=1)
            milestone_pct = st.number_input("Milestone % (for tracking)", min_value=0.0, max_value=100.0, value=70.0)
            no_of_partitions = st.number_input("No. of Partitions", min_value=1, value=5, step=1)

        # Auto-calculate
        chadara_per_sqft = 9.25  # standard conversion
        total_chadaras = total_sqft / 100 * chadara_per_sqft
        total_contract_cost = total_chadaras * rate_per_chadara
        cost_per_partition = total_contract_cost / no_of_partitions if no_of_partitions > 0 else 0
        milestone_amount = total_contract_cost * (milestone_pct / 100)

        st.divider()
        st.markdown("**Auto-Calculated Values**")
        calc_cols = st.columns(4)
        calc_cols[0].metric("Total Chadaras", f"{total_chadaras:.2f}")
        calc_cols[1].metric("Total Contract Cost", f"₹ {total_contract_cost:,.0f}")
        calc_cols[2].metric(f"{milestone_pct:.0f}% Milestone", f"₹ {milestone_amount:,.0f}")
        calc_cols[3].metric("Cost Per Partition", f"₹ {cost_per_partition:,.0f}")

        if st.button("✅ Create Contract"):
            if not vendor_name.strip():
                st.error("⚠️ Vendor name is required")
            elif total_sqft <= 0:
                st.error("⚠️ Square feet must be greater than 0")
            else:
                contract_data = {
                    "vendor_name": vendor_name,
                    "total_sqft": total_sqft,
                    "rate_per_chadara": rate_per_chadara,
                    "no_of_floors": no_of_floors,
                    "total_chadaras": total_chadaras,
                    "total_contract_cost": total_contract_cost,
                    "milestone_percentage": milestone_pct,
                    "no_of_partitions": no_of_partitions,
                    "cost_per_partition": cost_per_partition,
                    "notes": ""
                }
                response = create_civil_contract(contract_data)
                if response.status_code == 200:
                    st.success("✅ Contract created successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {response.text}")


def render_contract_dashboard(contract_id):
    """Main contract dashboard with summary, payments, and stage tracking."""
    summary = get_civil_contract_summary(contract_id)
    if not summary:
        st.error("Contract not found")
        return

    contract = summary["contract"]

    # ─── Contract Summary Header ───
    with st.container(border=True):
        st.markdown(f"### 📋 Contract: **{contract['vendor_name']}**")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Contract", f"₹ {contract['total_contract_cost']:,.0f}")
        col2.metric("Total Paid", f"₹ {summary['total_paid']:,.0f}")
        col3.metric("Balance", f"₹ {summary['balance']:,.0f}")
        col4.metric("Paid %", f"{summary['payment_percentage']}%")

        # Progress bar
        progress = min(summary['payment_percentage'] / 100, 1.0)
        st.progress(progress)

        # Contract details
        with st.expander("📐 Contract Details"):
            d_cols = st.columns(5)
            d_cols[0].write(f"**Sq Ft:** {contract['total_sqft']}")
            d_cols[1].write(f"**Rate/Chadara:** ₹{contract['rate_per_chadara']:,.0f}")
            d_cols[2].write(f"**Chadaras:** {contract['total_chadaras']:.2f}")
            d_cols[3].write(f"**Floors:** {contract['no_of_floors']}")
            d_cols[4].write(f"**Partitions:** {contract['no_of_partitions']}")

    st.write("")

    # ─── Two columns: Payment Form + Stage Tracking ───
    left_col, right_col = st.columns([3, 2])

    with left_col:
        # Payment entry form
        with st.container(border=True):
            st.subheader("💳 Add Payment")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                payment_date = st.date_input("Date", value=date.today(), format=DATE_FORMAT, key="cc_pay_date")
                construction_stage = st.selectbox("Stage", CIVIL_STAGES, key="cc_stage")
                description = st.text_input("Description", placeholder="e.g., 3rd Payment")
            with p_col2:
                payment_mode = st.selectbox("Payment Mode", PAYMENT_MODES, key="cc_mode")
                amount_paid = st.number_input("Amount (₹)", min_value=0.0, step=5000.0, key="cc_amount")

            if st.button("Add Payment", key="cc_add_pay"):
                if amount_paid <= 0:
                    st.error("⚠️ Amount must be greater than 0")
                else:
                    pay_data = {
                        "contract_id": contract_id,
                        "payment_date": str(payment_date),
                        "construction_stage": construction_stage,
                        "description": description,
                        "payment_mode": payment_mode,
                        "amount_paid": amount_paid
                    }
                    response = add_civil_contract_payment(pay_data)
                    if response.status_code == 200:
                        st.success("✅ Payment added")
                        st.rerun()
                    else:
                        st.error(f"❌ {response.text}")

        # Payment history
        st.subheader("📜 Payment History")
        payments = get_civil_contract_payments(contract_id)
        if payments:
            pay_df = pd.DataFrame(payments)
            pay_df = pay_df.drop(columns=["contract_id"], errors="ignore")
            st.dataframe(pay_df, use_container_width=True, hide_index=True)
            st.metric("Total Payments", f"₹ {summary['total_paid']:,.0f}")
        else:
            st.info("No payments recorded yet")

    with right_col:
        # Stage-wise Expected vs Actual
        with st.container(border=True):
            st.subheader("📊 Expected vs Actual")
            stage_comparison = summary.get("stage_comparison", [])
            if stage_comparison:
                for stage in stage_comparison:
                    expected = stage["expected"]
                    actual = stage["actual_paid"]
                    diff = expected - actual

                    st.markdown(f"**{stage['stage_name']}** ({stage['stage_type']})")
                    s_col1, s_col2, s_col3 = st.columns(3)
                    s_col1.metric("Expected", f"₹ {expected:,.0f}")
                    s_col2.metric("Actual", f"₹ {actual:,.0f}")
                    if diff > 0:
                        s_col3.metric("Remaining", f"₹ {diff:,.0f}")
                    elif diff < 0:
                        s_col3.metric("Over", f"₹ {abs(diff):,.0f}", delta=f"-₹{abs(diff):,.0f}", delta_color="inverse")
                    else:
                        s_col3.metric("Status", "✅ Settled")
                    st.divider()

                # Totals
                total_expected = sum(s["expected"] for s in stage_comparison)
                total_actual = sum(s["actual_paid"] for s in stage_comparison)
                st.markdown("**TOTAL**")
                t_col1, t_col2 = st.columns(2)
                t_col1.metric("Total Expected", f"₹ {total_expected:,.0f}")
                t_col2.metric("Total Actual", f"₹ {total_actual:,.0f}")
            else:
                st.info("No stages configured. Set up stages below.")

    # ─── Stage Setup Section ───
    st.divider()
    with st.expander("⚙️ Configure Stage Budget (Expected Amounts)", expanded=False):
        st.caption("Define expected payment amounts per construction stage")

        # Default stages based on the screenshot
        default_stages = [
            ("Basement", "structure"),
            ("First Floor", "structure"),
            ("Second Floor", "structure"),
            ("Third Floor", "structure"),
            ("Top Roof", "structure"),
            ("First Floor", "plastering"),
            ("Second Floor", "plastering"),
            ("Third Floor", "plastering"),
            ("Top Roof", "plastering"),
            ("Vaiskalu", "plastering"),
            ("Elevation", "plastering"),
            ("Additional Sompu", "additional"),
            ("Moridu", "additional"),
        ]

        stages_to_save = []
        for i, (default_name, default_type) in enumerate(default_stages):
            s_col1, s_col2, s_col3 = st.columns([2, 1, 2])
            with s_col1:
                stage_name = st.text_input("Stage", value=default_name, key=f"stg_name_{i}")
            with s_col2:
                stage_type = st.selectbox("Type", STAGE_TYPES, index=STAGE_TYPES.index(default_type), key=f"stg_type_{i}")
            with s_col3:
                expected_amt = st.number_input("Expected (₹)", min_value=0.0, step=10000.0, key=f"stg_amt_{i}")

            if stage_name.strip() and expected_amt > 0:
                stages_to_save.append({
                    "contract_id": contract_id,
                    "stage_name": stage_name,
                    "stage_type": stage_type,
                    "expected_amount": expected_amt
                })

        if st.button("💾 Save Stages", key="save_stages_btn"):
            if stages_to_save:
                response = save_civil_contract_stages(contract_id, stages_to_save)
                if response.status_code == 200:
                    st.success(f"✅ Saved {len(stages_to_save)} stages")
                    st.rerun()
                else:
                    st.error(f"❌ {response.text}")
            else:
                st.warning("No stages with amounts to save")


def render_civil_contract():
    """Main entry point for the Civil Contract page."""
    st.title("👷 Civil Contract Management")
    st.caption("Track your civil construction contract — payments, stage-wise budget, and progress.")

    # Check if contracts exist
    contracts = get_civil_contracts()

    if not contracts:
        st.info("No contracts found. Create your first contract below.")
        render_contract_setup()
        return

    # Contract selector (if multiple)
    if len(contracts) == 1:
        selected_contract_id = contracts[0]["id"]
    else:
        contract_options = {f"{c['vendor_name']} (ID: {c['id']})": c["id"] for c in contracts}
        selected_label = st.selectbox("Select Contract", list(contract_options.keys()))
        selected_contract_id = contract_options[selected_label]

    # Render the selected contract dashboard
    render_contract_dashboard(selected_contract_id)

    # Option to create another contract
    st.divider()
    with st.expander("➕ Create New Contract"):
        render_contract_setup()
