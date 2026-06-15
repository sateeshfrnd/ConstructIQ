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

# Cement Entry
def add_cement_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/cement_expenses", json=entry).json()

def get_cement_expenses_entry():
     return requests.get(f"{BASE_URL}/cement_expenses").json()


# Steel Entry
def add_steel_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/steel_expenses", json=entry).json()

def get_steel_expenses_entry():
     return requests.get(f"{BASE_URL}/steel_expenses").json()

# bricks Entry
def add_bricks_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/bricks_expenses", json=entry).json()

def get_bricks_expenses_entry():
     return requests.get(f"{BASE_URL}/bricks_expenses").json()

# Sand Entry
def add_sand_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/sand_expenses", json=entry).json()

def get_sand_expenses_entry():
     return requests.get(f"{BASE_URL}/sand_expenses").json()

# Stone Entry
def add_stone_expenses_entry(entry):
    response = requests.post(f"{BASE_URL}/stone_expenses", json=entry)
    try:
        return response.json()
    except ValueError:
        return {
            "error": f"Server returned non-JSON response (status {response.status_code}): {response.text}"
        }

def get_stone_expenses_entry():
     return requests.get(f"{BASE_URL}/stone_expenses").json()

# Labour Entry
def add_labour_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/labour_expenses", json=entry).json()

def get_labour_expenses_entry():
     return requests.get(f"{BASE_URL}/labour_expenses").json()

# electric Entry
def add_electric_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/electric_expenses", json=entry).json()

def get_electric_expenses_entry():
     return requests.get(f"{BASE_URL}/electric_expenses").json()

# plumbing Entry
def add_plumbing_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/plumbing_expenses", json=entry).json()

def get_plumbing_expenses_entry():
     return requests.get(f"{BASE_URL}/plumbing_expenses").json()

# painting Entry
def add_painting_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/painting_expenses", json=entry).json()

def get_painting_expenses_entry():
     return requests.get(f"{BASE_URL}/painting_expenses").json()

# Site Entry
def add_site_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/site_expenses", json=entry).json()


def get_site_expenses_entry():
     return requests.get(f"{BASE_URL}/site_expenses").json()