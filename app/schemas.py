from pydantic import BaseModel, ConfigDict

class HotelInRange(BaseModel):
    hotelID: int
    latitude: float
    longitude: float 
    distance_km: float
    estimated_travel: str

    model_config = ConfigDict(from_attributes=True)


class HotelOut(BaseModel):
    hotelID: int
    latitude: float
    longitude: float 

    model_config = ConfigDict(from_attributes=True)

class EventOut(BaseModel):
    eventID: int
    latitude: float
    longitude: float 

    model_config = ConfigDict(from_attributes=True)

