import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Layout: Sidebar for overview
with st.sidebar:
    st.markdown("## NiDAH Portal")
    st.markdown("""
    Welcome to the NiDAH Portal!  

    - Register as a health professional  
    - Indicate interest for training or service delivery  
    - Access your profile and programs  
    """)

# Main area: Sign in / Self-registration
st.title("NiDAH Portal")
st.subheader("Sign in or Register")

col1, col2 = st.columns(2)

with col1:
    if st.button("Sign In"):
        st.session_state.page = "login"
        st.write("Redirecting to login page...")

with col2:
    if st.button("Self Registration"):
        st.session_state.page = "register"
        st.write("Redirecting to registration page...")

# Optional: Display page based on session state
if st.session_state.page == "login":
    st.write("Login form will appear here.")
elif st.session_state.page == "register":
    st.write("Registration form will appear here.")
