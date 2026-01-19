import streamlit as st
from db import get_engine
import pandas as pd
from datetime import date

# ---------------- PAGE STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NiDAH Portal",
    page_icon="🏥",
    layout="centered"
)

if st.session_state.page == "home":
    st.write("")  # placeholder OR your landing page code

elif st.session_state.page == "register":
    st.write("")  # registration page content

elif st.session_state.page == "admin_login":
    st.write("")  # admin login page


# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style="text-align:center;">NiDAH Programme Portal</h1>
    <h4 style="text-align:center; color: grey;">
    National Integrated Diaspora Health Programme
    </h4>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- OVERVIEW ----------------
st.markdown(
    """
    ### Programme Overview

    The **National Integrated Diaspora Health (NiDAH) Programme** is designed to strengthen
    Nigeria’s healthcare system by facilitating structured engagement of health professionals
    across training and service delivery initiatives.

    This portal serves as the official platform for **registration, programme selection,
    and coordination** of participating health professionals and institutions.
    """
)

# ---------------- WHAT YOU CAN DO ----------------
st.markdown(
    """
    ### What You Can Do on This Portal

    - Register as a **Health Professional**
    - Apply for **Training Programmes** (Hybrid, Virtual, Physical)
    - Participate in **Service Delivery Initiatives**
    - Select preferred locations and programme tracks
    - Enable programme monitoring and reporting
    """
)

# ---------------- WHO SHOULD REGISTER ----------------
st.markdown(
    """
    ### Who Should Register

    - Medical specialists and subspecialists
    - Diaspora health professionals
    - Local healthcare practitioners supporting NiDAH initiatives
    """
)

st.divider()

# ---------------- CALL TO ACTION ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Health Professional Registration", use_container_width=True):
        st.session_state.page = "register"

with col2:
    if st.button("🔐 Admin Login", use_container_width=True):
        st.session_state.page = "admin_login"

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; color: grey; font-size: 0.85em;">
    © NiDAH Programme | Federal Ministry of Health & Social Welfare
    </p>
    """,
    unsafe_allow_html=True
)

# --- Form ---
st.header("NiDAH Health Professional Registration")

with st.form("registration_form"):
    # Basic info
    full_name = st.text_input("Full Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
    nationality = st.text_input("Nationality")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")

    # Professional info
    cadre = st.selectbox("Cadre", ["Oncology", "Cardiac Care", "Urology", "Neurology"])
    sub_specialty = st.text_input("Sub-specialty")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date", value=date.today())

    # Preferences
    states = ["Lagos","Oyo","Rivers","Kano","Kaduna"]  # Example states
    preferred_states = st.multiselect("Preferred States (max 3)", states, max_selections=3)

    # Dynamic LGAs (example mapping)
    state_lga_map = {
        "Lagos": ["Ikeja", "Surulere", "Epe"],
        "Oyo": ["Ibadan North", "Ibadan South", "Oyo East"],
        "Rivers": ["Port Harcourt", "Obio/Akpor", "Eleme"],
        "Kano": ["Kano Municipal", "Fagge", "Gwale"],
        "Kaduna": ["Kaduna North", "Kaduna South", "Zaria"]
    }

    lgas = []
    for s in preferred_states:
        lgas.extend(state_lga_map.get(s, []))
    preferred_lgas = st.multiselect("Preferred LGAs", lgas)

    # Consent
    consent = st.checkbox("I consent to the storage and use of my information for the NiDAH program.")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not consent:
            st.error("You must provide consent to continue.")
        elif not full_name or not email:
            st.error("Please fill in all required fields (Full Name and Email).")
        else:
            # Save to DB
            engine = get_engine()
            with engine.connect() as conn:
                insert_query = """
                INSERT INTO professionals 
                (full_name, gender, nationality, phone, email, cadre, sub_specialty, start_date, end_date, preferred_states, preferred_lgas, consent_given, consent_timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, NOW())
                """
                conn.execute(
                    insert_query,
                    (
                        full_name, gender, nationality, phone, email,
                        cadre, sub_specialty, start_date, end_date,
                        preferred_states, preferred_lgas
                    )
                )
            st.success(f"Thank you {full_name}, your registration has been saved successfully!")

    except Exception as e:
    st.error("Something went wrong. Please contact the administrator.")

