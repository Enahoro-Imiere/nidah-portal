import streamlit as st

# ----------------------------
# Initialize session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "reg_page" not in st.session_state:
    st.session_state.reg_page = "choose_type"
if "user_type_lookup" not in st.session_state:
    st.session_state.user_type_lookup = {}  # Store users temporarily
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# ----------------------------
# Homepage
# ----------------------------
if st.session_state.page == "home":
    st.title("NiDAH Programme Portal")
    
    # Two-column layout: Overview | Sign-in
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Overview")
        st.markdown("""
        Nigeria's health system, despite pockets of excellence, faces significant challenges, 
        including a shortage of skilled health workers, infrastructural deficits, and gaps in specialized medical services. 
        A primary driver is the emigration of highly trained medical professionals, known as "japa."
        
        Nigeria possesses a vast skilled diaspora in countries like the US, UK, Canada, and Saudi Arabia. 
        The Nigerian Diaspora Health Vanguard Initiative (NDHVI) aims to facilitate structured short-term engagement, 
        transforming brain drain into a strategic national asset.
        """)
    
    with col2:
        st.subheader("Sign In")
        if st.button("Sign In"):
            st.session_state.page = "login"
        st.markdown("---")
        st.write("New here?")
        if st.button("Register"):
            st.session_state.page = "register"
            st.session_state.reg_page = "choose_type"

# ----------------------------
# Registration Page
# ----------------------------
elif st.session_state.page == "register":
    st.title("Registration")
    
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
            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password or not email:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[email] = {
                        "type": "health_professional",
                        "username": username,
                        "password": password
                    }
                    st.success(f"Thank you {full_name}! Registration successful.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"
    
    # --------- Association / Organization Form ---------
    elif st.session_state.reg_page == "association":
        st.subheader("Association / Organization Registration")
        with st.form("assoc_form"):
            name = st.text_input("Name of Association / Organization")
            country = st.text_input("Country")
            state = st.text_input("State")
            email = st.text_input("Email Address")
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            consent = st.checkbox("I consent to the storage and use of this information for the NiDAH Programme")
            
            submitted = st.form_submit_button("Submit Registration")
            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password or not email:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[email] = {
                        "type": "association",
                        "username": username,
                        "password": password
                    }
                    st.success(f"Thank you {name}! Registration successful.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"
    
    # --------- Facility Form ---------
    elif st.session_state.reg_page == "facility":
        st.subheader("Facility Registration")
        with st.form("facility_form"):
            facility_name = st.text_input("Name of Facility")
            state = st.text_input("State")
            needs = st.text_area("Facility Needs")
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            consent = st.checkbox("I consent to the storage and use of this information for the NiDAH Programme")
            
            submitted = st.form_submit_button("Submit Registration")
            if submitted:
                if not consent:
                    st.error("You must give consent to continue.")
                elif not username or not password:
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state.user_type_lookup[facility_name] = {
                        "type": "facility",
                        "username": username,
                        "password": password
                    }
                    st.success(f"Thank you! The registration for {facility_name} has been submitted successfully.")
                    st.session_state.page = "login"
                    st.session_state.reg_page = "choose_type"

# ----------------------------
# Login Page
# ----------------------------
elif st.session_state.page == "login":
    st.title("Sign In")
    
    email_or_name = st.text_input("Email / Facility Name")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        user_info = st.session_state.user_type_lookup.get(email_or_name)
        if not email_or_name or not password:
            st.error("Please enter your credentials.")
        elif user_info and password == user_info["password"]:
            st.session_state.page = "dashboard"
            st.session_state.user_email = email_or_name
        else:
            st.error("Invalid credentials.")

# ----------------------------
# Dashboard Page
# ----------------------------
elif st.session_state.page == "dashboard":
    st.title(f"Welcome, {st.session_state.user_email}")
    user_info = st.session_state.user_type_lookup.get(st.session_state.user_email)
    
    if user_info["type"] in ["health_professional", "association"]:
        st.subheader("Choose a Program to Volunteer In")
        program = st.selectbox("Select Program", ["", "Services", "Training"])
        if program == "Services":
            service = st.selectbox("Select Service", ["", "Neurology", "Urology", "Gynaecology"])
            if service:
                st.success(f"You selected to volunteer in **{service}** service.")
        elif program == "Training":
            training_type = st.selectbox("Select Training Type", ["", "Virtual", "Hybrid", "Physical"])
            if training_type:
                st.success(f"You selected to participate in **{training_type}** training.")
    elif user_info["type"] == "facility":
        st.subheader("Facility Dashboard")
        st.write("Here you could manage your facility profile, needs, and updates.")

    if st.button("Logout"):
        st.session_state.page = "home"
        st.session_state.user_email = None
