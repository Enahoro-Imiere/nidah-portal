import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="NiDAH Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session state for login/signup
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False
if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": {"password": "admin123", "role": "admin", "name": "Admin User"}}

# -----------------------------
# Custom CSS for inputs and buttons
# -----------------------------
st.markdown("""
    <style>
    /* Input box styling */
    div.stTextInput > label, div.stTextInput > input {
        font-size:16px;
    }
    input {
        border: 2px solid #2E8B57 !important;
        border-radius:10px !important;
        padding:10px !important;
    }
    /* Button styling */
    div.stButton > button {
        background-color:#1E3A8A;
        color:white;
        font-size:16px;
        border-radius:10px;
        padding:8px 16px;
        border:none;
        width:100%;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        background-color:#2E8B57;
        color:white;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Landing page: Overview + Sign-in
# -----------------------------
def landing_page():
    col_overview, col_login = st.columns([2,1])

    # -----------------------------
    # Overview panel (left) - scrollable
    # -----------------------------
    overview_html = """
    <div style="background-color:#F0F8FF; padding:20px; border-radius:10px; height:650px; overflow-y:auto;">
        <h2 style="color:#1E3A8A;">Nigerians in Diaspora Advanced Health Programme (NiDAH)</h2>
        <p style="color:#2E8B57; font-size:16px;">
        Nigeria's health system, despite pockets of excellence, faces significant challenges, 
        including a critical shortage of skilled health workers, infrastructural deficits, 
        and gaps in specialized medical services. A primary driver of this human resource crisis 
        is the continuous emigration of highly trained medical professionals to higher income 
        countries in search of better opportunities ("japa"). The World Health Organization (WHO) 
        estimates a shortage of nearly 300,000 doctors and nurses in Nigeria, a gap that severely 
        impacts healthcare delivery, particularly in rural and underserved communities.
        </p>
        <p style="color:#2E8B57; font-size:16px;">
        Paradoxically, Nigeria possesses a vast and highly skilled diaspora of health professionals 
        who are global leaders in their respective fields. Thousands of Nigerian doctors, nurses, 
        pharmacists, and allied health professionals are making significant contributions to the 
        health systems of countries like the United States, the United Kingdom, Canada, and Saudi Arabia. 
        This community represents an immense reservoir of knowledge, advanced clinical skills, 
        and modern healthcare management expertise that is currently underutilized for national development.
        </p>
        <p style="color:#2E8B57; font-size:16px;">
        International evidence indicates that diaspora health workers can play a critical role 
        in strengthening health systems and services in low- or middle-income countries of heritage. 
        While permanent return is a complex personal decision, there is a strong, expressed desire 
        among many diaspora professionals to contribute to Nigeria's development. A structured, 
        short-term engagement scheme offers a pragmatic "brain circulation" model, providing a bridge 
        for this talent to flow back into the country, even if temporarily. The NiDAH Portal is conceived 
        as a formal, sustainable mechanism to facilitate this two-way exchange, transforming brain drain 
        into a strategic national asset.
        </p>
    </div>
    """
    with col_overview:
        st.markdown(overview_html, unsafe_allow_html=True)

    # -----------------------------
    # Sign-in panel (right) - styled
    # -----------------------------
    with col_login:
        card_html = """
        <div style="background-color:#E6F2FF; padding:30px; border-radius:15px; border: 2px solid #1E3A8A;
                    height:650px; display:flex; flex-direction:column; justify-content:center; box-shadow: 5px 5px 15px rgba(0,0,0,0.1);">
            <h2 style="color:#1E3A8A; text-align:center;">Sign In</h2>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        st.markdown("<div style='padding:10px'></div>", unsafe_allow_html=True)

        username = st.text_input("", placeholder="Username")
        password = st.text_input("", type="password", placeholder="Password")

        login_button = st.button("Login")
        col1, col2 = st.columns(2)
        with col1:
            signup_button = st.button("Sign Up")
        with col2:
            forgot_button = st.button("Forgot Password")

        # Login logic
        if login_button:
            if username in st.session_state.users_db and st.session_state.users_db[username]["password"] == password:
                st.session_state.logged_in = True
                st.success(f"Welcome {st.session_state.users_db[username]['name']}!")
            else:
                st.error("Invalid username or password")
        if signup_button:
            st.session_state.signup_mode = True
        if forgot_button:
            st.info("Password reset not available in dummy portal.")

# -----------------------------
# Sign-up page
# -----------------------------
def signup_page():
    st.write("### Create a New Account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        full_name = st.text_input("Full Name")
        location = st.text_input("Location")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            if username in st.session_state.users_db:
                st.error("Username already exists")
            else:
                st.session_state.users_db[username] = {
                    "password": password,
                    "role": "user",
                    "name": full_name,
                    "location": location
                }
                st.success("Account created successfully! Please login.")
                st.session_state.signup_mode = False

# -----------------------------
# Main flow
# -----------------------------
if not st.session_state.logged_in:
    if st.session_state.signup_mode:
        signup_page()
    else:
        landing_page()
else:
    st.write(f"Logged in as {st.session_state.users_db[st.session_state.current_user]['name']}!")
