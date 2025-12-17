import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="NiDAH Portal",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Initialize session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "email" not in st.session_state:
    st.session_state.email = None

# -----------------------------
# Sample users (mock)
# -----------------------------
users_db = {
    "admin@example.com": {"password": "admin123", "role": "admin", "name": "Admin User"},
    "user@example.com": {"password": "user123", "role": "user", "name": "Field Assessor"}
}

# -----------------------------
# Helper functions
# -----------------------------
def overview_page():
    st.markdown(
        """
        ## Nigerians in Diaspora Advanced Health Programme (NiDAH)
        Nigeria's health system faces critical challenges, including shortage of skilled health workers, infrastructural deficits, and gaps in specialized medical services.
        
        Thousands of Nigerian health professionals in the diaspora can play a key role in strengthening health systems in Nigeria through structured short-term engagements.
        
        The NiDAH Portal facilitates **facility profiling**, **program registration**, and **national reporting** to bridge this gap.
        """,
        unsafe_allow_html=True
    )

def login_page():
    st.markdown("<h1 style='color:navy'>NiDAH Portal</h1>", unsafe_allow_html=True)
    st.write("### Sign In")
    
    col1, col2 = st.columns([2,1])
    with col1:
        email_input = st.text_input("Email")
        password_input = st.text_input("Password", type="password")
        if st.button("Login"):
            if email_input in users_db and users_db[email_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.user_role = users_db[email_input]["role"]
                st.session_state.email = email_input
                st.success(f"Logged in as {users_db[email_input]['role'].title()}")
            else:
                st.error("Invalid credentials")
    with col2:
        if st.button("Sign Up"):
            st.session_state.signup = True
        if st.button("Forgot Password"):
            st.info("Password reset feature not implemented in mock portal.")

def signup_page():
    st.write("### Create a New Account")
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            users_db[email] = {"password": password, "role": "user", "name": full_name}
            st.success("Account created successfully! Please login.")
            st.session_state.signup = False

def admin_dashboard():
    st.sidebar.title("NiDAH Portal (Admin)")
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Facility Profiling", "Health Programs", "Reports", "Users"]
    )

    st.title("Admin Dashboard")

    if menu == "Dashboard":
        st.subheader("Overview Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Facilities Assessed", 128)
        col2.metric("States Covered", 32)
        col3.metric("Indicators", 54)
        col4.metric("Pending Reviews", 17)

        st.subheader("Assessment Progress (Mock Data)")
        data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
            "Completed Assessments": [12, 28, 45, 78, 128]
        })
        st.line_chart(data.set_index("Month"))

    elif menu == "Facility Profiling":
        st.subheader("New Facility Profiling")
        with st.form("facility_form"):
            facility_name = st.text_input("Facility Name")
            state = st.selectbox("State", ["Lagos", "Abuja", "Kano", "Oyo"])
            facility_type = st.selectbox("Facility Type", ["Primary", "Secondary", "Tertiary"])
            assessor = st.text_input("Assessor Name")
            assessment_date = st.date_input("Assessment Date", datetime.today())
            submitted = st.form_submit_button("Submit Profiling")
            if submitted:
                st.success("Facility profiling captured (mock submission).")

    elif menu == "Health Programs":
        st.subheader("Health Programs Management")
        programs = pd.DataFrame([
            {"Program": "Maternal & Child Health", "Status": "Active"},
            {"Program": "Digital Health Training", "Status": "Active"},
            {"Program": "Telemedicine Expansion", "Status": "Planned"},
            {"Program": "Health Facility Upgrades", "Status": "Ongoing"},
        ])
        st.dataframe(programs, use_container_width=True)

    elif menu == "Reports":
        st.subheader("Reports")
        st.info("National and state-level reports will be generated here.")
        if st.button("Generate Mock National Report"):
            st.success("National report generated (mock).")

    elif menu == "Users":
        st.subheader("Registered Users")
        users_list = []
        for email, info in users_db.items():
            users_list.append({"Name": info["name"], "Role": info["role"].title(), "Email": email})
        st.table(pd.DataFrame(users_list))

def user_dashboard():
    st.sidebar.title("NiDAH Portal (User)")
    menu = st.sidebar.radio(
        "Navigation",
        ["Overview", "Facility Profiling", "Health Programs", "Profile"]
    )

    st.title("User Dashboard")
    if menu == "Overview":
        st.write("Welcome! Please navigate using the sidebar to access your tasks.")

    elif menu == "Facility Profiling":
        st.subheader("New Facility Profiling")
        with st.form("facility_form_user"):
            facility_name = st.text_input("Facility Name")
            state = st.selectbox("State", ["Lagos", "Abuja", "Kano", "Oyo"])
            facility_type = st.selectbox("Facility Type", ["Primary", "Secondary", "Tertiary"])
            assessor = st.text_input("Assessor Name")
            assessment_date = st.date_input("Assessment Date", datetime.today())
            submitted = st.form_submit_button("Submit Profiling")
            if submitted:
                st.success("Facility profiling captured (mock submission).")

    elif menu == "Health Programs":
        st.subheader("Available Health Programs")
        programs = pd.DataFrame([
            {"Program": "Maternal & Child Health", "Status": "Active"},
            {"Program": "Digital Health Training", "Status": "Active"},
            {"Program": "Telemedicine Expansion", "Status": "Planned"},
            {"Program": "Health Facility Upgrades", "Status": "Ongoing"},
        ])
        st.dataframe(programs, use_container_width=True)

        st.write("### Register for a Program")
        with st.form("program_registration"):
            name = st.text_input("Full Name")
            location = st.text_input("Location")
            specialty = st.text_input("Specialty")
            qualification = st.text_input("Qualification")
            program_choice = st.selectbox("Program Choice", programs["Program"])
            submitted = st.form_submit_button("Register")
            if submitted:
                st.success(f"Registered for {program_choice} (mock submission).")

    elif menu == "Profile":
        user_info = users_db.get(st.session_state.email, {})
        st.subheader("My Profile")
        st.write(f"Name: {user_info.get('name', '')}")
        st.write(f"Email: {st.session_state.email}")
        st.write(f"Role: {user_info.get('role', '')}")

# -----------------------------
# Main App Logic
# -----------------------------
def main():
    st.markdown(
        """
        <style>
        .css-1d391kg {background-color: #f5f5f5;}  /* sidebar background */
        .stApp {background-color: #e6f2ff;}         /* page background */
        </style>
        """,
        unsafe_allow_html=True
    )

    if "signup" in st.session_state and st.session_state.signup:
        signup_page()
    elif not st.session_state.logged_in:
        col1, col2 = st.columns([2,3])
        with col1:
            overview_page()
        with col2:
            login_page()
    else:
        if st.session_state.user_role == "admin":
            admin_dashboard()
        else:
            user_dashboard()

    # Logout button at the bottom
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.email = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
