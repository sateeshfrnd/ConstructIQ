import streamlit as st

def render_dashboard():
    if not st.session_state.get("authenticated"):
        st.warning("Please login")
        st.stop()

    st.title("Construct IQ Dashboard")
    st.write("Welcome to the dashboard! Here you can access various features and insights related to your construction projects.")

    