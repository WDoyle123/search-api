from sqlalchemy import Column, Integer, Float
from app.db import Base

class Events(Base):
    __tablename__ = "events"

    eventID = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class Hotels(Base):
    __tablename__ = "hotels"

    hotelID = Column(Integer, primary_key=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
