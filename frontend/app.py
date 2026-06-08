import streamlit as st
from page_layouts.login_page import login_form
from components.sidebar import render_sidebar
from components.signup import render_signup

# menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

# if menu == "Login":
#     login_form()
# else:
#     render_signup()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Hide sidebar completely
    st.set_page_config(initial_sidebar_state="collapsed")
    login_form()
    st.stop()

# After login → load app
render_sidebar()