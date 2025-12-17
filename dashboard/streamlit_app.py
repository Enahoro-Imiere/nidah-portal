import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="NiDAH Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False

# In-memory user database
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "admin", "name": "Admin User"},
    }

# -----------------------------
# Overview page
# -----------------------------
def overview_page():
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("""
        <div style="background-color:#F0F8FF; padding:20px; border-radius:10px;">
            <h2 style="color:#1E3A8A;">Nigerians in Diaspora Advanced Health Programme (NiDAH)</h2>
            <p style="color:#2E8B57; font-size:16px;">
            Nigeria's health system faces challenges: shortage of skilled workers, infrastructural deficits, 
            and gaps in specialized medical services. Emigration of highly trained professionals ("japa") worsens the gap.
            </p>
            <p style="color:#2E8B57; font-size:16px;">
            NiDAH engages diaspora health workers for short-term contributions, strengthening the system. 
            This portal supports facility profiling, program registration, and national reporting.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/6b/Nigeria_Flag.png", width=200)

# -----------------------------
# Login page
# -----------------------------
def login_page():
    st.markdown("<h1 style='color:#1E3A8A;'>NiDAH Portal</h1>", unsafe_allow_html=True)
    st.write("### Sign In")
    
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            if username_input in st.session_state.users_db and \
               st.session_state.users_db[username_input]["password"] == password_input:
                st.session_state.logged_in = True
                st.session_state.user_role = st.session_state.users_db[username_input]["role"]
                st.session_state.current_user = username_input
                st.success(f"Logged in as {st.session_state.user_role.title()}")
            else:
                st.error("Invalid username or password")
    with col2:
        if st.button("Sign Up"):
            st.session_state.signup_mode = True
        if st.button("Forgot Password"):
            st.info("Password reset feature not implemented in this dummy portal.")

# -----------------------------
# Sign up page
# -----------------------------
def signup_page():
    st.write("### Create a New Account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if username in st.session_state.users_db:
                st.error("Username already exists")
            else:
                st.session_state.users_db[username] = {
                    "password": password,
                    "role": "user",
                    "name": full_name,
                    "location": location
                }
                st.success("Account created successfully! Please login.")
                st.session_state.signup_mode = False

# -----------------------------
# User dashboard
# -----------------------------
def user_dashboard():
    st.sidebar.title("NiDAH Portal (User)")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.experimental_rerun()
    
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Health Programs"])

    # Mock programs
    programs = [
        {"Program": "Maternal & Child Health", "Status": "Active"},
        {"Program": "Digital Health Training", "Status": "Active"},
        {"Program": "Telemedicine Expansion", "Status": "Planned"},
        {"Program": "Health Facility Upgrades", "Status": "Ongoing"}
    ]
    programs_df = pd.DataFrame(programs)

    if menu == "Dashboard":
        st.subheader(f"Welcome {st.session_state.current_user}!")
        st.write("Use Health Programs menu to register.")

    if menu == "Health Programs":
        st.subheader("Available Health Programs")
        st.dataframe(programs_df, use_container_width=True)

        st.write("### Register for a Program")
        with st.form("program_form"):
            name = st.text_input("Full Name", st.session_state.users_db[st.session_state.current_user]["name"])
            location = st.text_input("Location", st.session_state.users_db[st.session_state.current_user]["location"])
            specialty = st.text_input("Specialty")
            qualification = st.text_input("Qualification")
            selected_program = st.selectbox("Select Program", programs_df["Program"])
            submitted = st.form_submit_button("Register")
            if submitted:
                st.success(f"{name} registered for {selected_program} successfully!")

# -----------------------------
# Admin dashboard
# -----------------------------
def admin_dashboard():
    st.sidebar.title("NiDAH Portal (Admin)")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.current_user = None
        st.experimental_rerun()
    
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Health Programs", "Reports", "Users"])
    
    # Mock data for charts and KPIs
    months = ["Jan", "Feb", "Mar", "Apr", "May"]
    states = ["Lagos", "Abuja", "Kano", "Oyo"]

    facility_data = pd.DataFrame({
        "Month": months,
        "Facilities Registered": [10, 20, 35, 60, 128],
        "State": ["Lagos","Lagos","Abuja","Kano","Oyo"]
    })

    # KPI cards
    st.subheader("KPI Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Facilities", facility_data["Facilities Registered"].sum())
    col2.metric("Registered Volunteers", 300)
    col3.metric("Matched Volunteers", 150)
    col4.metric("Trained Health Workers", 75)

    st.subheader("KPI Charts")
    col1, col2 = st.columns(2)

    chart1 = alt.Chart(facility_data).mark_bar(color="#2E8B57").encode(
        x="Month",
        y="Facilities Registered",
        tooltip=["Month","Facilities Registered"]
    ).properties(width=650,height=450).configure_view(strokeWidth=4,stroke="black",fill="white")

    chart2 = alt.Chart(facility_data).mark_line(color="#1E3A8A",point=True).encode(
        x="Month",
        y="Facilities Registered",
        tooltip=["Month","Facilities Registered"]
    ).properties(width=650,height=450).configure_view(strokeWidth=4,stroke="black",fill="white")

    col1.altair_chart(chart1,use_container_width=True)
    col2.altair_chart(chart2,use_container_width=True)

    st.subheader("Health Programs")
    programs_df = pd.DataFrame([
        {"Program": "Orthopaedics"},
        {"Program": "Intervention Radiology"},
        {"Program": "Cardiac Care"},
        {"Program": "Neurology"},
        {"Program": "Urology"},
        {"Program": "General Surgery"}
    ])
    st.dataframe(programs_df,use_container_width=True)

# -----------------------------
# Main flow
# -----------------------------
if not st.session_state.logged_in:
    overview_page()
    if st.session_state.signup_mode:
        signup_page()
    else:
        login_page()
else:
    if st.session_state.user_role == "admin":
        admin_dashboard()
    else:
        user_dashboard()
