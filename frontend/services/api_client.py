import os
import requests
import streamlit as st

# Priority: Streamlit secrets > env var > default
def _get_base_url():
    try:
        return st.secrets["API_BASE_URL"]
    except (FileNotFoundError, KeyError):
        return os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")

BASE_URL = _get_base_url()

def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    return response


def get_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"}


def _safe_json(response):
    try:
        return response.json()
    except ValueError:
        return {
            "error": f"Server returned non-JSON response (status {response.status_code}): {response.text}"
        }


# Dashboard
def get_dashboard_summary():
    return requests.get(f"{BASE_URL}/dashboard/summary").json()

# =============== Cement Entry =====================
def add_cement_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/cement_expenses", json=entry).json()

def get_cement_expenses_entry():
     return requests.get(f"{BASE_URL}/cement_expenses").json()

def get_cement_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/cement_expenses/metrics", params=params).json()


# Steel Entry
def add_steel_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/steel_expenses", json=entry).json()

def get_steel_expenses_entry():
     return requests.get(f"{BASE_URL}/steel_expenses").json()

def get_steel_expenses_metrics(params):
    response = requests.get(f"{BASE_URL}/steel_expenses/metrics", params=params)
    return _safe_json(response)

# bricks Entry
def add_bricks_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/bricks_expenses", json=entry).json()

def get_bricks_expenses_entry():
     return requests.get(f"{BASE_URL}/bricks_expenses").json()

def get_bricks_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/bricks_expenses/metrics", params=params).json()

# Sand Entry
def add_sand_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/sand_expenses", json=entry).json()

def get_sand_expenses_entry():
     return requests.get(f"{BASE_URL}/sand_expenses").json()

def get_sand_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/sand_expenses/metrics", params=params).json()

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

def get_stone_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/stone_expenses/metrics", params=params).json()

# Labour Entry
def add_labour_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/labour_expenses", json=entry).json()

def get_labour_expenses_entry():
     return requests.get(f"{BASE_URL}/labour_expenses").json()

def get_labour_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/labour_expenses/metrics", params=params).json()

# electric Entry
def add_electric_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/electric_expenses", json=entry).json()

def get_electric_expenses_entry():
     return requests.get(f"{BASE_URL}/electric_expenses").json()

def get_electric_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/electric_expenses/metrics", params=params).json()

# plumbing Entry
def add_plumbing_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/plumbing_expenses", json=entry).json()

def get_plumbing_expenses_entry():
     return requests.get(f"{BASE_URL}/plumbing_expenses").json()

def get_plumbing_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/plumbing_expenses/metrics", params=params).json()

# painting Entry
def add_painting_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/painting_expenses", json=entry).json()

def get_painting_expenses_entry():
     return requests.get(f"{BASE_URL}/painting_expenses").json()

def get_painting_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/painting_expenses/metrics", params=params).json()

# Site Entry
def add_site_expenses_entry(entry):
     return requests.post(f"{BASE_URL}/site_expenses", json=entry).json()


def get_site_expenses_entry():
     return requests.get(f"{BASE_URL}/site_expenses").json()

def get_site_expenses_metrics(params):
     return requests.get(f"{BASE_URL}/site_expenses/metrics", params=params).json()


# Bulk Load
def get_bulk_load_schema(category):
    return requests.get(f"{BASE_URL}/bulk_load/schema/{category}").json()

def bulk_load_records(category, records):
    return requests.post(f"{BASE_URL}/bulk_load/{category}", json=records)


# CRUD Operations (Edit/Delete)
def update_entry(category, entry_id, updates):
    return requests.put(f"{BASE_URL}/entries/{category}/{entry_id}", json=updates)

def delete_entry(category, entry_id):
    return requests.delete(f"{BASE_URL}/entries/{category}/{entry_id}")


# Civil Contract
def create_civil_contract(data):
    return requests.post(f"{BASE_URL}/civil_contract", json=data)

def get_civil_contracts():
    return requests.get(f"{BASE_URL}/civil_contract").json()

def add_civil_contract_payment(data):
    return requests.post(f"{BASE_URL}/civil_contract/payments", json=data)

def get_civil_contract_payments(contract_id):
    return requests.get(f"{BASE_URL}/civil_contract/{contract_id}/payments").json()

def save_civil_contract_stages(contract_id, stages):
    return requests.post(f"{BASE_URL}/civil_contract/{contract_id}/stages", json={"stages": stages})

def get_civil_contract_stages(contract_id):
    return requests.get(f"{BASE_URL}/civil_contract/{contract_id}/stages").json()

def get_civil_contract_summary(contract_id):
    return requests.get(f"{BASE_URL}/civil_contract/{contract_id}/summary").json()