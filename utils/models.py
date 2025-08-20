# utils/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
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
    conductivity = Column(Float)
    temperature = Column(Float)
    pressure = Column(Float)
    sea_pressure = Column(Float)
    # add other sensor columns as needed
    dissolved_o2_saturation = Column(Float)
    chlorophyll_a = Column(Float)
    fdom = Column(Float)
    turbidity = Column(Float)
    depth = Column(Float)
    salinity = Column(Float)
    speed_of_sound = Column(Float)
    specific_conductivity = Column(Float)
    density_anomaly = Column(Float)
    dissolved_o2_concentration = Column(Float)
