import streamlit as st
from page_layouts.login_page import login_form
from components.sidebar import render_sidebar

from page_layouts.dashboard import render_dashboard
from page_layouts.cement import render_cement

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Hide sidebar completely
    st.set_page_config(initial_sidebar_state="collapsed")
    login_form()
    st.stop()

if "menu" not in st.session_state:
    st.session_state.menu = "overview"

menu = render_sidebar()

if menu == "overview":
    render_dashboard()

elif menu == "cement":
    render_cement()

# elif menu == "steel":
#     render_steel()

# elif menu == "bricks":
#     render_bricks()

# elif menu == "sand":
#     render_sand()

# elif menu == "stone":
#     render_stone()

# elif menu == "labour":
#     render_labour()

# elif menu == "electric":
#     render_electric_labour()

# elif menu == "plumbing":
#     render_plumbing()

# elif menu == "paint":
#     render_paint()

# elif menu == "misc":
#     render_misc()

# elif menu == "bulk":
#     render_bulk_order()
