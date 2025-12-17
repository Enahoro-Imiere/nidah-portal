import streamlit as st
import plotly.express as px
import pandas as pd

# -----------------------------------
# PAGE CONFIG (Cloud-safe)
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

# -----------------------------------
# DUMMY USERS (NO DATABASE)
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
        <h3 style="color:#006b3c;">
        Nigerians in Diaspora Advanced Health Programme (NiDAH)
        </h3>

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

        if st.button("Login", use_container_width=True):
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
# DASHBOARDS (PLACEHOLDERS)
# -----------------------------------
def admin_dashboard():
    st.sidebar.success("Admin")
    st.title("Admin Dashboard")

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown("""
        <div style="background:#e6f2ff; padding:20px; border-radius:15px; text-align:center;">
            <h3 style="color:#0f2a44;">Facilities</h3>
            <h1 style="color:#006b3c;">128</h1>
            <p>Registered</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi2:
        st.markdown("""
        <div style="background:#f0fff4; padding:20px; border-radius:15px; text-align:center;">
            <h3 style="color:#0f2a44;">Volunteers</h3>
            <h1 style="color:#006b3c;">342</h1>
            <p>Registered</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown("""
        <div style="background:#fff7ed; padding:20px; border-radius:15px; text-align:center;">
            <h3 style="color:#0f2a44;">Matched</h3>
            <h1 style="color:#006b3c;">97</h1>
            <p>Volunteers</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
        st.markdown("""
        <div style="background:#eef2ff; padding:20px; border-radius:15px; text-align:center;">
            <h3 style="color:#0f2a44;">Trained</h3>
            <h1 style="color:#006b3c;">215</h1>
            <p>Health Workers</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # -----------------------------
    # PLACEHOLDER SECTIONS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
    st.markdown(
        "<h4 style='margin-bottom:10px;'>Facilities Registered Monthly</h4>",
        unsafe_allow_html=True
    )

    # Dummy monthly data
    df_facilities = pd.DataFrame({
        "Month": [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
        ],
        "Facilities": [5, 8, 12, 15, 18, 20, 22, 25, 28, 30, 32, 35]
    })

    fig = px.bar(
        df_facilities,
        x="Month",
        y="Facilities",
        text="Facilities",
        color_discrete_sequence=["#0f766e"]
    )

    fig.update_layout(
        height=420,
        plot_bgcolor="#f9fafb",
        paper_bgcolor="#ffffff",
        margin=dict(l=20, r=20, t=30, b=20),
        font=dict(size=14),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        showlegend=False
    )

    fig.update_traces(
        textposition="outside",
        marker_line_width=2,
        marker_line_color="#0f2a44"
    )

    st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown("""
        <div style="background:#ffffff; padding:25px; border-radius:15px; box-shadow:0px 4px 10px rgba(0,0,0,0.1);">
            <h4>Volunteers by State</h4>
            <p style="color:gray;">🗺️ Chart / map placeholder – coming next</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#ffffff; padding:25px; border-radius:15px; box-shadow:0px 4px 10px rgba(0,0,0,0.1);">
        <h4>Training Progress Overview</h4>
        <p style="color:gray;">📈 Progress tracking placeholder – coming next</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------
# APP ROUTER
# -----------------------------------
if not st.session_state.logged_in:
    landing_page()
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.stop()

    if st.session_state.role == "admin":
        admin_dashboard()
    else:
        user_dashboard()
