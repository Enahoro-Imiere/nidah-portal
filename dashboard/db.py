from sqlalchemy import create_engine
import streamlit as st

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://nidah_user:12345@localhost:5432/nidah_db"
    )
    return engine
