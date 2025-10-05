from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import conlist, confloat
from typing import Literal, Dict


class TravelRequest(BaseModel):
    modes: conlist(Literal["walking", "driving", "public_transport"])
    distance_km: confloat(
        gt=0) = Field(..., description="Distance in kilometers, must be positive")


class TravelResponse(BaseModel):
    travel_times: Dict[str, float]


class HotelInRange(BaseModel):
    hotelID: int
    latitude: float
    longitude: float
    distance_km: float
    estimated_travel: Dict[str, float]

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
