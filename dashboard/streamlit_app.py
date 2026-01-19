import streamlit as st

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Page title
st.title("NiDAH Portal")

# Make left column wider (e.g., 3:1 ratio)
col_left, col_right = st.columns([3, 1])  # left column now wider

# ----------------------------
# LEFT COLUMN: Overview with background
# ----------------------------
with col_left:
    st.markdown(
        """
        <div style="
            background-color: #f0f8ff; 
            padding: 25px; 
            border-radius: 10px;
            height: 100%;
            overflow-y: auto;
        ">
        <h3>Overview</h3>
        <p>
        Nigeria's health system, despite pockets of excellence, faces significant challenges, 
        including a critical shortage of skilled health workers, infrastructural deficits, 
        and gaps in specialized medical services. A primary driver of this human resource crisis 
        is the continuous emigration of highly trained medical professionals to higher income 
        countries in search of better opportunities—a phenomenon colloquially known as "japa." 
        The World Health Organization (WHO) estimates a shortage of nearly 300,000 doctors and 
        nurses in Nigeria, a gap that severely impacts healthcare delivery, particularly in 
        rural and underserved communities.
        </p>
        <p>
        Paradoxically, Nigeria possesses a vast and highly skilled diaspora of health professionals 
        who are global leaders in their respective fields. Thousands of Nigerian doctors, nurses, 
        pharmacists, and allied health professionals are making significant contributions to the 
        health systems of countries like the United States, the United Kingdom, Canada, and Saudi Arabia. 
        This community represents an immense reservoir of knowledge, advanced clinical skills, 
        and modern healthcare management expertise that is currently underutilized for national development.
        </p>
        <p>
        International evidence indicates that diaspora health workers can play a critical role 
        in strengthening health systems and services in low- or middle-income countries of heritage, 
        as well as in their host countries. While permanent return is a complex personal decision, 
        there is a strong, expressed desire among many diaspora professionals to contribute to Nigeria's development. 
        A structured, short-term engagement scheme offers a pragmatic "brain circulation" or "brain gain" model, 
        providing a bridge for this talent to flow back into the country, even if temporarily. 
        The Nigerian Diaspora Health Vanguard Initiative (NDHVI) is conceived as a formal, sustainable mechanism 
        to facilitate this two-way exchange, transforming brain drain into a strategic national asset.
        </p>
        </div>
        """, unsafe_allow_html=True
    )

# ----------------------------
# RIGHT COLUMN: Sign-in Pane with background
# ----------------------------
with col_right:
    st.markdown(
        """
        <div style="
            background-color: #e6f7ff; 
            padding: 25px; 
            border-radius: 10px;
        ">
        <h3>Sign In</h3>
        </div>
        """, unsafe_allow_html=True
    )

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
            st.write("Redirecting to registration page...")  # Replace with actual registration logic
    with fp_col:
        if st.button("Forgot Password"):
            st.session_state.page = "forgot_password"
            st.write("Redirecting to password recovery...")  # Replace with actual recovery logic

# ----------------------------
# PAGE NAVIGATION PLACEHOLDER
# ----------------------------
if st.session_state.page == "login":
    st.write("Login form would appear here.")
elif st.session_state.page == "register":
    st.write("Registration form would appear here.")
elif st.session_state.page == "forgot_password":
    st.write("Forgot password form would appear here.")
