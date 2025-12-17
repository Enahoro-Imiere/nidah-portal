import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

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
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin": {"password": "admin123", "role": "admin", "name": "Admin User"},
        "user": {"password": "user123", "role": "user", "name": "Field Assessor"}
    }

# -----------------------------
# Overview page
# -----------------------------
def overview_page():
    st.markdown(
        """
        ## Nigerians in Diaspora Advanced Health Programme (NiDAH)
        
        Nigeria's health system faces serious challenges: shortage of skilled health workers, 
        infrastructural deficits, and gaps in specialized medical services. A key factor is the 
        emigration of highly trained professionals seeking better opportunities abroad ("japa"). 

        Meanwhile, Nigeria has a vast, highly skilled diaspora of doctors, nurses, pharmacists, 
        and allied health professionals contributing globally. This talent is underutilized for 
        national development.

        The NiDAH initiative creates a structured mechanism to engage diaspora health workers, 
        offering short-term engagements to strengthen Nigeria's health system. This portal 
        facilitates **facility profiling**, **program registration**, and **national reporting** 
        to bridge the gap between brain drain and national healthcare development.
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Login page
# -----------------------------
def login_page():
    st.markdown("<h1 style='color:navy'>NiDAH Portal</h1>", unsafe_allow_html=True)
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
            st.info("Password reset feature not implemented in this mock portal.")

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
# Admin dashboard
# -----------------------------
def admin_dashboard():
    st.sidebar.title("NiDAH Portal (Admin)")
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Health Programs", "Reports", "Users"]
    )

    st.title("Admin Dashboard")

    # ---------------- Dashboard KPIs ----------------
    if menu == "Dashboard":
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Registered Facilities", 128, "+12%")
        col2.metric("Registered Volunteers", 320, "+8%")
        col3.metric("Matched Volunteers", 210, "+15%")
        col4.metric("Trained Health Workers", 75, "+10%")

        st.subheader("KPI Charts")

        # --- Mock Data ---
        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        states = ["Lagos", "Abuja", "Kano", "Oyo"]

        facility_data = pd.DataFrame({
            "Month": months,
            "Facilities Registered": [10, 20, 35, 60, 128]
        })

        volunteers_data = pd.DataFrame({
            "Month": months,
            "Volunteers Registered": [30, 60, 120, 200, 320]
        })

        matched_data = pd.DataFrame({
            "Month": months,
            "Matched Volunteers": [5, 20, 50, 120, 210]
        })

        trained_data = pd.DataFrame({
            "Month": months,
            "Trained Health Workers": [10, 20, 30, 50, 75]
        })

        facilities_by_state = pd.DataFrame({
            "State": ["Lagos", "Abuja", "Kano", "Oyo", "Lagos", "Abuja"],
            "Facility": ["F1", "F2", "F3", "F4", "F5", "F6"],
            "Count": [50, 30, 20, 15, 78, 45]
        })

        # --- Charts ---
        st.subheader("Facilities Registered Monthly")
        chart1 = alt.Chart(facility_data).mark_line(point=True, color="green").encode(
            x="Month",
            y="Facilities Registered",
            tooltip=["Month", "Facilities Registered"]
        ).properties(height=300)
        st.altair_chart(chart1, use_container_width=True)

        st.subheader("Volunteers Registered Monthly")
        chart2 = alt.Chart(volunteers_data).mark_line(point=True, color="navy").encode(
            x="Month",
            y="Volunteers Registered",
            tooltip=["Month", "Volunteers Registered"]
        ).properties(height=300)
        st.altair_chart(chart2, use_container_width=True)

        st.subheader("Matched Volunteers Monthly")
        chart3 = alt.Chart(matched_data).mark_area(color="#90ee90", opacity=0.6).encode(
            x="Month",
            y="Matched Volunteers",
            tooltip=["Month", "Matched Volunteers"]
        ).properties(height=300)
        st.altair_chart(chart3, use_container_width=True)

        st.subheader("Trained Health Workers Monthly")
        chart4 = alt.Chart(trained_data).mark_bar(color="teal").encode(
            x="Month",
            y="Trained Health Workers",
            tooltip=["Month", "Trained Health Workers"]
        ).properties(height=300)
        st.altair_chart(chart4, use_container_width=True)

        # --- Facilities by State ---
        st.subheader("Facilities Registered by State")
        selected_state = st.selectbox("Select State", ["All"] + states)
        if selected_state != "All":
            filtered_data = facilities_by_state[facilities_by_state["State"] == selected_state]
        else:
            filtered_data = facilities_by_state

        chart_state = alt.Chart(filtered_data).mark_bar(color="orange").encode(
            x="Facility",
            y="Count",
            tooltip=["Facility", "State", "Count"]
        ).properties(height=300)
        st.altair_chart(chart_state, use_container_width=True)

    # ---------------- Health Programs ----------------
    elif menu == "Health Programs":
        st.subheader("NiDAH Supported Health Interventions")
        programs = pd.DataFrame([
            {"Program": "Orthopaedics", "Status": "Active"},
            {"Program": "Interventional Radiology", "Status": "Active"},
            {"Program": "Cardiac Care", "Status": "Planned"},
            {"Program": "Neurology", "Status": "Ongoing"},
            {"Program": "Urology", "Status": "Active"},
            {"Program": "General Surgery", "Status": "Planned"},
        ])
        st.dataframe(programs, use_container_width=True)

    # ---------------- Reports ----------------
    elif menu == "Reports":
        st.subheader("Reports")
        st.info("National and state-level reports will be generated here.")
        if st.button("Generate Mock National Report"):
            st.success("National report generated (mock).")

    # ---------------- Users ----------------
    elif menu == "Users":
        st.subheader("Registered Users")
        users_list = []
        for username, info in st.session_state.users_db.items():
            users_list.append({
                "Username": username,
                "Name": info["name"],
                "Role": info["role"].title()
            })
        st.table(pd.DataFrame(users_list))

# -----------------------------
# User dashboard
# -----------------------------
def user_dashboard():
    st.sidebar.title("NiDAH Portal (User)")
    menu = st.sidebar.radio(
        "Navigation",
        ["Overview", "Facility Profiling", "Health Programs", "Profile"]
    )

    st.title("User Dashboard")

    if menu == "Overview":
        overview_page()

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
            {"Program": "Orthopaedics", "Status": "Active"},
            {"Program": "Interventional Radiology", "Status": "Active"},
            {"Program": "Cardiac Care", "Status": "Planned"},
            {"Program": "Neurology", "Status": "Ongoing"},
            {"Program": "Urology", "Status": "Active"},
            {"Program": "General Surgery", "Status": "Planned"},
        ])
        st.dataframe(programs, use_container_width=True)

        st.write("### Register for a Program")
        with st.form("program_registration"):
            full_name = st.text_input("Full Name")
            location = st.text_input("Location")
            specialty = st.text_input("Specialty")
            qualification = st.text_input("Qualification")
            program_choice = st.selectbox("Program Choice", programs["Program"])
            submitted = st.form_submit_button("Register")
            if submitted:
                st.success(f"Registered for {program_choice} (mock submission).")

    elif menu == "Profile":
        user_info = st.session_state.users_db.get(st.session_state.current_user, {})
        st.subheader("My Profile")
        st.write(f"Name: {user_info.get('name', '')}")
        st.write(f"Username: {st.session_state.current_user}")
        st.write(f"Role: {user_info.get('role', '')}")
        st.write(f"Location: {user_info.get('location', '')}")

# -----------------------------
# Main App
# -----------------------------
def main():
    st.markdown(
        """
        <style>
        .css-1d391kg {background-color: #d9f0d9;}  /* sidebar background */
        .stApp {background-color: #f0f8ff;}         /* page background */
        h1 {color: navy;}
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.signup_mode:
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

    # Logout button
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.current_user = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
