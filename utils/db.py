# utils/db.py
from config import SessionLocal, engine

def get_session():
    return SessionLocal()

def get_connection():
    """Return a raw DB-API connection backed by SQLAlchemy's engine.

    This is used by code paths that expect a `.cursor()` and `%s` paramstyle
    (e.g., pandas read_sql with a DB-API connection, and manual INSERTs).
    """
    return engine.raw_connection()
