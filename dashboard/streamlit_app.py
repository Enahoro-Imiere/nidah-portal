import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="NiDAH Portal", layout="wide")

# -------------------------------
# SESSION STATE
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------------
# DUMMY USERS
# -------------------------------
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# -------------------------------
# LANDING PAGE
# -------------------------------
def landing_page():
    left, right = st.columns([2, 1])

    # LEFT: OVERVIEW
    with left:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e6f2ff, #f7fbff);
                    padding: 35px; border-radius: 18px;
                    box-shadow: 0px 6px 20px rgba(0,0,0,0.12);">
        <h1 style="color:#0f2a44;">NiDAH Portal</h1>
        <h3 style="color:#006b3c;">
        Nigerians in Diaspora Advanced Health Programme (NiDAH)
        </h3>
        <p style="font-size:16px; line-height:1.7;">
        Nigeria's health system faces significant challenges, including a shortage
        of skilled health workers, infrastructural deficits, and gaps in specialized
        medical services. Continuous emigration of highly trained medical professionals
        — known as <b>"japa"</b> — exacerbates this shortage.
        </p>
        <p style="font-size:16px; line-height:1.7;">
        The WHO estimates a shortage of nearly <b>300,000 doctors and nurses</b>
        in Nigeria, impacting rural and underserved communities. Paradoxically,
        Nigeria has a highly skilled diaspora of health professionals contributing
        globally, representing an immense reservoir of knowledge and expertise.
        </p>
        <p style="font-size:16px; line-height:1.7;">
        Structured short-term engagements provide a pragmatic model for <b>brain
        circulation</b> and <b>brain gain</b>. The <b>NiDAH Portal</b> enables
        diaspora professionals to contribute meaningfully to Nigeria’s health system.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT: SIGN IN
    with right:
        st.markdown("""
        <div style="background:#ffffff; padding:30px;
                    border-radius:18px; box-shadow:0px 6px 20px rgba(0,0,0,0.12);">
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

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
def sidebar_menu():
    st.sidebar.title("NiDAH Portal")
    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Health Programs", "Users", "Reports"]
    )
    return menu

# -------------------------------
# ADMIN DASHBOARD
# -------------------------------
def admin_dashboard():
    st.header("Admin Dashboard")

    # KPI CARDS
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Registered Facilities", 128, "12%")
    kpi2.metric("Registered Volunteers", 342, "18%")
    kpi3.metric("Matched Volunteers", 96, "8%")
    kpi4.metric("Trained Health Workers", 214, "15%")
    st.markdown("---")

    # CHARTS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Facilities Registered Monthly")
        df1 = pd.DataFrame({"Month": ["Jan","Feb","Mar","Apr","May"], "Facilities": [12,18,25,31,44]})
        fig1 = px.bar(df1, x="Month", y="Facilities", text="Facilities", color_discrete_sequence=["#0f766e"])
        fig1.update_layout(height=450, plot_bgcolor="#f0fdf4", paper_bgcolor="#ffffff", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("Volunteers by Specialty")
        df2 = pd.DataFrame({"Specialty":["Surgery","Radiology","Paediatrics","Cardiology"], "Volunteers":[120,80,65,77]})
        fig2 = px.pie(df2, names="Specialty", values="Volunteers", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig2.update_layout(height=450)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Facilities by State")
        df3 = pd.DataFrame({"State":["Lagos","FCT","Oyo","Kano","Rivers"], "Facilities":[45,28,21,19,15]})
        fig3 = px.bar(df3, x="State", y="Facilities", text="Facilities", color_discrete_sequence=["#1e3a8a"])
        fig3.update_layout(height=450, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.subheader("Programme Status Overview")
        df4 = pd.DataFrame({"Programme":["Maternal & Child Health","Digital Health Training","Telemedicine Expansion","Facility Upgrades"], "Status":["Active","Active","Planned","Ongoing"]})
        st.dataframe(df4, use_container_width=True)

# -------------------------------
# USER DASHBOARD
# -------------------------------
def user_dashboard():
    st.header("User Dashboard")
    st.write("This is the user view. Only programs, reports, and basic info are visible.")

# -------------------------------
# APP ROUTER
# -------------------------------
if not st.session_state.logged_in:
    landing_page()
else:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.stop()

    menu = sidebar_menu()

    if st.session_state.role == "admin":
        if menu == "Dashboard":
            admin_dashboard()
        elif menu == "Health Programs":
            st.write("Admin: Health Programs page")
        elif menu == "Users":
            st.write("Admin: Users management page")
        elif menu == "Reports":
            st.write("Admin: Reports page")
    else:
        if menu == "Dashboard":
            user_dashboard()
        elif menu == "Health Programs":
            st.write("User: Health Programs page")
        elif menu == "Users":
            st.write("User: Users page")
        elif menu == "Reports":
            st.write("User: Reports page")
