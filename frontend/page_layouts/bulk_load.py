import streamlit as st
import pandas as pd

from services.api_client import get_bulk_load_schema, bulk_load_records

BULK_LOAD_CATEGORIES = {
    "Cement": "cement",
    "Bricks": "bricks",
    "Steel": "steel",
    "Sand": "sand",
    "Stone": "stone",
    "Labour": "labour",
    "Electric": "electric",
    "Plumbing": "plumbing",
    "Painting": "painting",
    "Site Expenses": "site_expenses",
}


def render_bulk_load():
    st.title("📤 Bulk Load")
    st.caption("Upload CSV or Excel files to bulk-load historical expense data.")

    # Step 1: Select category
    selected_label = st.selectbox(
        "Select Category",
        list(BULK_LOAD_CATEGORIES.keys()),
        index=None,
        placeholder="Choose a category..."
    )

    if not selected_label:
        st.info("Select a category to get started.")
        return

    category_key = BULK_LOAD_CATEGORIES[selected_label]

    # Fetch expected schema for selected category
    schema_response = get_bulk_load_schema(category_key)
    expected_columns = schema_response.get("columns", [])

    # Show expected columns
    with st.expander("📋 Expected Columns", expanded=True):
        st.write("Your file must contain these columns:")
        cols = st.columns(3)
        for i, col_name in enumerate(expected_columns):
            cols[i % 3].code(col_name)

    st.divider()

    # Step 2: Upload file
    uploaded_file = st.file_uploader(
        f"Upload {selected_label} data",
        type=["csv", "xlsx", "xls"],
        key=f"bulk_upload_{category_key}"
    )

    if uploaded_file is None:
        return

    # Step 3: Parse the file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to parse file: {e}")
        return

    if df.empty:
        st.warning("⚠️ The uploaded file is empty.")
        return

    # Step 4: Validate columns
    file_columns = set(df.columns.str.strip())
    expected_set = set(expected_columns)
    missing_cols = expected_set - file_columns
    extra_cols = file_columns - expected_set

    if missing_cols:
        st.error(f"❌ Missing required columns: **{', '.join(sorted(missing_cols))}**")
        st.write("Your file has:", sorted(file_columns))
        return

    if extra_cols:
        st.warning(f"⚠️ Extra columns will be ignored: {', '.join(sorted(extra_cols))}")

    # Keep only expected columns
    df = df[expected_columns]

    # Check for null values in required fields
    null_counts = df.isnull().sum()
    cols_with_nulls = null_counts[null_counts > 0]
    if not cols_with_nulls.empty:
        st.warning("⚠️ Some rows have empty values:")
        st.dataframe(cols_with_nulls.reset_index().rename(
            columns={"index": "Column", 0: "Empty Rows"}
        ), hide_index=True)

    # Step 5: Preview data
    st.subheader("📊 Data Preview")
    st.write(f"**{len(df)} records** found in the file")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Step 6: Load to DB
    col1, col2 = st.columns([1, 4])
    with col1:
        load_btn = st.button("🚀 Load to Database", type="primary")

    if load_btn:
        # Convert DataFrame to list of dicts
        records = df.fillna("").to_dict(orient="records")

        # Convert date columns to string if they're datetime
        for record in records:
            for key, value in record.items():
                if hasattr(value, 'strftime'):
                    record[key] = value.strftime("%Y-%m-%d")
                elif pd.isna(value):
                    record[key] = ""

        with st.spinner(f"Loading {len(records)} records..."):
            response = bulk_load_records(category_key, records)

        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
            st.balloons()
        else:
            try:
                error_detail = response.json().get("detail", "Unknown error")
            except Exception:
                error_detail = response.text
            st.error(f"❌ Failed to load data: {error_detail}")
