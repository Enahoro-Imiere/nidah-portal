import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="NiDAH Portal", layout="wide")

# -----------------------------
# Dummy Users
# -----------------------------
users_db = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "user1", "password": "user123", "role": "user"},
]

# -----------------------------
# Session state
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
# Logout
# -----------------------------
def logout():
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# -----------------------------
# Landing Page
# -----------------------------
def landing_page():
    col_overview, col_login = st.columns([2,1])

    with col_overview:
        st.markdown("""
        <div style="background-color:#E6F2FF; padding:30px; border-radius:20px; box-shadow: 3px 3px 15px #888;">
        <h1 style="color:#1E3A8A;">NiDAH Portal</h1>
        <h3 style="color:#006400;">Nigerians in Diaspora Advanced Health Programme (NiDAH)</h3>
        <p style="font-size:16px; line-height:1.6;">Nigeria's health system faces challenges, including shortage of skilled health workers, infrastructural deficits, and gaps in specialized services. Continuous emigration of trained professionals (known as "japa") severely impacts delivery, particularly in underserved communities.</p>
        <p style="font-size:16px; line-height:1.6;">Nigeria also has a vast, skilled diaspora making contributions globally. This is a reservoir of knowledge, advanced clinical skills, and modern healthcare management expertise.</p>
        <p style="font-size:16px; line-height:1.6;">Short-term engagement schemes allow diaspora talent to contribute temporarily. The NiDAH Portal facilitates this exchange, transforming brain drain into a national asset.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_login:
        st.markdown("""
        <div style="background-color:#F0F8FF; padding:25px; border-radius:20px; box-shadow: 3px 3px 15px #888;">
        <h2 style="color:#1E3A8A; text-align:center;">Sign In</h2>
        </div>
        """, unsafe_allow_html=True)

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

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign Up"):
                st.session_state["show_signup"] = True
        with col2:
            if st.button("Forgot Password"):
                st.info("Password reset workflow will go here…")

# -----------------------------
# Sign Up Page
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

    # Dummy Data
    states = ["Lagos","Abuja","Kano","Oyo","Rivers"]
    facilities_all = pd.DataFrame({
        "Facility":[f"Facility {i}" for i in range(1,21)],
        "State":[states[i%5] for i in range(20)],
        "RegisteredMonth":["Jan","Feb","Mar","Apr","May"]*4
    })
    volunteers_all = pd.DataFrame({
        "Volunteer":[f"Volunteer {i}" for i in range(1,31)],
        "State":[states[i%5] for i in range(30)],
        "RegisteredMonth":["Jan","Feb","Mar","Apr","May"]*6
    })
    trained_all = pd.DataFrame({
        "Worker":[f"Worker {i}" for i in range(1,26)],
        "TrainedMonth":["Jan","Feb","Mar","Apr","May"]*5
    })
    interventions_all = pd.DataFrame({
        "State":states,
        "Intervention_Count":[5,3,4,2,6],
        "Latitude":[6.5244,9.0578,12.0022,7.3775,4.8156],
        "Longitude":[3.3792,7.4951,8.5919,3.947,7.0498]
    })

    # State filter
    state_filter = st.selectbox("Select State", ["All"]+states)
    if state_filter != "All":
        facilities = facilities_all[facilities_all["State"]==state_filter]
        volunteers = volunteers_all[volunteers_all["State"]==state_filter]
        interventions = interventions_all[interventions_all["State"]==state_filter]
    else:
        facilities = facilities_all
        volunteers = volunteers_all
        interventions = interventions_all

    # KPI Cards
    card_col1, card_col2, card_col3, card_col4 = st.columns(4)
    card_col1.markdown(f"<div style='background-color:#DFF0D8; padding:20px; border-radius:15px; text-align:center;'><h3>Registered Facilities</h3><h2>{facilities['Facility'].nunique()}</h2></div>", unsafe_allow_html=True)
    card_col2.markdown(f"<div style='background-color:#D9EDF7; padding:20px; border-radius:15px; text-align:center;'><h3>Registered Volunteers</h3><h2>{volunteers['Volunteer'].nunique()}</h2></div>", unsafe_allow_html=True)
    card_col3.markdown(f"<div style='background-color:#FCF8E3; padding:20px; border-radius:15px; text-align:center;'><h3>Matched Volunteers</h3><h2>12</h2></div>", unsafe_allow_html=True)
    card_col4.markdown(f"<div style='background-color:#F2DEDE; padding:20px; border-radius:15px; text-align:center;'><h3>Trained Health Workers</h3><h2>{trained_all['Worker'].nunique()}</h2></div>", unsafe_allow_html=True)

    # Charts 2x2
    chart_col1, chart_col2 = st.columns(2)

    # Facilities by month
    fac_month = facilities.groupby("RegisteredMonth")["Facility"].count().reset_index()
    fig1 = px.bar(fac_month, x="RegisteredMonth", y="Facility", text="Facility", title="Facilities Registered Monthly", template="plotly_dark")
    # Volunteers by month
    vol_month = volunteers.groupby("RegisteredMonth")["Volunteer"].count().reset_index()
    fig2 = px.bar(vol_month, x="RegisteredMonth", y="Volunteer", text="Volunteer", title="Volunteers Registered Monthly", template="plotly_dark")
    # Facilities by state
    fac_state = facilities.groupby("State")["Facility"].count().reset_index()
    fig3 = px.pie(fac_state, names="State", values="Facility", title="Facilities by State")
    # Trained health workers
    trained_month = trained_all.groupby("TrainedMonth")["Worker"].count().reset_index()
    fig4 = px.line(trained_month, x="TrainedMonth", y="Worker", title="Trained Health Workers Monthly", markers=True, template="plotly_dark")

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
    st.markdown("Register for the health programs you are interested in:")
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
            st.success(f"Thank you {full_name}, you have registered for: {', '.join(program_choice)}")

# -----------------------------
# App Flow
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
