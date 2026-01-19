import streamlit as st

# ----------------------------
# Initialize session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reg_page" not in st.session_state:
    st.session_state.reg_page = "choose_type"
if "user_type_lookup" not in st.session_state:
    st.session_state.user_type_lookup = {}
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ----------------------------
# Custom CSS for backgrounds
# ----------------------------
st.markdown("""
<style>
.overview-bg {
    background-color: #e8f0fe;
    padding: 20px;
    border-radius: 100px;
}
.signin-bg {
    background-color: #fef3e8;
    padding: 20px;
    border-radius: 100px;
}
.form-bg {
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Homepage / Landing Page
# ----------------------------
if st.session_state.page == "home":
    st.title("NiDAH Programme Portal")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="overview-bg">', unsafe_allow_html=True)
        st.subheader("Overview")
        st.markdown("""
        Nigeria's health system, despite pockets of excellence, faces significant challenges, 
        including a shortage of skilled health workers, infrastructural deficits, and gaps in specialized medical services. 
        A primary driver is the emigration of highly trained medical professionals, known as "japa."
        
        Nigeria possesses a vast skilled diaspora in countries like the US, UK, Canada, and Saudi Arabia. 
        The Nigerian Diaspora Health Vanguard Initiative (NDHVI) aims to facilitate structured short-term engagement, 
        transforming brain drain into a strategic national asset.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="signin-bg">', unsafe_allow_html=True)
        st.subheader("Sign In")
        if st.button("Sign In"):
            st.session_state.page = "login"
        st.markdown("---")
        st.write("New here?")
        if st.button("Register"):
            st.session_state.page = "register"
            st.session_state.reg_page = "choose_type"
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Registration Page
# ----------------------------
elif st.session_state.page == "register":
    st.title("Registration")

    if st.button("← Back to Homepage"):
        st.session_state.page = "home"

    if st.session_state.reg_page == "choose_type":
        choice = st.radio("Register as:", ["Health Professional", "Association / Organization", "Facility"])
        if st.button("Continue"):
            if choice == "Health Professional":
                st.session_state.reg_page = "health_professional"
            elif choice == "Association / Organization":
                st.session_state.reg_page = "association"
            elif choice == "Facility":
                st.session_state.reg_page = "facility"

    # --------- Health Professional Form ---------
    elif st.session_state.reg_page == "health_professional":
        st.subheader("Health Professional Registration")
        with st.form("hp_registration_form"):
            st.markdown('<div class="form-bg">', unsafe_allow_html=True)
            full_name = st.text_input("Full Name")
            country = st.text_input("Country")
            state = st.text_input("State")
            email = st.text_input("Email Address")
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            cadre = st.selectbox("Cadre", ["Medical Doctor", "Nurse", "Pharmacist"])
            specialty = st.text_input("Specialty")
            subspecialty = st.text_input("Sub-Specialty")
            consent = st.checkbox("I consent to the storage and use of my information for the NiDAH Programme")
            submitted = st.form_submit_button("Submit Registration")
            st.markdown('</div>', unsafe_allow_html=True)

            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[username] = {
                        "type": "health_professional",
                        "full_name": full_name,
                        "email": email,
                        "password": password
                    }
                    st.success(f"Thank you {full_name}! Registration successful.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"

    # --------- Association / Organization Form ---------
    elif st.session_state.reg_page == "association":
        st.subheader("Association / Organization Registration")
        with st.form("assoc_form"):
            st.markdown('<div class="form-bg">', unsafe_allow_html=True)
            name = st.text_input("Name of Association / Organization")
            country = st.text_input("Country")
            state = st.text_input("State")
            email = st.text_input("Email Address")
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            consent = st.checkbox("I consent to the storage and use of this information for the NiDAH Programme")
            submitted = st.form_submit_button("Submit Registration")
            st.markdown('</div>', unsafe_allow_html=True)

            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[username] = {
                        "type": "association",
                        "name": name,
                        "email": email,
                        "password": password
                    }
                    st.success(f"Thank you {name}! Registration successful.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"

    # --------- Facility Form ---------
    elif st.session_state.reg_page == "facility":
        st.subheader("Facility Registration")
        with st.form("facility_form"):
            st.markdown('<div class="form-bg">', unsafe_allow_html=True)
            facility_name = st.text_input("Name of Facility")
            state = st.text_input("State")
            needs = st.text_area("Facility Needs")
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            consent = st.checkbox("I consent to the storage and use of this information for the NiDAH Programme")
            submitted = st.form_submit_button("Submit Registration")
            st.markdown('</div>', unsafe_allow_html=True)

            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[username] = {
                        "type": "facility",
                        "facility_name": facility_name,
                        "state": state,
                        "needs": needs,
                        "password": password
                    }
                    st.success(f"Thank you! Registration for {facility_name} submitted successfully.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"

# ----------------------------
# Login Page
# ----------------------------
elif st.session_state.page == "login":
    st.title("Sign In")
    
    if st.button("← Back to Homepage"):
        st.session_state.page = "home"

    st.markdown("---")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Sign In"):
        user_info = st.session_state.user_type_lookup.get(username_input)
        if not username_input or not password_input:
            st.error("Please enter your credentials.")
        elif user_info and password_input == user_info["password"]:
            st.session_state.page = "dashboard"
            st.session_state.user_email = username_input
        else:
            st.error("Invalid username or password.")

# ----------------------------
# Dashboard Page
# ----------------------------
elif st.session_state.page == "dashboard":
    st.title(f"Welcome, {st.session_state.user_email}")
    user_info = st.session_state.user_type_lookup.get(st.session_state.user_email)

    if user_info["type"] in ["health_professional", "association"]:
        st.subheader("Volunteer Programs")

        # Services panel
        with st.expander("Services"):
            st.write("Choose a service to volunteer in:")
            service = st.selectbox("Select Service", ["", "Neurology", "Urology", "Gynaecology"])
            if service:
                st.success(f"You selected to volunteer in **{service}** service.")

        # Training panel
        with st.expander("Training"):
            st.write("Choose a training type to participate in:")
            training_type = st.selectbox("Select Training Type", ["", "Virtual", "Hybrid", "Physical"])
            if training_type:
                st.success(f"You selected to participate in **{training_type}** training.")

    elif user_info["type"] == "facility":
        st.subheader("Facility Dashboard")
        st.write("Manage your facility profile, needs, and updates here.")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.page = "home"
        st.session_state.user_email = None
