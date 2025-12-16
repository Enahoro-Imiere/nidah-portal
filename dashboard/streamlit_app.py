import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="NiDAH Portal", layout="wide")

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {
            "full_name": "Administrator",
            "location": "Head Office",
            "email": "admin@example.com",
            "password": "admin123",
            "role": "admin"
        }
    }
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# ---------------- COLOR HELPERS ----------------
def styled_header(text, color="#003366"):  # navy
    st.markdown(f"<h2 style='color:{color};'>{text}</h2>", unsafe_allow_html=True)

def styled_subheader(text, color="#006400"):  # green
    st.markdown(f"<h4 style='color:{color};'>{text}</h4>", unsafe_allow_html=True)

def colored_button(label, color="#006400"):
    st.markdown(f"""
        <style>
        div.stButton > button:first-child {{
            background-color: {color};
            color: white;
            height: 40px;
            width: 100%;
            border-radius:10px;
            border: none;
            font-size:16px;
            font-weight:bold;
        }}
        </style>
        """, unsafe_allow_html=True)
    return st.button(label)

# ---------------- LOGOUT ----------------
def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.page = "Overview"
    st.experimental_rerun()

# ---------------- OVERVIEW PAGE ----------------
def overview_page():
    col_overview, col_auth = st.columns([3, 1])

    # Overview left
    with col_overview:
        styled_header("Nigerians in Diaspora Advanced Health Programme (NiDAH)")
        styled_subheader("Overview")

        overview_text = """
Nigeria's health system, despite pockets of excellence, faces significant challenges, including a critical shortage 
of skilled health workers, infrastructural deficits, and gaps in specialized medical services. A primary driver of this 
human resource crisis is the continuous emigration of highly trained medical professionals to higher-income countries 
in search of better opportunities—a phenomenon known as "japa." The World Health Organization (WHO) estimates a 
shortage of nearly 300,000 doctors and nurses in Nigeria, a gap that severely impacts healthcare delivery, particularly 
in rural and underserved communities.

Paradoxically, Nigeria possesses a vast and highly skilled diaspora of health professionals who are global leaders in 
their respective fields. Thousands of Nigerian doctors, nurses, pharmacists, and allied health professionals are making 
significant contributions to the health systems of countries like the United States, the United Kingdom, Canada, and Saudi Arabia. 
This community represents an immense reservoir of knowledge, advanced clinical skills, and modern healthcare management 
expertise that is currently underutilized for national development.

International evidence indicates that diaspora health workers can play a critical role in strengthening health systems 
and services in low- or middle-income countries of heritage, as well as in their host countries. While permanent return 
is a complex personal decision, there is a strong, expressed desire among many diaspora professionals to contribute to 
Nigeria's development. A structured, short-term engagement scheme offers a pragmatic "brain circulation" or "brain gain" 
model, providing a bridge for this talent to flow back into the country, even if temporarily.

The Nigerian Diaspora Health Vanguard Initiative (NDHVI) is conceived as a formal, sustainable mechanism to facilitate 
this two-way exchange, transforming brain drain into a strategic national asset.
"""
        st.markdown(f"<div style='color:#003366'>{overview_text}</div>", unsafe_allow_html=True)

    # Login form right
    with col_auth:
        styled_header("NiDAH Login", color="#006400")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

            if login_btn:
                users = st.session_state.users
                if username in users and users[username]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.role = users[username]["role"]
                    st.session_state.username = username
                    st.session_state.page = "Main"
                    st.success("Login successful")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")

        # Sign Up / Forgot Password buttons below login
        col1, col2 = st.columns([1,1])
        with col1:
            if colored_button("Sign Up", "#006400"):
                st.session_state.page = "Sign Up"
        with col2:
            if colored_button("Forgot Password", "#003366"):
                st.session_state.page = "Forgot Password"

# ---------------- SIGN UP PAGE ----------------
def signup_page():
    st.title("Sign Up for NiDAH Portal")
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        email = st.text_input("Email Address")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Create Account")

        if submit:
            users = st.session_state.users
            if not (full_name and location and email and username and password):
                st.error("All fields are required")
            elif username in users:
                st.error("Username already exists")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                users[username] = {
                    "full_name": full_name,
                    "location": location,
                    "email": email,
                    "password": password,
                    "role": "user"
                }
                st.success("Account created successfully! Please log in.")
                st.session_state.page = "Overview"
                st.experimental_rerun()

# ---------------- MAIN APP ----------------
def main_app():
    st.sidebar.markdown("<h3 style='color:#003366'>NiDAH Portal</h3>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**User:** {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** {st.session_state.role.capitalize()}")
    if colored_button("Logout", "#003366"):
        logout()

    # Sidebar menu by role
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation",
            ["Dashboard", "Facility Profiling", "Indicators", "Health Programs", "Reports", "Users"])
    else:
        menu = st.sidebar.radio("Navigation",
            ["Dashboard", "Facility Profiling", "Health Programs"])

    st.title("NiDAH Portal")
    st.divider()

    # ---------------- DASHBOARD ----------------
    if menu=="Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        for col, label, value in zip(
            [col1,col2,col3,col4],
            ["Participating Facilities","States/Regions Covered","Key Health Indicators","Pending Assessments"],
            [128,32,54,17]):
            col.markdown(f"<div style='background-color:#006400;color:white;padding:10px;border-radius:10px;text-align:center;font-weight:bold'>{label}<br>{value}</div>", unsafe_allow_html=True)

        st.subheader("Assessment Progress (Mock Data)")
        data = pd.DataFrame({"Month":["Jan","Feb","Mar","Apr","May"],"Completed Assessments":[12,28,45,78,128]})
        st.line_chart(data.set_index("Month"))

    # ---------------- FACILITY PROFILING ----------------
    elif menu=="Facility Profiling":
        styled_subheader("New Facility Profiling", "#003366")
        with st.form("facility_form"):
            facility_name = st.text_input("Facility Name")
            state = st.selectbox("State/Region", ["Lagos","Abuja","Kano","Oyo"])
            facility_type = st.selectbox("Facility Type", ["Primary","Secondary","Tertiary"])
            assessor = st.text_input("Assessor Name")
            assessment_date = st.date_input("Profiling Date", datetime.today())
            submitted = st.form_submit_button("Submit Profiling")
            if submitted:
                st.success("Facility profiling captured (mock submission).")

    # ---------------- INDICATORS (ADMIN ONLY) ----------------
    elif menu=="Indicators" and st.session_state.role=="admin":
        styled_subheader("NiDAH Indicators", "#006400")
        indicators = pd.DataFrame({
            "Code":["NH01","NH02","NH03"],
            "Indicator":["Availability of Electronic Health Records",
                        "Internet Connectivity in Facility",
                        "Digital Health Skills of Staff"],
            "Score (Mock)":[3,2,4]
        })
        st.dataframe(indicators, use_container_width=True)

    # ---------------- HEALTH PROGRAMS ----------------
    elif menu=="Health Programs":
        styled_subheader("NiDAH Health Programs Registration", "#003366")
        programs = ["Training","Advanced Procedures","Other Interest","Maternal & Child Health",
                    "Digital Health Training","Telemedicine Expansion","Health Facility Upgrades"]
        st.write("Select program(s) to register for:")

        selected_programs = st.multiselect("Choose programs", programs)
        with st.form("program_registration_form"):
            specialty = st.text_input("Your Specialty")
            qualification = st.text_input("Your Qualification")
            submit_program = st.form_submit_button("Register for Selected Programs")
        if submit_program:
            if not selected_programs:
                st.warning("Select at least one program")
            elif not (specialty and qualification):
                st.warning("Fill specialty and qualification")
            else:
                if "user_programs" not in st.session_state:
                    st.session_state.user_programs = {}
                user_info = st.session_state.users[st.session_state.username]
                registrations = st.session_state.user_programs.get(st.session_state.username, [])
                for prog in selected_programs:
                    registrations.append({"Program":prog,"Full Name":user_info["full_name"],
                                          "Location":user_info["location"],"Specialty":specialty,
                                          "Qualification":qualification})
                st.session_state.user_programs[st.session_state.username] = registrations
                st.success(f"Registered for: {', '.join(selected_programs)}")
        # Show current registrations
        if "user_programs" in st.session_state and st.session_state.username in st.session_state.user_programs:
            st.table(pd.DataFrame(st.session_state.user_programs[st.session_state.username]))

    # ---------------- REPORTS (ADMIN ONLY) ----------------
    elif menu=="Reports":
        styled_subheader("Reports", "#006400")
        st.info("National and state-level reports will be generated here.")
        if st.button("Generate Mock National Report"):
            st.success("National report generated (mock).")

    # ---------------- USERS (ADMIN ONLY) ----------------
    elif menu=="Users":
        styled_subheader("Registered Users", "#003366")
        users_df = pd.DataFrame([{"Full Name":d.get("full_name",""),"Username":u,"Email":d.get("email",""),
                                  "Location":d.get("location",""),"Role":d.get("role","")} for u,d in st.session_state.users.items()])
        st.table(users_df)

# ---------------- APP ENTRY ----------------
if st.session_state.page=="Overview":
    overview_page()
elif st.session_state.page=="Sign Up":
    signup_page()
else:
    main_app()
