import streamlit as st
import utils.auth as auth

def render_dashboard():
    auth.show_dashboard()
    st.title("Construct IQ Dashboard")
    st.write("Welcome to the dashboard! Here you can access various features and insights related to your construction projects.")  

    
def show_dashboard():
    if not st.session_state.get("authenticated"):
        # st.warning("Please login")
        # st.stop()
        st.switch_page("app.py")
    else:
        render_dashboard()

    