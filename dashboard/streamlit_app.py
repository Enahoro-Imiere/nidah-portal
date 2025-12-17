import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="NiDAH Portal", layout="wide")

# -----------------------------
# Dummy users (replace with DB later)
# -----------------------------
users_db = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "user1", "password": "user123", "role": "user"},
]

# -----------------------------
# Initialize session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""

# -----------------------------
# Logout function
# -----------------------------
def logout():
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# -----------------------------
# Landing Page: Overview + Login
# -----------------------------
def landing_page():
    col_overview, col_login = st.columns([2, 1])

    # Overview
    with col_overview:
        st.markdown(
            """
            <div style="background-color:#E6F2FF; padding:25px; border-radius:15px;">
            <h1 style="color:#1E3A8A;">NiDAH Portal</h1>
            <h3 style="color:#006400;">Nigerians in Diaspora Advanced Health Programme (NiDAH)</h3>
            <p style="font-size:16px; color:#000000;">
            Nigeria's health system, despite pockets of excellence, faces significant challenges, including a critical shortage of skilled health workers, infrastructural deficits, and gaps in specialized medical services. A primary driver of this human resource crisis is the continuous emigration of highly trained medical professionals to higher income countries in search of better opportunities—a phenomenon known as "japa." The World Health Organization (WHO) estimates a shortage of nearly 300,000 doctors and nurses in Nigeria, a gap that severely impacts healthcare delivery, particularly in rural and underserved communities.
            </p>
            <p style="font-size:16px; color:#000000;">
            Paradoxically, Nigeria possesses a vast and highly skilled diaspora of health professionals who are global leaders in their respective fields. Thousands of Nigerian doctors, nurses, pharmacists, and allied health professionals are making significant contributions to the health systems of countries like the US, UK, Canada, and Saudi Arabia. This represents an immense reservoir of knowledge, advanced clinical skills, and modern healthcare management expertise currently underutilized for national development.
            </p>
            <p style="font-size:16px; color:#000000;">
            International evidence indicates that diaspora health workers can play a critical role in strengthening health systems and services in low- or middle-income countries of heritage, as well as in their host countries. While permanent return is a complex personal decision, there is a strong desire among many diaspora professionals to contribute to Nigeria's development. A structured, short-term engagement scheme offers a pragmatic "brain circulation" model, providing a bridge for this talent to flow back into the country, even if temporarily. The NiDAH Portal is conceived as a formal, sustainable mechanism to facilitate this two-way exchange, transforming brain drain into a strategic national asset.
            </p>
            </div>
            """, unsafe_allow_html=True
        )

    # Login box
    with col_login:
        st.markdown(
            """
            <div style="background-color:#F0F8FF; padding:25px; border-radius:15px;">
            <h2 style="color:#1E3A8A;">Sign In</h2>
            </div>
            """, unsafe_allow_html=True
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            for user in users_db:
                if user["username"] == username and user["password"] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = user["role"]
                    st.experimental_rerun()
            st.error("Invalid username or password")

        # Sign Up / Forgot Password links
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign Up"):
                st.session_state["show_signup"] = True
        with col2:
            if st.button("Forgot Password"):
                st.info("Password reset workflow goes here…")

# -----------------------------
# Sign-up form
# -----------------------------
def signup_page():
    st.subheader("Create a new account")
    with st.form("signup_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            users_db.append({"username": new_username, "password": new_password, "role": "user"})
            st.success(f"User {new_username} registered successfully! Please login.")
            st.session_state["show_signup"] = False
            st.experimental_rerun()

# -----------------------------
# Admin Dashboard
# -----------------------------
def admin_dashboard():
    st.header("Admin Dashboard")

    # Dummy data
    states = ["Lagos", "Abuja", "Kano", "Oyo", "Rivers"]
    facilities_all = pd.DataFrame({
        "Facility": [f"Facility {i}" for i in range(1,21)],
        "State": [states[i%5] for i in range(20)],
        "RegisteredMonth": ["Jan","Feb","Mar","Apr","May"]*4
    })
    volunteers_all = pd.DataFrame({
        "Volunteer": [f"Volunteer {i}" for i in range(1,31)],
        "State": [states[i%5] for i in range(30)],
        "RegisteredMonth": ["Jan","Feb","Mar","Apr","May"]*6
    })
    trained_all = pd.DataFrame({
        "Worker": [f"Worker {i}" for i in range(1,26)],
        "TrainedMonth": ["Jan","Feb","Mar","Apr","May"]*5
    })
    interventions_all = pd.DataFrame({
        "State": states,
        "Intervention_Count": [5, 3, 4, 2, 6],
        "Latitude": [6.5244, 9.0578, 12.0022, 7.3775, 4.8156],
        "Longitude": [3.3792, 7.4951, 8.5919, 3.9470, 7.0498]
    })

    # State filter
    state_filter = st.selectbox("Select State", ["All"] + states)
    if state_filter != "All":
        facilities = facilities_all[facilities_all["State"]==state_filter]
        volunteers = volunteers_all[volunteers_all["State"]==state_filter]
        interventions = interventions_all[interventions_all["State"]==state_filter]
    else:
        facilities = facilities_all
        volunteers = volunteers_all
        interventions = interventions_all

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registered Facilities", facilities["Facility"].nunique())
    col2.metric("Registered Volunteers", volunteers["Volunteer"].nunique())
    col3.metric("Matched Volunteers", 12)
    col4.metric("Trained Health Workers", trained_all["Worker"].nunique())

    # Charts 2x2
    chart_col1, chart_col2 = st.columns(2)

    # Facilities by month
    fac_month = facilities.groupby("RegisteredMonth")["Facility"].count().reset_index()
    fig1 = px.bar(fac_month, x="RegisteredMonth", y="Facility", text="Facility", title="Facilities Registered Monthly")
    # Volunteers by month
    vol_month = volunteers.groupby("RegisteredMonth")["Volunteer"].count().reset_index()
    fig2 = px.bar(vol_month, x="RegisteredMonth", y="Volunteer", text="Volunteer", title="Volunteers Registered Monthly")
    # Facilities by state
    fac_state = facilities.groupby("State")["Facility"].count().reset_index()
    fig3 = px.pie(fac_state, names="State", values="Facility", title="Facilities by State")
    # Trained health workers
    trained_month = trained_all.groupby("TrainedMonth")["Worker"].count().reset_index()
    fig4 = px.line(trained_month, x="TrainedMonth", y="Worker", title="Trained Health Workers Monthly", markers=True)

    with chart_col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    with chart_col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)

    # Map
    st.subheader("Health Intervention Coverage Map")
    map_fig = px.scatter_mapbox(interventions, lat="Latitude", lon="Longitude", size="Intervention_Count",
                                hover_name="State", hover_data=["Intervention_Count"],
                                color="Intervention_Count", color_continuous_scale=px.colors.sequential.Teal,
                                size_max=30, zoom=4)
    map_fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(map_fig, use_container_width=True)

# -----------------------------
# User Dashboard
# -----------------------------
def user_dashboard():
    st.header("NiDAH Program Registration")
    st.markdown("""
    Welcome to the **NiDAH Portal**. Here you can register for the health programs you are interested in.
    """)
    with st.form("program_signup"):
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        specialty = st.text_input("Specialty")
        qualification = st.text_input("Qualification")
        program_choice = st.multiselect("Select Programs", 
                                        ["Training", "Advanced Procedures", "Other Interests",
                                         "Maternal & Child Health", "Digital Health Training",
                                         "Telemedicine Expansion", "Health Facility Upgrades"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Thank you {full_name}, you have successfully registered for: {', '.join(program_choice)}")

# -----------------------------
# App flow
# -----------------------------
if not st.session_state["logged_in"]:
    if st.session_state["show_signup"]:
        signup_page()
    else:
        landing_page()
else:
    st.sidebar.write(f"Welcome, {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        logout()

    if st.session_state["role"] == "admin":
        admin_dashboard()
    else:
        user_dashboard()
