import streamlit as st

PAGES = [
    "Dashboard",
    "Cement",
    "Steel", 
    "Bricks",
    "Sand",
    "Stone",
    "Labour",
    "Electric Labour",      
    "Plumbing",
    "Paint",
    "Miscellaneous",  
    "Bulk order"
]



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

    for page in PAGES:
        if st.sidebar.button(page, use_container_width=True):
            st.session_state.menu = page    
    
    st.sidebar.divider()

    # Logout
    if st.sidebar.button("Logout", use_container_width=True):
        logout_and_redirect()
    
    return st.session_state.menu   


# Logout function
def logout_and_redirect():
    st.session_state.clear()
    st.switch_page("app.py")