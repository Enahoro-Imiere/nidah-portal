import streamlit as st
import plotly.express as px
import pandas as pd

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="NiDAH Portal",
    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# -----------------------------------
# DUMMY USERS
# -----------------------------------
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

# -----------------------------------
# LANDING PAGE
# -----------------------------------
def landing_page():
    left, right = st.columns([2, 1])

    # -------- LEFT: OVERVIEW --------
    with left:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #e6f2ff, #f7fbff);
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0px 6px 20px rgba(0,0,0,0.12);
        ">
        <h1 style="color:#0f2a44;">NiDAH Portal</h1>
        <h3 style="color:#006b3c;">Nigerians in Diaspora Advanced Health Programme (NiDAH)</h3>

        <p style="font-size:16px; line-height:1.7;">
        Nigeria's health system, despite pockets of excellence, faces significant
        challenges, including a critical shortage of skilled health workers,
        infrastructural deficits, and gaps in specialized medical services.
        A primary driver of this human resource crisis is the continuous emigration
        of highly trained medical professionals to higher income countries in search
        of better opportunities — a phenomenon commonly known as <b>"japa."</b>
        </p>

        <p style="font-size:16px; line-height:1.7;">
        The World Health Organization (WHO) estimates a shortage of nearly
        <b>300,000 doctors and nurses</b> in Nigeria, a gap that severely impacts
        healthcare delivery, particularly in rural and underserved communities.
        </p>

        <p style="font-size:16px; line-height:1.7;">
        Paradoxically, Nigeria possesses a vast and highly skilled diaspora of health
        professionals who are global leaders in their respective fields.
        Thousands of Nigerian doctors, nurses, pharmacists, and allied health
        professionals are making significant contributions to health systems in
        the United States, United Kingdom, Canada, Saudi Arabia, and beyond.
        </p>

        <p style="font-size:16px; line-height:1.7;">
        This community represents an immense reservoir of knowledge, advanced
        clinical skills, and modern healthcare management expertise that remains
        largely underutilized for national development.
        </p>

        <p style="font-size:16px; line-height:1.7;">
        International evidence demonstrates that diaspora health workers can play
        a transformative role in strengthening health systems in low- and
        middle-income countries of heritage. While permanent return may not always
        be feasible, structured short-term engagements provide a pragmatic model
        for <b>brain circulation</b> and <b>brain gain</b>.
        </p>

        <p style="font-size:16px; line-height:1.7;">
        The <b>Nigerian Diaspora Health Vanguard Initiative (NDHVI)</b> is conceived
        as a formal, sustainable mechanism to facilitate this exchange — enabling
        diaspora professionals to contribute meaningfully to Nigeria’s health
        system while strengthening institutional capacity, clinical excellence,
        and service delivery.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # -------- RIGHT: SIGN IN --------
    with right:
        st.markdown("""
        <div style="
            background:#ffffff;
            padding:30px;
            border-radius:18px;
            box-shadow:0px 6px 20px rgba(0,0,0,0.12);
        ">
        <h2 style="text-align:center; color:#0f2a44;">Sign In</h2>
        """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.role = USERS[username]["role"]
                st.success("Login successful")
            else:
                st.error("Invalid username or password")

        st.markdown("""
        <div style="display:flex; justify-content:space-between; margin-top:10px;">
            <span style="color:#006b3c; cursor:pointer;">Sign Up</span>
            <span style="color:#006b3c; cursor:pointer;">Forgot Password?</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------
# ADMIN DASHBOARD
# -----------------------------------
def admin_dashboard():
    st.subheader("Admin Dashboard")

    # KPI CARDS
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Registered Facilities", 128, "12%")
    with kpi2:
        st.metric("Registered Volunteers", 342, "18%")
    with kpi3:
        st.metric("Matched Volunteers", 96, "8%")
    with kpi4:
        st.metric("Trained Health Workers", 214, "15%")

    st.markdown("---")

    # CHART ROW 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Facilities Registered Monthly")
        df1 = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Facilities": [12, 18, 25, 31, 44, 56]
        })
        fig1 = px.bar(df1, x="Month", y="Facilities", text="Facilities",
                      color_discrete_sequence=["#0f766e"])
        fig1.update_layout(height=450, plot_bgcolor="#f0fdf4", paper_bgcolor="#ffffff",
                           xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### Volunteers by Specialty")
        df2 = pd.DataFrame({
            "Specialty": ["Surgery", "Radiology", "Paediatrics", "Cardiology"],
            "Volunteers": [120, 80, 65, 77]
        })
        fig2 = px.pie(df2, names="Specialty", values="Volunteers",
                      hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True)

    # CHART ROW 2
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Facilities by State")
        df3 = pd.DataFrame({
            "State": ["Lagos", "FCT", "Oyo", "Kano", "Rivers"],
            "Facilities": [45, 28, 21, 19, 15]
        })
        fig3 = px.bar(df3, x="State", y="Facilities", text="Facilities",
                      color_discrete_sequence=["#1e3a8a"])
        fig3.update_layout(height=450, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("### Programme Status Overview")
        df4 = pd.DataFrame({
            "Programme": ["Maternal & Child Health", "Digital Health Training",
                          "Telemedicine Expansion", "Facility Upgrades"],
            "Status": ["Active", "Active", "Planned", "Ongoing"]
        })
        st.dataframe(df4, use_container_width=True)

# -----------------------------------
# APP ROUTER
# -----------------------------------
if not st.session_state.logged_in:
    landing_page()
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.stop()

    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        st.info("User dashboard will appear here.")
