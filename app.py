import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from ai import DiseasePredictor  # Import the predictor class
import time  # For progress bar


st.set_page_config(
    page_title="HeyDoc - Disease Prediction",
    page_icon="🧑‍⚕️",
    layout="centered",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f9fafb;
    }
    
    .header-container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-bottom: 3px solid #3b82f6;
    }
    
    .container {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #e5e7eb;
    }
    
    .section-title {
        color: #fffff0;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .symptom-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #f8fafc;
        border-radius: 8px;
        color: #1e40af;
        font-weight: 500;
        border-left: 3px solid #3b82f6;
    }
    
    .detail-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #f8fafc;
        border-radius: 8px;
        color: #166534;
        border-left: 3px solid #10b981;
    }
    
    .risk-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #f8fafc;
        border-radius: 8px;
        color: #991b1b;
        border-left: 3px solid #ef4444;
    }
    
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
    }
    
    .prediction-result {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
        text-align: center;
        margin: 1.5rem 0;
        padding: 1rem;
        background-color: #f0fdf4;
        border-radius: 8px;
        border-left: 4px solid #10b981;
    }
    
    .stSelectbox, .stSlider {
        margin-bottom: 0.5rem;
    }
    
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    </style>
    """, unsafe_allow_html=True)

with stylable_container(
    key="header_container",
    css_styles="""
        {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            border-bottom: 3px solid #3b82f6;
        }
    """
):
    st.markdown('<h1 style="color: #111827; margin-bottom: 0.25rem;">🧑‍⚕️ HeyDoc - Disease Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #4b5563; margin-bottom: 0;">Professional health assessment tool</p>', unsafe_allow_html=True)

main_col1, main_col2 = st.columns([2, 1], gap="large")

with main_col1:
    with stylable_container(
        key="symptoms_container",
        css_styles="""
            .container {
                background-color: white;
                border: 1px solid #e5e7eb;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title">🌸 SYMPTOMS CHECKLIST</div>', unsafe_allow_html=True)
            
            symptom_col1, symptom_col2 = st.columns(2)
            
            with symptom_col1:
                fever = st.selectbox("Fever", ["No", "Yes"], key="fever")
                cough = st.selectbox("Cough", ["No", "Yes"], key="cough")
                fatigue = st.selectbox("Fatigue", ["No", "Yes"], key="fatigue")
                breathing = st.selectbox("Difficulty breathing", ["No", "Yes"], key="breathing")
                headache = st.selectbox("Headache", ["No", "Yes"], key="headache")
            
            with symptom_col2:
                rash = st.selectbox("Rash", ["No", "Yes"], key="rash")
                nausea = st.selectbox("Nausea", ["No", "Yes"], key="nausea")
                joint_pain = st.selectbox("Joint Pain", ["No", "Yes"], key="joint_pain")
                weight_change = st.selectbox("Weight change", ["No", "Yes"], key="weight_change")

with main_col2:
    with stylable_container(
        key="details_container",
        css_styles="""
            .container {
                background-color: white;
                border: 1px solid #e5e7eb;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title">📋 PERSONAL DETAILS</div>', unsafe_allow_html=True)
            age = st.slider("Your Age", min_value=20, max_value=80, value=30, key="age")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
    
    with stylable_container(
        key="risk_container",
        css_styles="""
            .container {
                background-color: white;
                border: 1px solid #e5e7eb;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title">⚠️ RISK FACTORS</div>', unsafe_allow_html=True)
            blood_pressure = st.selectbox("Blood pressure", ["Normal", "Low", "High"], key="bp")
            cholesterol = st.selectbox("Cholesterol level", ["Normal", "Low", "High"], key="chol")

active_symptoms = []
if fever == "Yes": active_symptoms.append("Fever")
if cough == "Yes": active_symptoms.append("Cough")
if fatigue == "Yes": active_symptoms.append("Fatigue")
if breathing == "Yes": active_symptoms.append("Difficulty breathing")
if headache == "Yes": active_symptoms.append("Headache")
if rash == "Yes": active_symptoms.append("Rash")
if nausea == "Yes": active_symptoms.append("Nausea")
if joint_pain == "Yes": active_symptoms.append("Joint pain")
if weight_change == "Yes": active_symptoms.append("Weight change")

with stylable_container(
    key="results_container",
    css_styles="""
        .container {
            background-color: white;
            border: 1px solid #e5e7eb;
        }
    """
):
    with st.container():
        st.markdown('<div class="section-title">✨ HEALTH SUMMARY</div>', unsafe_allow_html=True)
        
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            st.markdown("**Your symptoms:**")
            if not active_symptoms:
                st.markdown('<div style="color: #6b7280; font-style: italic;">No symptoms selected</div>', unsafe_allow_html=True)
            else:
                for symptom in active_symptoms:
                    st.markdown(f'<div class="symptom-item">• {symptom}</div>', unsafe_allow_html=True)
        
        with result_col2:
            st.markdown("**Your details:**")
            st.markdown(f'<div class="detail-item">Age: {age}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-item">Gender: {gender}</div>', unsafe_allow_html=True)
            st.markdown("**Risk factors:**")
            st.markdown(f'<div class="risk-item">Blood pressure: {blood_pressure}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="risk-item">Cholesterol: {cholesterol}</div>', unsafe_allow_html=True)

        # Add a button to trigger prediction
        predict_button = st.button("Analyze Symptoms", type="primary")

        # Initialize the predictor (we'll cache this to load only once)
        @st.cache_resource
        def load_predictor():
            return DiseasePredictor()

        predictor = load_predictor()

        if predict_button:
            # Prepare the input data
            new_patient = {
                'Fever': fever,
                'Cough': cough,
                'Fatigue': fatigue,
                'Difficulty Breathing': breathing,
                'Headache': headache,
                'Rash': rash,
                'Nausea': nausea,
                'Joint Pain': joint_pain,
                'Weight Change': weight_change,
                'Age': age,
                'Gender': gender,
                'Blood Pressure': blood_pressure,
                'Cholesterol Level': cholesterol
            }        
            # Make prediction
            prediction = predictor.predict_disease(new_patient)
            with st.spinner('Analyzing symptoms...'):
                progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.07)  # Simulate processing time
                progress_bar.progress(percent_complete + 1)
        
            # Display results in a nice container
            with stylable_container(
                key="prediction_container",
                css_styles="""
                    .container {
                        background-color: white;
                        border: 1px solid #e5e7eb;
                    }
                """
            ):
                with st.container():
                    st.markdown('<div class="section-title">🔍 PREDICTION RESULTS</div>', unsafe_allow_html=True)
                    st.markdown('Based on your symptoms and health data, the predicted condition is:')
                    st.markdown(f'<div class="prediction-result">{prediction}</div>', unsafe_allow_html=True)
                    #st.markdown('<div style="color: #6b7280; font-size: 0.85rem; text-align: center;">This is a predictive model output and should not replace professional medical advice.</div>', unsafe_allow_html=True)


st.markdown("""
    <div class="footer">
        Made by HeyDoc | Professional Health Assessment
    </div>
    """, unsafe_allow_html=True)
