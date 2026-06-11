import streamlit as st
from services.api_client import login

def login_form():
    st.title("Construct IQ Login")

    email = st.text_input("Email",value="admin@example.com")
    password = st.text_input("Password", type="password", value="admin710")

    if st.button("Login"):
        res = login(email, password)

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.session_state.authenticated = True

            # Store user info in session
            st.session_state["user"] = email
            st.session_state["logged_in"] = True

            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
            