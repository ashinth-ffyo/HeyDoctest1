import streamlit as st

st.set_page_config(
    page_title="HeyDoc - AI-Powered Diagnosis",
    page_icon="🧑‍⚕️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.let_it_rain import rain
import time
from user_manager import validate_login, load_users, get_user, is_admin_user
from email_manager import send_diagnosis_email, send_confirmation_email, generate_confirmation_token, store_pending_user, confirm_user
from pdf_generator import generate_treatment_pdf, generate_illness_pdf
from history_manager import get_user_illness_history, add_user_illness
from constants import DISEASE_INFO, SYMPTOMS, TIMEZONE
from ai import DiseasePredictor
import re
import datetime
import base64


with open("styles.css", "r") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

def login_ui():
    st.title("Login or Create Account")
    login_tab, create_tab, confirm_tab = st.tabs(["Login", "Create Account", "Confirm Account"])

    with login_tab:
        st.header("Login")
        with st.form(key='login_form'):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button(label="Login")

            if submit_button:
                if username and password:
                    if validate_login(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please fill in all fields")

    with create_tab:
        st.header("Create Account")
        with st.form(key='create_account_form'):
            new_username = st.text_input("New Username", key="create_username")
            new_password = st.text_input("New Password", type="password", key="create_password")
            new_email = st.text_input("Email Address", key="create_email")
            create_button = st.form_submit_button(label="Create Account")

            if create_button:
                if new_username and new_password and new_email:
                    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if not re.match(email_regex, new_email):
                        st.error("Invalid email format!")
                    else:
                        users = load_users()
                        if any(u['username'].lower() == new_username.lower() or u['email'] == new_email for u in users):
                            st.error("Username or email already exists!")
                        else:
                            token = generate_confirmation_token()
                            success, message = store_pending_user(new_username, new_password, new_email, token)
                            if success:
                                success, email_message = send_confirmation_email(new_email, new_username, token)
                                if success:
                                    st.success("Please check your email for a confirmation link.")
                                else:
                                    st.error(email_message)
                            else:
                                st.error(message)
                else:
                    st.error("Please fill in all fields")

    with confirm_tab:
        st.header("Confirm Account")
        with st.form(key='confirm_account_form'):
            confirm_username = st.text_input("Username", key="confirm_username")
            confirm_token = st.text_input("Confirmation Token", key="confirm_token")
            confirm_button = st.form_submit_button(label="Confirm Account")

            if confirm_button:
                if confirm_username and confirm_token:
                    success, message = confirm_user(confirm_username, confirm_token)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                else:
                    st.error("Please fill in all fields")

def dashboard_ui(username):
    illnesses = get_user_illness_history(username)
    with stylable_container(key="dashboard_container", css_styles=".container { background-color: #1e293b; border: none; }"):
        with st.container():
            st.markdown('<div class="section-title">📜 Your Health History</div>', unsafe_allow_html=True)
            if not illnesses:
                st.info("No illness history available.")
            else:
                for idx, illness in enumerate(illnesses):
                    with st.expander(f"📅 {illness['disease']} - {illness['timestamp']}", expanded=False):
                        with stylable_container(
                            key=f"history_card_{idx}",
                            css_styles=".history-card { background-color: #1e293b; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border-left: 4px solid #3b82f6; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2); }"
                        ):
                            st.markdown(f"**Disease**: {illness['disease']}")
                            st.markdown(f"**Date**: {illness['timestamp']}")
                            st.markdown("**Symptoms Reported**:")
                            if illness['symptoms']:
                                for symptom in illness['symptoms']:
                                    st.markdown(f'<div class="history-symptom">• {symptom}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div style="color: #6b7280; font-style: italic;">No symptoms recorded</div>', unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    label="Download Treatment Plan PDF",
                                    data=base64.b64decode(illness["treatment_pdf"]),
                                    file_name=f"HeyDoc_Treatment_Plan_{illness['disease']}_{illness['timestamp'].replace(' ', '_').replace(':', '-')}.pdf",
                                    mime="application/pdf",
                                    key=f"treatment_pdf_history_{idx}",
                                    type="primary",
                                    use_container_width=True
                                )
                            with col2:
                                st.download_button(
                                    label="Download Illness Info PDF",
                                    data=base64.b64decode(illness["illness_pdf"]),
                                    file_name=f"HeyDoc_Illness_Info_{illness['disease']}_{illness['timestamp'].replace(' ', '_').replace(':', '-')}.pdf",
                                    mime="application/pdf",
                                    key=f"illness_pdf_history_{idx}",
                                    type="primary",
                                    use_container_width=True
                                )

def predict_disease_ui(username, predictor):
    from user_manager import increment_usage_count, get_usage_count
    user = get_user(username)
    is_admin = is_admin_user(username)
    
    main_col1, main_col2 = st.columns([2, 1], gap="large")
    active_symptoms = []
    
    with main_col1:
        with stylable_container(key="symptoms_container", css_styles=".container { background-color: #1e293b; border: none; }"):
            with st.container():
                st.markdown('<div class="section-title">🌸 SYMPTOMS CHECKLIST</div>', unsafe_allow_html=True)
                symptom_col1, symptom_col2 = st.columns(2)
                with symptom_col1:
                    for symptom in SYMPTOMS[:len(SYMPTOMS)//2]:
                        value = st.selectbox(symptom, ["No", "Yes"], key=symptom.lower().replace(" ", "_"))
                        if value == "Yes":
                            active_symptoms.append(symptom)
                with symptom_col2:
                    for symptom in SYMPTOMS[len(SYMPTOMS)//2:]:
                        value = st.selectbox(symptom, ["No", "Yes"], key=symptom.lower().replace(" ", "_"))
                        if value == "Yes":
                            active_symptoms.append(symptom)

    with main_col2:
        with stylable_container(key="details_container", css_styles=".container { background-color: #1e293b; border: none; }"):
            with st.container():
                st.markdown('<div class="section-title">📋 PERSONAL DETAILS</div>', unsafe_allow_html=True)
                age = st.slider("Your Age", min_value=20, max_value=80, value=30, key="age")
                gender = st.selectbox("Gender", ["Male", "Female"], key="gender")
        
        with stylable_container(key="risk_container", css_styles=".container { background-color: #1e293b; border: none; }"):
            with st.container():
                st.markdown('<div class="section-title">⚠️ RISK FACTORS</div>', unsafe_allow_html=True)
                blood_pressure = st.selectbox("Blood pressure", ["Normal", "Low", "High"], key="bp")
                cholesterol = st.selectbox("Cholesterol level", ["Normal", "Low", "High"], key="chol")

    with stylable_container(key="results_container", css_styles=".container { background-color: #1e293b; border: none; }"):
        with st.container():
            st.markdown('<div class="section-title">✨ HEALTH SUMMARY</div>', unsafe_allow_html=True)
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

            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                predict_button = st.button("Analyze My Symptoms", type="primary", use_container_width=True)

            if 'prediction' not in st.session_state:
                st.session_state.prediction = None
            if 'show_treatment' not in st.session_state:
                st.session_state.show_treatment = False

            if predict_button:
                if not active_symptoms:
                    st.warning("Please select at least one symptom.")
                elif user and not is_admin and get_usage_count(username) >= 1:
                    st.error("Usage limit reached. Contact admin.")
                else:
                    new_patient = {
                        'Fever': 'Yes' if 'Fever' in active_symptoms else 'No',
                        'Cough': 'Yes' if 'Cough' in active_symptoms else 'No',
                        'Fatigue': 'Yes' if 'Fatigue' in active_symptoms else 'No',
                        'Difficulty Breathing': 'Yes' if 'Difficulty breathing' in active_symptoms else 'No',
                        'Headache': 'Yes' if 'Headache' in active_symptoms else 'No',
                        'Rash': 'Yes' if 'Rash' in active_symptoms else 'No',
                        'Nausea': 'Yes' if 'Nausea' in active_symptoms else 'No',
                        'Joint Pain': 'Yes' if 'Joint pain' in active_symptoms else 'No',
                        'Weight Change': 'Yes' if 'Weight change' in active_symptoms else 'No',
                        'Age': age,
                        'Gender': gender,
                        'Blood Pressure': blood_pressure,
                        'Cholesterol Level': cholesterol
                    }
                    with st.spinner('Analyzing symptoms with AI...'):
                        progress_bar = st.progress(0)
                        for percent_complete in range(100):
                            time.sleep(0.06)
                            progress_bar.progress(percent_complete + 1)
                    
                    prediction = predictor.predict_disease(new_patient)
                    st.session_state.prediction = prediction
                    st.session_state.show_treatment = False
                    
                    increment_usage_count(username)
                    
                    disease_data = DISEASE_INFO.get(prediction, None)
                    treatment_pdf = generate_treatment_pdf(prediction, disease_data, username)
                    illness_pdf = generate_illness_pdf(prediction, disease_data, username)
                    add_user_illness(username, prediction, active_symptoms, treatment_pdf, illness_pdf)
                    
                    if user and 'email' in user:
                        success, message = send_diagnosis_email(
                            user['email'], username, prediction, active_symptoms, treatment_pdf, illness_pdf
                        )
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    else:
                        st.warning("No email found. Update your profile.")
                    
                    rain(emoji="🎉", font_size=20, falling_speed=5, animation_length=1)
                    
                    with stylable_container(key="prediction_container", css_styles=".container { background-color: #1e293b; border: none; }"):
                        with st.container():
                            st.markdown('<div class="section-title">🔍 AI HEALTH ASSESSMENT</div>', unsafe_allow_html=True)
                            st.markdown('Based on advanced analysis of your symptoms and health profile:')
                            st.markdown(f'<div class="prediction-result">{prediction}</div>', unsafe_allow_html=True)
                            if disease_data:
                                with st.expander("📌 Detailed Information", expanded=True):
                                    st.subheader("Description")
                                    for desc in disease_data.get("definition", []):
                                        st.markdown(f"- {desc}")
                                    st.subheader("Common Symptoms")
                                    for symptom in disease_data.get("symptoms", []):
                                        st.markdown(f"- {symptom}")
                                    st.subheader("Causes")
                                    for cause in disease_data.get("causes", []):
                                        st.markdown(f"- {cause}")
                                    st.subheader("Risk Factors")
                                    for risk in disease_data.get("risk_factors", []):
                                        st.markdown(f"- {risk}")
                            else:
                                st.warning("No detailed information available.")
                            st.markdown("""
                                <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 1rem;">
                                    <strong>Disclaimer:</strong> This AI assessment is not a substitute for professional medical advice.
                                </div>
                            """, unsafe_allow_html=True)

            if st.session_state.prediction:
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    treatment_button = st.button(
                        "View Treatment Plan", key="treatment_button", type="secondary", use_container_width=True
                    )
                    if treatment_button:
                        st.session_state.show_treatment = True
                    disease_data = DISEASE_INFO.get(st.session_state.prediction, None)
                    treatment_pdf = generate_treatment_pdf(st.session_state.prediction, disease_data, username)
                    st.download_button(
                        label="Download Treatment Plan PDF",
                        data=treatment_pdf,
                        file_name=f"HeyDoc_Treatment_Plan_{st.session_state.prediction}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="treatment_pdf_button",
                        type="primary",
                        use_container_width=True
                    )
                    illness_pdf = generate_illness_pdf(st.session_state.prediction, disease_data, username)
                    st.download_button(
                        label="Download Illness Info PDF",
                        data=illness_pdf,
                        file_name=f"HeyDoc_Illness_Info_{st.session_state.prediction}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        key="illness_pdf_button",
                        type="primary",
                        use_container_width=True
                    )

            if st.session_state.show_treatment and st.session_state.prediction:
                with stylable_container(key="treatment_container", css_styles=".container { background-color: #1e293b; border: none; }"):
                    with st.container():
                        st.markdown('<div class="section-title">💊 TREATMENT PLAN</div>', unsafe_allow_html=True)
                        disease_data = DISEASE_INFO.get(st.session_state.prediction, None)
                        if disease_data and "treatment" in disease_data:
                            for treatment in disease_data["treatment"]:
                                st.markdown(f'<div class="remedy-item">{treatment}</div>', unsafe_allow_html=True)
                            st.subheader("Prevention Tips")
                            for prevention in disease_data.get("prevention", []):
                                st.markdown(f"- {prevention}")
                            st.subheader("When to See a Doctor")
                            st.warning("Consult a healthcare provider if symptoms persist.")
                        else:
                            st.warning("No treatment information available.")
                        st.markdown("""
                            <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 1rem;">
                                <strong>Note:</strong> Follow professional medical advice.
                            </div>
                        """, unsafe_allow_html=True)

def profile_ui(username):
    from user_manager import update_user_profile, get_user
    user = get_user(username)
    with stylable_container(key="profile_container", css_styles=".container { background-color: #1e293b; border: none; }"):
        with st.container():
            st.markdown('<div class="section-title">👤 Your Profile</div>', unsafe_allow_html=True)
            if user:
                st.markdown(f"**Username**: {user['username']}")
                st.markdown(f"**Email**: {user.get('email', 'Not set')}")
                st.markdown(f"**Usage Count**: {user.get('usage_count', 'Unlimited' if user.get('is_admin', False) else 0)}")
                st.markdown(f"**Admin Status**: {'Yes' if user.get('is_admin', False) else 'No'}")
            else:
                st.error("User profile not found!")
            st.markdown("### Update Profile")
            with st.form(key='profile_form'):
                new_email = st.text_input("New Email Address", key="profile_email")
                new_password = st.text_input("New Password", type="password", key="profile_password")
                update_button = st.form_submit_button(label="Update Profile")
                if update_button:
                    if not new_email and not new_password:
                        st.warning("Provide at least one field to update.")
                    else:
                        success, message = update_user_profile(username, new_email, new_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

def admin_ui(username):
    from user_manager import load_users, delete_user, toggle_admin_status, reset_user_usage, reset_all_usage, load_pending_users, approve_pending_user, reject_pending_user
    with stylable_container(key="admin_container", css_styles=".container { background-color: #1e293b; border: none; }"):
        with st.container():
            st.markdown('<div class="section-title">🛠️ Admin Dashboard</div>', unsafe_allow_html=True)
            st.markdown("### User Statistics")
            users = load_users()
            st.write(f"**Total Users**: {len(users)}")
            st.markdown("### User Details")
            for u in users:
                usage = "Unlimited" if u.get('is_admin', False) else u.get('usage_count', 0)
                st.markdown(f"- **{u['username']}**: {usage} predictions, Email: {u.get('email', 'Not set')}, Admin: {u.get('is_admin', False)}")
            
            st.markdown("### Manage Users")
            with st.form(key='delete_user_form'):
                delete_username = st.selectbox("Select User to Delete", [u['username'] for u in users if u['username'].lower() != username.lower()], key="delete_user")
                delete_button = st.form_submit_button("Delete User")
                if delete_button:
                    success, message = delete_user(username, delete_username)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with st.form(key='toggle_admin_form'):
                toggle_username = st.selectbox("Select User to Toggle Admin", [u['username'] for u in users if u['username'].lower() != username.lower()], key="toggle_admin")
                toggle_button = st.form_submit_button("Toggle Admin Status")
                if toggle_button:
                    success, message = toggle_admin_status(username, toggle_username)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with st.form(key='reset_form'):
                reset_username = st.selectbox("Select User to Reset Usage", [u['username'] for u in users if not u.get('is_admin', False)], key="reset_usage")
                reset_button = st.form_submit_button("Reset Usage Count")
                if reset_button:
                    success, message = reset_user_usage(reset_username)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            
            with st.form(key='reset_all_form'):
                reset_all_button = st.form_submit_button("Reset All Non-Admin Usage")
                if reset_all_button:
                    success, message = reset_all_usage(username)
                    st.success(message)
            
            st.markdown("### View User History")
            with st.form(key='view_history_form'):
                history_username = st.selectbox("Select User", [u['username'] for u in users], key="view_history")
                view_button = st.form_submit_button("View History")
                if view_button:
                    illnesses = get_user_illness_history(history_username)
                    if not illnesses:
                        st.info(f"No history for {history_username}.")
                    else:
                        for idx, illness in enumerate(illnesses):
                            with st.expander(f"📅 {illness['disease']} - {illness['timestamp']}", expanded=False):
                                st.markdown(f"**Disease**: {illness['disease']}")
                                st.markdown(f"**Date**: {illness['timestamp']}")
                                st.markdown("**Symptoms Reported**:")
                                if illness['symptoms']:
                                    for symptom in illness['symptoms']:
                                        st.markdown(f'<div class="history-symptom">• {symptom}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown('<div style="color: #6b7280; font-style: italic;">No symptoms recorded</div>', unsafe_allow_html=True)
            
            st.markdown("### Manage Pending Users")
            pending_users = load_pending_users()
            if not pending_users:
                st.info("No pending users.")
            else:
                for pu in pending_users:
                    st.markdown(f"- **{pu['username']}**: {pu['email']}, Requested: {pu['timestamp']}")
                with st.form(key='manage_pending_form'):
                    pending_username = st.selectbox("Select Pending User", [pu['username'] for pu in pending_users], key="manage_pending")
                    col1, col2 = st.columns(2)
                    with col1:
                        approve_button = st.form_submit_button("Approve")
                    with col2:
                        reject_button = st.form_submit_button("Reject")
                    if approve_button:
                        success, message = approve_pending_user(username, pending_username)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
                    if reject_button:
                        success, message = reject_pending_user(username, pending_username)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

def main_app(username):
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
                position: sticky;
                top: 0;
                z-index: 1000;
            }
        """
    ):
        st.markdown('<h1 style="color: #f8fafc; margin-bottom: 0.25rem;"><span class="icon-large">🧑‍⚕️</span> HeyDoc - Disease Prediction</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #94a3b8; margin-bottom: 0;">AI Powered Diagnosis App</p>', unsafe_allow_html=True)

    tabs = ["📊 Dashboard", "🔍 Predict Disease", "👤 Profile"]
    if is_admin_user(username):
        tabs.append("🛠️ Admin Dashboard")
    
    tab_objects = st.tabs(tabs)
    
    with tab_objects[0]:
        dashboard_ui(username)
    
    with tab_objects[1]:
        predictor = DiseasePredictor()
        predict_disease_ui(username, predictor)
    
    with tab_objects[2]:
        profile_ui(username)
    
    if is_admin_user(username):
        with tab_objects[3]:
            admin_ui(username)
    
    st.markdown("""
        <div class="footer">
            © 2023 HeyDoc™. All rights reserved. 
            <br> Made By The Mind 🧠 of Ashinth 
        </div>
    """, unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    query_params = st.query_params
    if query_params.get("confirm") == "true":
        username = query_params.get("username")
        token = query_params.get("token")
        if username and token:
            success, message = confirm_user(username, token)
            if success:
                st.success(message)
            else:
                st.error(message)
            st.query_params.clear()
            st.rerun()

    if not st.session_state.logged_in:
        login_ui()
    else:
        main_app(st.session_state.username)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.prediction = None
            st.session_state.show_treatment = False
            st.rerun()

if __name__ == "__main__":
    main()