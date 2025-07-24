import streamlit as st
from pages.login import user_login, doctor_login, user_register, doctor_register
from pages import (
    pdf_generator,
    appointment,
    diagnosis2, health_records2
)

# Set Streamlit page configuration
st.set_page_config(
    page_title="Smart Health App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Initialize session state if it doesn't exist
    if 'role' not in st.session_state and 'page_state' not in st.session_state:
        st.session_state.page_state = "register"  # default to registration page

    if st.session_state.get("role"):
        show_dashboard()
    elif st.session_state.page_state == "register":
        show_welcome_page()
    elif st.session_state.page_state == "login":
        show_login_page()

def show_welcome_page():
    st.title("Smart Health Portal")
    st.markdown("---")
    st.subheader("New to the platform? Register below:")

    tab1, tab2 = st.tabs(["Patient Registration", "Doctor Registration"])

    with tab1:
        with st.form("patient_register"):
            new_user = st.text_input("Username", key="new_patient_user")
            new_pass = st.text_input("Password", type="password", key="new_patient_pass")
            if st.form_submit_button("Register"):
                if user_register(new_user, new_pass):
                    st.success("Account created! Please login.")

    with tab2:
        with st.form("doctor_register"):
            new_doc = st.text_input("Username", key="new_doctor_user")
            new_pass = st.text_input("Password", type="password", key="new_doctor_pass")
            if st.form_submit_button("Register"):
                if doctor_register(new_doc, new_pass):
                    st.success("Account created! Please login.")

    st.markdown("Already have an account?")
    if st.button("Go to Login"):
        st.session_state.page_state = "login"
        st.rerun()

def show_login_page():
    st.title("Login to Smart Health")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Patient Login", "Doctor Login"])

    with tab1:
        with st.form("patient_login"):
            username = st.text_input("Username", key="patient_user")
            password = st.text_input("Password", type="password", key="patient_pass")
            if st.form_submit_button("Login"):
                if user_login(username, password):
                    st.session_state.role = "user"
                    st.session_state.username = username
                    st.rerun()

    with tab2:
        with st.form("doctor_login"):
            username = st.text_input("Username", key="doctor_user")
            password = st.text_input("Password", type="password", key="doctor_pass")
            if st.form_submit_button("Login"):
                if doctor_login(username, password):
                    st.session_state.role = "doctor"
                    st.session_state.username = username
                    st.rerun()

    st.markdown("New to the platform?")
    if st.button("Go to Registration"):
        st.session_state.page_state = "register"
        st.rerun()

def show_dashboard():
    st.sidebar.title(f"Hello {st.session_state.username}")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    if st.session_state.role == "user":
        show_patient_dashboard()
    else:
        show_doctor_dashboard()

def show_patient_dashboard():
    st.title("Patient Health Dashboard")
    menu = st.sidebar.radio("Navigation", [
        "Medical Records",
        "Generate PDF Report",
        "Book Appointment"
    ])
    if menu == "Medical Records":
        health_records2.show_page(st.session_state.username)
    elif menu == "Generate PDF Report":
        pdf_generator.show_page(st.session_state.username)
    elif menu == "Book Appointment":
        appointment.show_page(st.session_state.username)

def show_doctor_dashboard():
    st.title("Doctor Clinical Dashboard")
    menu = st.sidebar.radio("Navigation", [
        "View Appointments",
        "Upload Diagnosis Report"
    ])
    if menu == "View Appointments":
        appointment.doctor_view(st.session_state.username)
    elif menu == "Upload Diagnosis Report":
        diagnosis2.show_page(st.session_state.username)

if __name__ == "__main__":
    main()
