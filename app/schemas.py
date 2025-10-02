from pydantic import BaseModel, ConfigDict


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

