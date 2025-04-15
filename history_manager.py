import json
import base64
import datetime
import streamlit as st
from constants import TIMEZONE

@st.cache_data(ttl=300)
def load_user_history():
    try:
        with open('user_history.json', 'r') as file:
            data = json.load(file)
            return data.get('users', [])
    except FileNotFoundError:
        save_user_history([])
        return []
    except json.JSONDecodeError:
        st.error("Invalid JSON format in user_history.json!")
        return []

def save_user_history(users):
    try:
        with open('user_history.json', 'w') as file:
            json.dump({"users": users}, file, indent=2)
        load_user_history.clear()
    except Exception as e:
        st.error(f"Error saving user history: {str(e)}")

def add_user_illness(username, disease, symptoms, treatment_pdf_data, illness_pdf_data):
    history = load_user_history()
    user_entry = next((u for u in history if u['username'] == username), None)
    timestamp = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")
    
    illness_entry = {
        "disease": disease,
        "timestamp": timestamp,
        "symptoms": symptoms,
        "treatment_pdf": base64.b64encode(treatment_pdf_data.getvalue()).decode('utf-8'),
        "illness_pdf": base64.b64encode(illness_pdf_data.getvalue()).decode('utf-8')
    }
    
    if user_entry:
        user_entry['illnesses'].append(illness_entry)
    else:
        history.append({
            "username": username,
            "illnesses": [illness_entry]
        })
    
    save_user_history(history)

def get_user_illness_history(username):
    history = load_user_history()
    user_entry = next((u for u in history if u['username'] == username), None)
    return user_entry['illnesses'] if user_entry else []