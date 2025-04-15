import json
import streamlit as st
import pytz

TIMEZONE = pytz.timezone('Asia/Colombo')

SYMPTOMS = [
    "Fever",
    "Cough",
    "Fatigue",
    "Difficulty breathing",
    "Headache",
    "Rash",
    "Nausea",
    "Joint pain",
    "Weight change"
]

@st.cache_data
def load_disease_info():
    try:
        with open('disease_info.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Disease information file not found. Using fallback data.")
        return {
            "Common Cold": {
                "description": "A viral infection of your nose and throat.",
                "symptoms": ["Runny nose", "Sore throat", "Cough"],
                "remedies": ["Rest", "Drink fluids"],
                "when_to_see_doctor": "If symptoms persist"
            }
        }

DISEASE_INFO = load_disease_info()