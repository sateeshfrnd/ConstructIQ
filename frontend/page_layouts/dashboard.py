import streamlit as st
import pandas as pd

from services.api_client import get_dashboard_summary
from components.metric_cards import render_data_metrics_style3


def render_dashboard():
    if not st.session_state.get("authenticated"):
        st.warning("Please login")
        st.stop()

    st.title("🏗️ Construct IQ Dashboard")
    st.caption("Complete overview of your construction project expenses at a glance.")

    data = get_dashboard_summary()

    # ─────────────────────────────────────────────
    # ROW 1: Grand totals
    # ─────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Project Cost", f"₹ {data['grand_total']:,.0f}")
    col2.metric("✅ Total Paid", f"₹ {data['total_paid']:,.0f}")
    col3.metric("⚠️ Outstanding", f"₹ {data['outstanding']:,.0f}")
    col4.metric("📋 Total Entries", f"{data['total_entries']}")

    st.divider()

    # ─────────────────────────────────────────────
    # ROW 2: Category-wise spend (bar chart + table)
    # ─────────────────────────────────────────────
    st.subheader("📊 Category-wise Expenses")

    categories = data.get("categories", {})
    if categories:
        # Build DataFrame for chart
        cat_df = pd.DataFrame([
            {
                "Category": cat,
                "Total Amount": info["total_amount"],
                "Total Paid": info["total_paid"],
                "Outstanding": info["total_amount"] - info["total_paid"],
                "Entries": info["entries"]
            }
            for cat, info in categories.items()
            if info["total_amount"] > 0
        ])

        if not cat_df.empty:
            left_col, right_col = st.columns([3, 2])

            with left_col:
                # Bar chart
                chart_df = cat_df.set_index("Category")[["Total Amount"]]
                st.bar_chart(chart_df, color="#38bdf8")

            with right_col:
                # Summary table
                display_df = cat_df.copy()
                display_df["Total Amount"] = display_df["Total Amount"].apply(lambda x: f"₹ {x:,.0f}")
                display_df["Total Paid"] = display_df["Total Paid"].apply(lambda x: f"₹ {x:,.0f}")
                display_df["Outstanding"] = display_df["Outstanding"].apply(lambda x: f"₹ {x:,.0f}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No expense data available yet. Start adding entries!")

    st.divider()

    # ─────────────────────────────────────────────
    # ROW 3: Stage-wise breakdown + Payment modes
    # ─────────────────────────────────────────────
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("🏗️ Stage-wise Spend")
        stage_data = data.get("stage_breakdown", {})
        if stage_data:
            stage_df = pd.DataFrame([
                {"Stage": stage, "Amount": amount}
                for stage, amount in sorted(stage_data.items(), key=lambda x: x[1], reverse=True)
            ])
            st.bar_chart(stage_df.set_index("Stage"), color="#818cf8")

            # Show as metrics
            stage_cols = st.columns(min(len(stage_data), 3))
            for i, (stage, amount) in enumerate(sorted(stage_data.items(), key=lambda x: x[1], reverse=True)):
                with stage_cols[i % 3]:
                    st.metric(stage, f"₹ {amount:,.0f}")
        else:
            st.info("No stage data available")

    with right_col:
        st.subheader("💳 Payment Modes")
        payment_modes = data.get("payment_modes", {})
        if payment_modes:
            mode_df = pd.DataFrame([
                {"Mode": mode, "Amount": amount}
                for mode, amount in payment_modes.items()
            ])
            # Pie-like display using metrics
            total_payments = sum(payment_modes.values())
            for mode, amount in sorted(payment_modes.items(), key=lambda x: x[1], reverse=True):
                pct = (amount / total_payments * 100) if total_payments > 0 else 0
                st.metric(
                    f"{mode}",
                    f"₹ {amount:,.0f}",
                    f"{pct:.1f}%"
                )
        else:
            st.info("No payment data available")

    st.divider()

    # ─────────────────────────────────────────────
    # ROW 4: Material vs Workforce vs Other split
    # ─────────────────────────────────────────────
    st.subheader("📈 Expense Distribution")

    materials = ["Cement", "Bricks", "Steel", "Sand", "Stone"]
    workforce = ["Labour", "Electric", "Plumbing", "Painting"]
    other = ["Site Expenses"]

    material_total = sum(categories.get(c, {}).get("total_amount", 0) for c in materials)
    workforce_total = sum(categories.get(c, {}).get("total_amount", 0) for c in workforce)
    other_total = sum(categories.get(c, {}).get("total_amount", 0) for c in other)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("**🧱 Materials**")
            st.metric("Total", f"₹ {material_total:,.0f}")
            if data["grand_total"] > 0:
                pct = material_total / data["grand_total"] * 100
                st.progress(min(pct / 100, 1.0))
                st.caption(f"{pct:.1f}% of total")

    with col2:
        with st.container(border=True):
            st.markdown("**👷 Workforce**")
            st.metric("Total", f"₹ {workforce_total:,.0f}")
            if data["grand_total"] > 0:
                pct = workforce_total / data["grand_total"] * 100
                st.progress(min(pct / 100, 1.0))
                st.caption(f"{pct:.1f}% of total")

    with col3:
        with st.container(border=True):
            st.markdown("**📦 Other Expenses**")
            st.metric("Total", f"₹ {other_total:,.0f}")
            if data["grand_total"] > 0:
                pct = other_total / data["grand_total"] * 100
                st.progress(min(pct / 100, 1.0))
                st.caption(f"{pct:.1f}% of total")
