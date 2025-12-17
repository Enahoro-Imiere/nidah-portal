import streamlit as st

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
    st.info("Admin KPIs and charts will appear here.")

def user_dashboard():
    st.sidebar.success("User")
    st.title("User Dashboard")
    st.info("User program registration will appear here.")

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
