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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* BASE FONT SIZE INCREASED TO 20PX */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        font-size: 20px !important;
    }
    
    /* SUPER LARGE HEADINGS */
    h1 {
        font-size: 2.8rem !important;  /* 45px */
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }
    
    /* SECTION TITLES */
    .section-title {
        color: #3b82f6;
        font-weight: 700 !important;
        margin-bottom: 1.5rem;
        font-size: 1.8rem !important;  /* 29px */
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* FORM ELEMENTS */
    .stSelectbox, .stSlider {
        font-size: 1.2rem !important;  /* 19px */
    }
    
    .stSelectbox>div>div {
        padding: 1rem 1.25rem !important;
        font-size: 1.2rem !important;
    }
    
    /* SYMPTOM ITEMS */
    .symptom-item, .detail-item, .risk-item {
        padding: 1.25rem !important;
        margin: 1rem 0 !important;
        font-size: 1.3rem !important;  /* 21px */
        border-left-width: 5px !important;
    }
    
    /* PREDICTION RESULT - VERY LARGE */
    .prediction-result {
        font-size: 2.2rem !important;  /* 35px */
        padding: 2rem !important;
    }
    
    /* BUTTON TEXT */
    .stButton>button {
        font-size: 1.4rem !important;  /* 22px */
        padding: 1.5rem !important;
    }
    
    /* FOOTER */
    .footer {
        font-size: 1.1rem !important;  /* 18px */
    }
    
    /* TOOLTIPS */
    .stTooltip {
        font-size: 1.1rem !important;
    }
    
    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        html, body, [class*="css"] {
            font-size: 18px !important;
        }
        h1 {
            font-size: 2.2rem !important;
        }
        .section-title {
            font-size: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
# Header with animated gradient
with stylable_container(
    key="header_container",
    css_styles="""
        {
            background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
            border-radius: 16px;
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.15);
            color: white;
            animation: gradient 8s ease infinite;
            background-size: 200% 200%;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    """
):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="floating">🧑‍⚕️</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<h1 style="color: white; margin-bottom: 0.25rem;">HeyDoc Health AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #e0e7ff; margin-bottom: 0;">Advanced symptom analysis and health assessment</p>', unsafe_allow_html=True)

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
            <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Privacy Policy</a> • 
            <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Terms of Service</a> • 
            <a href="#" style="color: #3b82f6; text-decoration: none; margin: 0 0.5rem;">Contact Us</a>
        </div>
        © 2023 HeyDoc Health Technologies. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
