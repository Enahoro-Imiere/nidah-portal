from db import get_engine
import streamlit as st

try:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        st.success("Database is connected!")
        st.write("Test query result:", result.fetchone())
except Exception as e:
    st.error("Database connection failed!")
    st.write(e)
