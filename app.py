import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from ai import DiseasePredictor
import time
from streamlit_extras.let_it_rain import rain

# Configure page
st.set_page_config(
    page_title="HeyDoc - AI-Powered Health Assessment",
    page_icon="🧑‍⚕️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS with EXTRA LARGE, CLEAR fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #e5e7eb;
        background-color: #0f172a;
    }
    
    .stApp {
        background-color: #0f172a;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        color: #f8fafc;
    }
    
    .main {
        background-color: #0f172a;
    }
    
    .header-container {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-bottom: 3px solid #3b82f6;
    }
    
    .container {
        background-color: #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 1.5rem;
        border: 1px solid #334155;
    }
    
    .section-title {
        color: #f8fafc;
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.25rem;
        letter-spacing: 0.25px;
        border-bottom: 2px solid #334155;
        padding-bottom: 0.5rem;
    }
    
    .symptom-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #334155;
        border-radius: 8px;
        color: #93c5fd;
        font-weight: 500;
        border-left: 3px solid #3b82f6;
        font-family: 'Inter', sans-serif;
    }
    
    .detail-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #334155;
        border-radius: 8px;
        color: #86efac;
        border-left: 3px solid #10b981;
        font-family: 'Inter', sans-serif;
    }
    
    .risk-item {
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background-color: #334155;
        border-radius: 8px;
        color: #fca5a5;
        border-left: 3px solid #ef4444;
        font-family: 'Inter', sans-serif;
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
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
    }
    
    .prediction-result {
        font-size: 1.5rem;
        font-family: 'Playfair Display', serif;
        font-weight: 600;
        color: #f8fafc;
        text-align: center;
        margin: 1.5rem 0;
        padding: 1.5rem;
        background-color: #1e3a8a;
        border-radius: 8px;
        border-left: 4px solid #10b981;
    }
    
    .stSelectbox, .stSlider {
        margin-bottom: 0.5rem;
    }
    
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #334155;
        font-family: 'Inter', sans-serif;
    }
    
    /* Larger medical icon */
    .icon-large {
        font-size: 2.5rem;
        vertical-align: middle;
        margin-right: 0.5rem;
    }
    
    /* Light text for better contrast */
    .stMarkdown p, .stSelectbox label, .stSlider label {
        line-height: 1.6;
        color: #e5e7eb;
    }
    
    .stSelectbox label, .stSlider label {
        font-weight: 500;
        color: #f8fafc;
        margin-bottom: 0.25rem;
    }
    
    /* Dark theme form elements */
    .st-bd, .st-bc, .st-bb, .st-at {
        border-radius: 8px !important;
        background-color: #334155 !important;
        color: #f8fafc !important;
        border-color: #475569 !important;
    }
    
    /* Dropdown menu styling */
    .st-cj {
        background-color: #1e293b !important;
    }
    
    /* Slider track color */
    .st-emotion-cache-1m7p7tn {
        background-color: #3b82f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)
# Header with animated gradient
with stylable_container(
    key="header_container",
    css_styles="""
        {
            background-color: #1e293b;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            border-bottom: 3px solid #3b82f6;
        }
    """
):
    st.markdown('<h1 style="color: #f8fafc; margin-bottom: 0.25rem;"><span class="icon-large">🧑‍⚕️</span> HeyDoc - Disease Prediction</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; margin-bottom: 0;">Professional health assessment tool</p>', unsafe_allow_html=True)
main_col1, main_col2 = st.columns([2, 1], gap="large")

with main_col1:
    with stylable_container(
        key="symptoms_container",
        css_styles="""
            .container {
                background: white;
                border: none;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title"><span class="emoji-icon">🌸</span> SYMPTOMS CHECKLIST</div>', unsafe_allow_html=True)
            
            symptom_col1, symptom_col2 = st.columns(2)
            
            with symptom_col1:
                fever = st.selectbox("Fever", ["No", "Yes"], key="fever", help="Have you had a fever above 100.4°F (38°C)?")
                cough = st.selectbox("Cough", ["No", "Yes"], key="cough", help="Persistent cough lasting more than a few days?")
                fatigue = st.selectbox("Fatigue", ["No", "Yes"], key="fatigue", help="Unusual tiredness or lack of energy?")
                breathing = st.selectbox("Difficulty breathing", ["No", "Yes"], key="breathing", help="Shortness of breath or labored breathing?")
                headache = st.selectbox("Headache", ["No", "Yes"], key="headache", help="Persistent or severe headaches?")
            
            with symptom_col2:
                rash = st.selectbox("Rash", ["No", "Yes"], key="rash", help="Any unexplained skin rash or irritation?")
                nausea = st.selectbox("Nausea", ["No", "Yes"], key="nausea", help="Feeling sick to your stomach?")
                joint_pain = st.selectbox("Joint Pain", ["No", "Yes"], key="joint_pain", help="Pain or discomfort in your joints?")
                weight_change = st.selectbox("Weight change", ["No", "Yes"], key="weight_change", help="Significant unintentional weight loss or gain?")

with main_col2:
    with stylable_container(
        key="details_container",
        css_styles="""
            .container {
                background: white;
                border: none;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title"><span class="emoji-icon">📋</span> PERSONAL DETAILS</div>', unsafe_allow_html=True)
            age = st.slider("Your Age", min_value=20, max_value=80, value=30, key="age", help="Age can affect disease risk factors")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gender", help="Some conditions are gender-specific")
    
    with stylable_container(
        key="risk_container",
        css_styles="""
            .container {
                background: white;
                border: none;
            }
        """
    ):
        with st.container():
            st.markdown('<div class="section-title"><span class="emoji-icon">⚠️</span> RISK FACTORS</div>', unsafe_allow_html=True)
            blood_pressure = st.selectbox("Blood pressure", ["Normal", "Low", "High"], key="bp", help="Current blood pressure status")
            cholesterol = st.selectbox("Cholesterol level", ["Normal", "Low", "High"], key="chol", help="Current cholesterol level")

# Active symptoms list
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

# Results section
with stylable_container(
    key="results_container",
    css_styles="""
        .container {
            background: white;
            border: none;
        }
    """
):
    with st.container():
        st.markdown('<div class="section-title"><span class="emoji-icon">✨</span> HEALTH SUMMARY</div>', unsafe_allow_html=True)
        
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            st.markdown("**Your symptoms:**")
            if not active_symptoms:
                st.markdown('<div style="color: #6b7280; font-style: italic; padding: 1rem;">No symptoms selected</div>', unsafe_allow_html=True)
            else:
                for symptom in active_symptoms:
                    st.markdown(f'<div class="symptom-item">• {symptom}</div>', unsafe_allow_html=True)
        
        with result_col2:
            st.markdown("**Your details:**")
            st.markdown(f'<div class="detail-item">• Age: {age}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="detail-item">• Gender: {gender}</div>', unsafe_allow_html=True)
            st.markdown("**Risk factors:**")
            st.markdown(f'<div class="risk-item">• Blood pressure: {blood_pressure}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="risk-item">• Cholesterol: {cholesterol}</div>', unsafe_allow_html=True)

        # Prediction button centered
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            predict_button = st.button("Analyze My Symptoms", type="primary", use_container_width=True)

        # Initialize the predictor
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
            
            # Animated progress bar
            with st.spinner('Analyzing symptoms with AI...'):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.03)  # Faster animation
                    progress_bar.progress(percent_complete + 1)
            
            # Make prediction
            prediction = predictor.predict_disease(new_patient)
            
            # Celebration animation
            rain(
                emoji="🎉",
                font_size=20,
                falling_speed=5,
                animation_length=1,
            )
            
            # Display results with animation
            with stylable_container(
                key="prediction_container",
                css_styles="""
                    .container {
                        background: white;
                        border: none;
                    }
                """
            ):
                with st.container():
                    st.markdown('<div class="section-title"><span class="emoji-icon">🔍</span> AI HEALTH ASSESSMENT</div>', unsafe_allow_html=True)
                    st.markdown('Based on advanced analysis of your symptoms and health profile:')
                    st.markdown(f'<div class="prediction-result success-animation">{prediction}</div>', unsafe_allow_html=True)
                    
                    # Additional recommendations
                    with st.expander("📌 Health Recommendations"):
                        st.markdown("""
                        - **Consult a healthcare professional** for proper diagnosis
                        - Drink plenty of water and rest
                        - Monitor your symptoms for changes
                        - Consider preventive health measures
                        """)
                    
                    st.markdown("""
                    <div style="text-align: center; color: #6b7280; font-size: 0.85rem; margin-top: 1rem;">
                        <i>This AI assessment is for informational purposes only and not a substitute for professional medical advice.</i>
                    </div>
                    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown("""
    <div class="footer">
        <div style="margin-bottom: 0.5rem;">
            <!-- <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Privacy Policy</a> • -->
            <!-- <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Terms of Service</a> • -->
            <!-- <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Contact Us</a>-->
        </div>
        © 2023 HeyDoc Health Technologies. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
