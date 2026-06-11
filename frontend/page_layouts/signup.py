import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

def render_signup():
    st.title("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        response = requests.post(
            f"{API_URL}/signup",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            st.success("Account created successfully!")
        else:
            st.error(response.json().get("detail", "Signup failed."))
