import streamlit as st
from page_layouts.login_page import login_form
from components.sidebar import render_sidebar

from page_layouts.dashboard import render_dashboard
from page_layouts.cement import render_cement
from page_layouts.bricks import render_bricks
from page_layouts.steel import render_steel
from page_layouts.sand import render_sand
from page_layouts.stone import render_stone
from page_layouts.labour import render_labour
from page_layouts.electric import render_electric_expenses
from page_layouts.plumbing import render_plumbing_expenses
from page_layouts.painting import render_painting_expenses
from page_layouts.site_expenses import render_site_expenses
from page_layouts.bulk_load import render_bulk_load
from page_layouts.civil_contract import render_civil_contract

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

elif menu == "steel":
    render_steel()

elif menu == "bricks":
    render_bricks()

elif menu == "sand":
    render_sand()

elif menu == "stone":
    render_stone()

elif menu == "labour":
    render_labour()

elif menu == "electrical":
    render_electric_expenses()

elif menu == "plumbing":
    render_plumbing_expenses()

elif menu == "painting":
    render_painting_expenses()

elif menu == "site_expenses":
    render_site_expenses()

elif menu == "bulk_load":
    render_bulk_load()

elif menu == "civil_contract":
    render_civil_contract()