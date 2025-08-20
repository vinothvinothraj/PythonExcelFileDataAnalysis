# config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Change username/password/DB as needed
DB_USER = "root"
DB_PASS = ""
DB_HOST = "localhost"
DB_NAME = "excel_analyzer"

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
