import streamlit as st
from db import get_engine
import pandas as pd
from datetime import date

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

    st.error("❌ Database connection failed")
    st.write(e)
