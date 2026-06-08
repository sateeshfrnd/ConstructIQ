import streamlit as st

# 🧭 Central page config (easy to manage)
PAGES = {
    "Dashboard": "pages/dashboard.py",
    # "Cement": "pages/cement.py",
    # "Steel": "pages/steel.py",
    # "Sand": "pages/sand.py",
    # "Bricks": "pages/bricks.py",
    # "Stone": "pages/stone.py",
    # "Construction Labour": "pages/construction_labour.py",
    # "Electric Labour": "pages/electric_labour.py",
    # "Miscellaneous": "pages/miscellaneous.py",
    # "Bulk Order": "pages/bulk_order.py",
}


# PAGES = {
#     "admin": {
#         "Dashboard": "pages/dashboard.py",
#         # "Bulk Order": "pages/bulk_order.py",
#     },
#     "user": {
#         "Dashboard": "pages/dashboard.py",
#         # "Cement": "pages/cement.py",
#         # "Steel": "pages/steel.py",
#     }
# }

def render_sidebar():
    # 🚫 Protect sidebar (only after login)
    if not st.session_state.get("authenticated"):
        return

    with st.sidebar:
        st.title("🏗️ Construct IQ")

        # 👤 User Info
        user = st.session_state.get("user", "User")
        st.markdown(f"👤 **{user}**")

        st.divider()

        # 📌 Navigation
        st.subheader("📊 Menu")

        # role = st.session_state.get("role", "user")

        # for page_name, page_path in PAGES.get(role, {}).items():
        #     if st.button(page_name, use_container_width=True):
        #         st.switch_page(page_path)

        # current_page = st.session_state.get("current_page", "Dashboard")

        for page_name, page_path in PAGES.items():
            if st.button(page_name, use_container_width=True):
                st.session_state.current_page = page_name
                st.switch_page(page_path)

        st.divider()

        # 🚪 Logout
        if st.button("🚪 Logout", use_container_width=True):
            logout_and_redirect()


# 🔐 Logout function
def logout_and_redirect():
    st.session_state.clear()
    st.switch_page("app.py")