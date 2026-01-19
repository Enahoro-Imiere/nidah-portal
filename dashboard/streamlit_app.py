import streamlit as st

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="NiDAH Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>
.main .block-container {
    max-width: 1200px;
    padding-left: 20px;
    padding-right: 20px;
}
.scrollable-overview {
    overflow-y: auto;
    max-height: 600px;
}
.signin-pane {
    background-color: #e6f7ff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #ccc;
}
.stButton>button {
    border-radius: 10px;
    padding: 8px 20px;
    background-color: #4a90e2;
    color: white;
    font-weight: bold;
    border: none;
    cursor: pointer;
    margin-top: 10px;
}
.stButton>button:hover {
    background-color: #357abd;
}
.inline-btns .stButton>button {
    width: 100%;
    background-color: #4a90e2;
}
.inline-btns .stButton>button:hover {
    background-color: #357abd;
}
.reg-card {
    background-color: #f0f8ff;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session state for page navigation
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reg_page" not in st.session_state:
    st.session_state.reg_page = "choose_type"

# ----------------------------
# ---------- HOMEPAGE ----------
# ----------------------------
if st.session_state.page == "home":
    st.title("NiDAH Portal")
    col_left, col_right = st.columns([3, 1])

    # LEFT COLUMN: Overview
    with col_left:
        st.markdown("""
        <div class="scrollable-overview" style="background-color: #f0f8ff; padding: 25px; border-radius: 15px;">
        <h3>Overview</h3>
        <p>
        Nigeria's health system, despite pockets of excellence, faces significant challenges, 
        including a critical shortage of skilled health workers, infrastructural deficits, 
        and gaps in specialized medical services. A primary driver of this human resource crisis 
        is the continuous emigration of highly trained medical professionals to higher income 
        countries in search of better opportunities—a phenomenon colloquially known as "japa." 
        The WHO estimates a shortage of nearly 300,000 doctors and nurses in Nigeria.
        </p>
        <p>
        Nigeria possesses a vast and highly skilled diaspora of health professionals who are global leaders 
        in their respective fields. Thousands of Nigerian doctors, nurses, pharmacists, and allied health professionals
        are making significant contributions to the health systems of countries like the US, UK, Canada, and Saudi Arabia.
        This community represents an immense reservoir of knowledge and expertise currently underutilized for national development.
        </p>
        <p>
        International evidence indicates that diaspora health workers can play a critical role 
        in strengthening health systems in countries of heritage. A structured, short-term engagement 
        scheme offers a pragmatic "brain circulation" model. The Nigerian Diaspora Health Vanguard Initiative (NDHVI) 
        is conceived as a formal, sustainable mechanism to facilitate this two-way exchange.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT COLUMN: Sign-in Pane
    with col_right:
        st.markdown('<div class="signin-pane">', unsafe_allow_html=True)
        st.subheader("Sign In")
        username = st.text_input("Email / Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In"):
            st.session_state.page = "login"
            st.write("Signing in...")  # Replace with actual login logic

        # Bottom row: Register and Forgot Password
        reg_col, fp_col = st.columns(2)
        with reg_col:
            if st.button("Register"):
                st.session_state.page = "register"
        with fp_col:
            if st.button("Forgot Password"):
                st.session_state.page = "forgot_password"
                st.write("Redirecting to password recovery...")
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# ---------- REGISTRATION PAGE ----------
# ----------------------------
elif st.session_state.page == "register":
    st.title("Register for NiDAH Programme")

    # Step 1: Choose registration type
    if st.session_state.reg_page == "choose_type":
        st.subheader("Register as:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Health Professional"):
                st.session_state.reg_page = "health_professional"
        with col2:
            if st.button("Health Association / Organization"):
                st.session_state.reg_page = "association"
        with col3:
            if st.button("Facility"):
                st.session_state.reg_page = "facility"

    # ---------------- Health Professional Registration Form ----------------
    elif st.session_state.reg_page == "health_professional":
        st.subheader("Health Professional Registration")
        with st.form("hp_registration_form"):
            full_name = st.text_input("Full Name")
            country = st.text_input("Country")
            state = st.text_input("State")  # Typed by user
            email = st.text_input("Email Address")
            cadre = st.selectbox("Cadre", ["Medical Doctor", "Nurse", "Pharmacist"])
            specialty = st.text_input("Specialty")
            subspecialty = st.text_input("Sub-Specialty")

            consent = st.checkbox("I consent to the storage and use of my information for the NiDAH Programme")

            submitted = st.form_submit_button("Submit Registration")
            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                else:
                    st.success(f"Thank you {full_name}! Your registration has been submitted successfully.")

    # ---------------- Association / Organization Form ----------------
    elif st.session_state.reg_page == "association":
        st.subheader("Health Association / Organization Registration")
        with st.form("assoc_form"):
            name = st.text_input("Association / Organization Name")
            country = st.text_input("Country")
            state = st.text_input("State")
            email = st.text_input("Email Address")
            submitted = st.form_submit_button("Submit Association Registration")
            if submitted:
                st.success("Association / Organization registration submitted! (DB integration pending)")

    # ---------------- Facility Form ----------------
    elif st.session_state.reg_page == "facility":
        st.subheader("Facility Registration")
        with st.form("facility_form"):
            facility_name = st.text_input("Facility Name")
            state = st.text_input("State")
            email = st.text_input("Email Address")
            submitted = st.form_submit_button("Submit Facility Registration")
            if submitted:
                st.success("Facility registration submitted! (DB integration pending)")

    # Back button
    if st.button("Back"):
        st.session_state.reg_page = "choose_type"
        st.session_state.page = "home"

# ----------------------------
# PAGE PLACEHOLDERS
# ----------------------------
elif st.session_state.page == "login":
    st.title("Login Page")
    st.write("Login form would appear here.")

elif st.session_state.page == "forgot_password":
    st.title("Forgot Password Page")
    st.write("Forgot password form would appear here.")
