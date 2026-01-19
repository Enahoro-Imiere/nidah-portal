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
# Custom CSS for styling
# ----------------------------
st.markdown("""
<style>
/* Center content and limit max width */
.main .block-container {
    max-width: 1200px;
    padding-left: 20px;
    padding-right: 20px;
}

/* Scrollable overview */
.scrollable-overview {
    overflow-y: auto;
    max-height: 600px;
}

/* Modern sign-in pane */
.signin-pane {
    background-color: #e6f7ff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

/* Input fields styling */
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #ccc;
}

/* Buttons styling */
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

/* Register/Forgot buttons smaller and inline */
.inline-btns .stButton>button {
    width: 100%;
    background-color: #4a90e2;
}

.inline-btns .stButton>button:hover {
    background-color: #357abd;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Session state for page navigation
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

st.title("NiDAH Portal")

# ----------------------------
# Columns layout (wider left)
# ----------------------------
col_left, col_right = st.columns([3, 1])

# ----------------------------
# Left column: Overview
# ----------------------------
with col_left:
    st.markdown("""
    <div class="scrollable-overview" style="
        background-color: #f0f8ff; 
        padding: 25px; 
        border-radius: 15px;
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
    """, unsafe_allow_html=True)

# ----------------------------
# Right column: Modern Sign-in Pane
# ----------------------------
with col_right:
    st.markdown('<div class="signin-pane">', unsafe_allow_html=True)

    st.subheader("Sign In")
    username = st.text_input("Email / Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        st.session_state.page = "login"
        st.write("Signing in...")  # Replace with real login

    # Register and Forgot Password inline
    reg_col, fp_col = st.columns(2)
    with reg_col:
        if st.button("Register"):
            st.session_state.page = "register"
            st.write("Redirecting to registration page...")
    with fp_col:
        if st.button("Forgot Password"):
            st.session_state.page = "forgot_password"
            st.write("Redirecting to password recovery...")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# PAGE NAVIGATION PLACEHOLDER
# ----------------------------
if st.session_state.page == "login":
    st.write("Login form would appear here.")
elif st.session_state.page == "register":
    st.write("Registration form would appear here.")
elif st.session_state.page == "forgot_password":
    st.write("Forgot password form would appear here.")
