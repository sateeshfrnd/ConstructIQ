import streamlit as st

MENU = {
    "Overview": {
        "Project Overview": "overview",
        "Budget vs Actual": "budget"
    },
    "Materials": {
        "Cement & Concrete": "cement",
        "Steel & Reinforcement": "steel",
        "Brickwork": "bricks",
        "Sand Supply": "sand",
        "Aggregates & Stone": "stone"
    },
    "Workforce": {
        "General Labour": "labour",
        "Electrical Work": "electrical",
        "Plumbing Work": "plumbing",
        "Painting & Finishing": "painting"
    },
    "Other Expenses" : {
        "Site Expenses": "site_expenses",
    }
}

# Function to load CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_sidebar():    
    # Protect sidebar (only after login)
    if not st.session_state.get("authenticated"):
        return
    
    st.set_page_config(layout="wide")

    if "menu" not in st.session_state:
        st.session_state.menu = "Dashboard"
    
    load_css("assets/styles.css")
    st.sidebar.markdown('<div class="sidebar-title"> Construct IQ</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-caption">Build smart. Spend smarter.</div>', unsafe_allow_html=True)

    # Display User Info
    user = st.session_state.get("user", "User")
    st.sidebar.markdown(
        f'<div class="email-text">{user}</div>',
        unsafe_allow_html=True
    )    

    st.sidebar.divider()
   
    for section, items in MENU.items():
        with st.sidebar.expander(section, expanded=(section == "📊 Overview")):
            for item, key in items.items():
                if st.button(item, use_container_width=True):
                    st.session_state.menu = key

    st.sidebar.divider()

    # Logout
    if st.sidebar.button("Logout", use_container_width=True):
        logout_and_redirect()
    
    return st.session_state.menu   


# Logout function
def logout_and_redirect():
    st.session_state.clear()
    st.switch_page("app.py")