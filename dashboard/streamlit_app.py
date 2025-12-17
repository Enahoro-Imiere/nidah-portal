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
# Login page
# -----------------------------
def login_page():
    st.title("NiDAH Portal")
    st.markdown("Nigerians in Diaspora Advanced Health Programme (NiDAH)")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        sign_in = st.button("Sign In")
    with col2:
        sign_up = st.button("Sign Up")
    
    if sign_in:
        for user in users_db:
            if user["username"] == username and user["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user["role"]
                st.experimental_rerun()
        st.error("Invalid username or password")
    
    if sign_up:
        st.session_state["show_signup"] = True
        st.experimental_rerun()

# -----------------------------
# Sign-up page
# -----------------------------
def signup_page():
    st.header("Create a new account")
    with st.form("signup_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        role_choice = st.selectbox("Role", ["user"])
        submitted = st.form_submit_button("Register")
        if submitted:
            users_db.append({"username": new_username, "password": new_password, "role": role_choice})
            st.success(f"User {new_username} registered successfully! Please login.")
            st.session_state["show_signup"] = False
            st.experimental_rerun()

# -----------------------------
# Logout function
# -----------------------------
def logout():
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

# -----------------------------
# Initialize session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False

# -----------------------------
# App main logic
# -----------------------------
if not st.session_state["logged_in"]:
    if st.session_state["show_signup"]:
        signup_page()
    else:
        login_page()
else:
    st.sidebar.write(f"Welcome, {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        logout()

    role = st.session_state["role"]

    if role == "admin":
        st.header("Admin Dashboard")

        # -----------------------------
        # Dummy data
        # -----------------------------
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

        # -----------------------------
        # CSS for cards
        # -----------------------------
        st.markdown("""
            <style>
            .kpi-card {
                background-color:#E0F7FA;
                border: 3px solid #1E3A8A;
                border-radius:15px;
                padding:20px;
                text-align:center;
                box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
                margin-bottom:15px;
                transition: transform 0.2s, background-color 0.2s;
            }
            .kpi-card:hover {
                transform: scale(1.05);
                background-color: #B2EBF2;
            }
            .chart-card {
                background-color:#F0F8FF;
                border:3px solid #1E3A8A;
                border-radius:15px;
                padding:15px;
                box-shadow: 4px 4px 15px rgba(0,0,0,0.2);
                margin-bottom:20px;
            }
            </style>
        """, unsafe_allow_html=True)

        # -----------------------------
        # State filter
        # -----------------------------
        col_filter, col_reset = st.columns([3,1])
        with col_filter:
            state_filter = st.selectbox("Select State", ["All"]+states, index=0)
        with col_reset:
            if st.button("Reset Filter"):
                state_filter = "All"

        if state_filter != "All":
            facilities = facilities_all[facilities_all["State"]==state_filter]
            volunteers = volunteers_all[volunteers_all["State"]==state_filter]
            interventions = interventions_all[interventions_all["State"]==state_filter]
        else:
            facilities = facilities_all
            volunteers = volunteers_all
            interventions = interventions_all

        # -----------------------------
        # KPI Cards
        # -----------------------------
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='kpi-card'><h3>Registered Facilities</h3><h2>{facilities['Facility'].nunique()}</h2></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='kpi-card'><h3>Registered Volunteers</h3><h2>{volunteers['Volunteer'].nunique()}</h2></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='kpi-card'><h3>Matched Volunteers</h3><h2>12</h2></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='kpi-card'><h3>Trained Health Workers</h3><h2>{trained_all['Worker'].nunique()}</h2></div>", unsafe_allow_html=True)

        # -----------------------------
        # Charts 2x2
        # -----------------------------
        st.markdown("### Dashboard Charts")
        chart_col1, chart_col2 = st.columns(2)

        # Facilities by month
        fac_month = facilities.groupby("RegisteredMonth")["Facility"].count().reset_index()
        fig1 = px.bar(fac_month, x="RegisteredMonth", y="Facility", text="Facility",
                      title="Facilities Registered Monthly", color="Facility",
                      color_continuous_scale=px.colors.sequential.Teal)
        fig1.update_traces(marker_line_color='black', marker_line_width=2)
        fig1.update_layout(plot_bgcolor="#E6F2FF", paper_bgcolor="#E0F7FA", title_x=0.5)

        # Volunteers by month
        vol_month = volunteers.groupby("RegisteredMonth")["Volunteer"].count().reset_index()
        fig2 = px.bar(vol_month, x="RegisteredMonth", y="Volunteer", text="Volunteer",
                      title="Volunteers Registered Monthly", color="Volunteer",
                      color_continuous_scale=px.colors.sequential.Mint)
        fig2.update_traces(marker_line_color='black', marker_line_width=2)
        fig2.update_layout(plot_bgcolor="#FFF6E6", paper_bgcolor="#FFF8E1", title_x=0.5)

        # Facilities by state
        fac_state = facilities.groupby("State")["Facility"].count().reset_index()
        fig3 = px.pie(fac_state, names="State", values="Facility", title="Facilities by State",
                      color_discrete_sequence=px.colors.sequential.Darkmint)
        fig3.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05]*len(fac_state))

        # Trained health workers
        trained_month = trained_all.groupby("TrainedMonth")["Worker"].count().reset_index()
        fig4 = px.line(trained_month, x="TrainedMonth", y="Worker", title="Trained Health Workers Monthly",
                       markers=True, line_shape="spline")
        fig4.update_traces(line=dict(color="#FF6347", width=4), marker=dict(size=12))
        fig4.update_layout(plot_bgcolor="#F5F5F5", paper_bgcolor="#FFF0F5", title_x=0.5)

        with chart_col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with chart_col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Map
        st.markdown("### Health Intervention Coverage Map")
        map_fig = px.scatter_mapbox(interventions, lat="Latitude", lon="Longitude", size="Intervention_Count",
                                    hover_name="State", hover_data=["Intervention_Count"],
                                    color="Intervention_Count", color_continuous_scale=px.colors.sequential.Teal,
                                    size_max=30, zoom=4)
        map_fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(map_fig, use_container_width=True)

    elif role == "user":
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
