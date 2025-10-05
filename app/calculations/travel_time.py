from app.schemas import TravelRequest, TravelResponse


def travel_time(data: TravelRequest) -> TravelResponse:

    speed_kmh = {
        "walking": 5,
        "driving": 30,
        "public_transport": 25
    }

    fixed_overhead_hr = {
        "walking": 0,
        "driving": 0,
        "public_transport": 8 / 60  # 8 minutes in hours
    }

    travel_time_dict = {}

    for mode in data.modes:
        travel_time_hr = (data.distance_km /
                          speed_kmh[mode]) + fixed_overhead_hr[mode]
        travel_time_seconds = travel_time_hr * 60 * 60
        travel_time_seconds_rounded = int(round(travel_time_seconds))
        travel_time_dict[mode] = travel_time_seconds_rounded

    return TravelResponse(travel_times=travel_time_dict)
