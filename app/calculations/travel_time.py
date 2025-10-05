from pydantic import BaseModel, Field
from pydantic.types import conlist, confloat
from typing import Literal, Dict


class TravelRequest(BaseModel):
    modes: conlist(Literal["walking", "driving",
                   "public_transport"])
    distance_km: confloat(
        gt=0) = Field(..., description="Distance in kilometers, must be positive")


class TravelResponse(BaseModel):
    travel_times: Dict[str, float]


def travel_time(data: TravelRequest) -> TravelResponse:

    speed_kmh = {
        "walking": 5,
        "driving": 30,
        "public_transport": 25
    }

    fixed_overhead_hr = {
        "walking": 0,
        "driving": 0,
        "public_transport": 8 / 60  # 8 minutes
    }

    travel_time_dict = {}

    for mode in data.modes:
        travel_time_hr = (data.distance_km /
                          speed_kmh[mode]) + fixed_overhead_hr[mode]
        travel_time_dict[mode] = travel_time_hr

    return TravelResponse(travel_times=travel_time_dict)
