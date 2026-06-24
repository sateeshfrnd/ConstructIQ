import streamlit as st

if not st.session_state.get("authenticated"):
    st.warning("Please login")
    st.stop()