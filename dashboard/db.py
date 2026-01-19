# db_test.py — temporary for DB connection test
from sqlalchemy import create_engine, text

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://nidah_user:12345@localhost:5432/nidah_db"
    )
    # test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return engine
