import streamlit as st

# =====================================================
# PAGE STATE (MUST BE AT THE VERY TOP)
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="NiDAH Portal",
    page_icon="🏥",
    layout="wide"
)

# =====================================================
# HOME / LANDING PAGE
# =====================================================
if st.session_state.page == "home":

    st.markdown(
        """
        <style>
        .overview-box {
            background-color: #0f3d3e;
            padding: 40px;
            border-radius: 12px;
            color: white;
            height: 100%;
        }
        .overview-box h1 {
            color: #ffffff;
        }
        .overview-box p {
            font-size: 16px;
            line-height: 1.6;
        }
        .action-box {
            padding: 60px 40px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([2, 1])

    # -------- LEFT: OVERVIEW --------
    with left:
        st.markdown(
            """
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
            """,
            unsafe_allow_html=True
        )

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

    st.markdown(
        """
        <hr>
        <p style="text-align:center; font-size: 0.85em; color: grey;">
        © NiDAH Programme | Federal Ministry of Health & Social Welfare
        </p>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# HEALTH PROFESSIONAL REGISTRATION PAGE
# =====================================================
elif st.session_state.page == "register":

    st.title("Health Professional Registration")
    st.write("Please complete the form below to register for the NiDAH Programme.")

    st.info("🔒 Your information will be stored securely and used strictly for programme purposes.")

    with st.form("registration_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
        nationality = st.text_input("Nationality")
        phone = st.text_input("Phone Number")

        cadre = st.selectbox(
            "Cadre",
            ["Oncology", "Cardiac Care", "Urology", "Neurology"]
        )

        sub_specialty = st.text_input("Sub-specialty")

        consent = st.checkbox(
            "I consent to the storage and use of my information for the purposes of the NiDAH Programme."
        )

        submitted = st.form_submit_button("Submit Registration")

        if submitted:
            if not consent:
                st.error("Consent is required to proceed.")
            elif not full_name or not email:
                st.error("Full Name and Email are required.")
            else:
                st.success("Registration submitted successfully.")
                st.write("🔜 Database save will be connected next.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# =====================================================
# ADMIN LOGIN PAGE
# =====================================================
elif st.session_state.page == "admin_login":

    st.title("Admin Login")

    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        login = st.form_submit_button("Login")

        if login:
            st.error("Admin authentication will be implemented next.")

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
