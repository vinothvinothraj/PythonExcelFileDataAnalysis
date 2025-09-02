# utils/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Double
from sqlalchemy.dialects.mysql import DATETIME as MySQLDATETIME
from config import Base
from datetime import datetime

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    uploaded_at = Column(MySQLDATETIME(fsp=6), default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    time = Column(MySQLDATETIME(fsp=6), nullable=False)
    type = Column(String(255), nullable=False)

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    time = Column(MySQLDATETIME(fsp=6), nullable=False)

    # Sensor columns (DOUBLE for high precision, can store negatives, no constraints)
    conductivity = Column(Double)
    temperature = Column(Double)
    pressure = Column(Double)
    sea_pressure = Column(Double)
    dissolved_o2_saturation = Column(Double)
    chlorophyll_a = Column(Double)
    fdom = Column(Double)
    turbidity = Column(Double)
    depth = Column(Double)
    salinity = Column(Double)
    speed_of_sound = Column(Double)
    specific_conductivity = Column(Double)
    density_anomaly = Column(Double)
    dissolved_o2_concentration = Column(Double)
