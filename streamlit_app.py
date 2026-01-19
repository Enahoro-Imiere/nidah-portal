import streamlit as st
from sqlalchemy import create_engine, text
from datetime import date

# ----------------------
# DATABASE CONNECTION
# ----------------------
DB_USER = "nidah_user"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nidah_db"

try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    st.success("✅ Database connected successfully!")
except Exception as e:
    st.error("❌ Database connection failed!")
    st.write(e)
    st.stop()

# ----------------------
# PAGE STATE
# ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="NiDAH Portal",
    page_icon="🏥",
    layout="wide"
)

# ----------------------
# HOME / LANDING PAGE
# ----------------------
if st.session_state.page == "home":
    st.markdown("""
    <style>
    .overview-box {
        background-color: #0f3d3e;
        padding: 40px;
        border-radius: 12px;
        color: white;
        height: 100%;
    }
    .overview-box h1 { color: #ffffff; }
    .overview-box p { font-size: 16px; line-height: 1.6; }
    .action-box { padding: 60px 40px; }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([2, 1])

    # -------- LEFT: OVERVIEW --------
    with left:
        st.markdown("""
        <div class="overview-box">
            <h1>NiDAH Programme Portal</h1>
            <h4>National Integrated Diaspora Health Programme</h4>
            <br>
            <p>
            The National Integrated Diaspora Health (NiDAH) Programme is a strategic
            initiative aimed at strengthening Nigeria’s health system through structured
            engagement of health professionals across training and service delivery.
            </p>
            <p>
            This portal serves as the official platform for registration, programme selection,
            coordination, and monitoring of NiDAH-supported activities nationwide.
            </p>
            <p>
            Health professionals can apply for training opportunities or participate
            in service delivery initiatives aligned with national health priorities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # -------- RIGHT: ACTIONS --------
    with right:
        st.markdown("<div class='action-box'>", unsafe_allow_html=True)
        st.subheader("Get Started")
        if st.button("📝 Health Professional Registration", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()
        st.write("")
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.page = "admin_login"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------
# REGISTRATION PAGE
# ----------------------
elif st.session_state.page == "register":
    st.title("Health Professional Registration")
    st.info("🔒 Your information will be stored securely and used strictly for NiDAH Programme purposes.")

    with st.form("registration_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
        nationality = st.text_input("Nationality")
        phone = st.text_input("Phone Number")
        cadre = st.selectbox("Cadre", ["Oncology", "Cardiac Care", "Urology", "Neurology"])
        sub_specialty = st.text_input("Sub-specialty")
        start_date = st.date_input("Start Date of Availability", min_value=date(2000,1,1))
        end_date = st.date_input("End Date of Availability", min_value=start_date)
        preferred_states = st.multiselect("Preferred States (max 3)", ["Lagos","Kano","Rivers","Delta","Abuja"])
        preferred_lgas = st.text_input("Preferred LGAs (after selecting states)")
        consent = st.checkbox("I consent to the storage and use of my information for the NiDAH Programme")

        submitted = st.form_submit_button("Submit Registration")

        if submitted:
            if not consent:
                st.error("Consent is required to proceed.")
            elif not full_name or not email:
                st.error("Full Name and Email are required.")
            else:
                try:
                    with engine.connect() as conn:
                        insert_query = text("""
                            INSERT INTO health_professionals
                            (full_name, email, gender, nationality, phone, cadre, sub_specialty,
                             start_date, end_date, preferred_states, preferred_lgas, consent)
                            VALUES
                            (:full_name, :email, :gender, :nationality, :phone, :cadre, :sub_specialty,
                             :start_date, :end_date, :preferred_states, :preferred_lgas, :consent)
                        """)
                        conn.execute(insert_query, {
                            "full_name": full_name,
                            "email": email,
                            "gender": gender,
                            "nationality": nationality,
                            "phone": phone,
                            "cadre": cadre,
                            "sub_specialty": sub_specialty,
                            "start_date": start_date,
                            "end_date": end_date,
                            "preferred_states": ",".join(preferred_states),
                            "preferred_lgas": preferred_lgas,
                            "consent": consent
                        })
                    st.success("✅ Registration saved to database successfully!")
                except Exception as e:
                    st.error("❌ Failed to save registration.")
                    st.write(e)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ----------------------
# ADMIN LOGIN PAGE
# ----------------------
elif st.session_state.page == "admin_login":
    st.title("Admin Login")

    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            st.error("Admin authentication not implemented yet.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
