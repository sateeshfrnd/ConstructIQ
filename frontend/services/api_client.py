import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    return response


def get_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"}