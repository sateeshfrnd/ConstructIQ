import streamlit as st
import pandas as pd
from services.api_client import update_entry, delete_entry


def render_editable_history(data, category_key, title="Expense History"):
    """
    Render an expense history table with edit/delete actions.
    
    Args:
        data: List of dicts from the API
        category_key: Category string for API calls (e.g., "cement", "bricks")
        title: Section title
    """
    st.subheader(title)

    if not data:
        st.info("No expenses added yet.")
        return

    df = pd.DataFrame(data=data)

    # Initialize session state for edit mode
    edit_key = f"edit_{category_key}"
    if edit_key not in st.session_state:
        st.session_state[edit_key] = None

    # If in edit mode, show edit form
    if st.session_state[edit_key] is not None:
        _render_edit_form(df, category_key, edit_key)
        return

    # Display table with action buttons
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.write("")
    st.caption("Select an entry to edit or delete:")

    # Entry selector
    entry_ids = df["id"].tolist()
    selected_id = st.selectbox(
        "Select Entry ID",
        options=[None] + entry_ids,
        format_func=lambda x: "-- Choose --" if x is None else f"ID: {x}",
        key=f"select_{category_key}"
    )

    if selected_id is not None:
        # Show selected row preview
        selected_row = df[df["id"] == selected_id].iloc[0]
        with st.expander(f"Entry #{selected_id} details", expanded=True):
            cols = st.columns(3)
            for i, (col_name, value) in enumerate(selected_row.items()):
                if col_name != "id":
                    cols[i % 3].write(f"**{col_name}:** {value}")

        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("✏️ Edit", key=f"edit_btn_{category_key}"):
                st.session_state[edit_key] = selected_id
                st.rerun()
        with col2:
            if st.button("🗑️ Delete", type="secondary", key=f"del_btn_{category_key}"):
                response = delete_entry(category_key, selected_id)
                if response.status_code == 200:
                    st.success(f"✅ Entry #{selected_id} deleted")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete: {response.text}")


def _render_edit_form(df, category_key, edit_key):
    """Render an inline edit form for the selected entry."""
    entry_id = st.session_state[edit_key]
    row = df[df["id"] == entry_id]

    if row.empty:
        st.error("Entry not found")
        st.session_state[edit_key] = None
        return

    row = row.iloc[0]

    st.markdown(f"### ✏️ Editing Entry #{entry_id}")

    with st.form(f"edit_form_{category_key}_{entry_id}"):
        updated_values = {}
        cols = st.columns(2)
        col_idx = 0

        for col_name, value in row.items():
            if col_name == "id":
                continue
            with cols[col_idx % 2]:
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    updated_values[col_name] = st.number_input(
                        col_name, value=float(value),
                        key=f"edit_{category_key}_{entry_id}_{col_name}"
                    )
                else:
                    updated_values[col_name] = st.text_input(
                        col_name, value=str(value) if value else "",
                        key=f"edit_{category_key}_{entry_id}_{col_name}"
                    )
            col_idx += 1

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Save Changes", type="primary")
        with col2:
            cancelled = st.form_submit_button("❌ Cancel")

        if submitted:
            response = update_entry(category_key, entry_id, updated_values)
            if response.status_code == 200:
                st.success(f"✅ Entry #{entry_id} updated successfully")
                st.session_state[edit_key] = None
                st.rerun()
            else:
                st.error(f"❌ Failed to update: {response.text}")

        if cancelled:
            st.session_state[edit_key] = None
            st.rerun()
