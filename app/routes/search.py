from typing import List
from pydantic import ValidationError

from app import models
from app.db import get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from app.schemas import HotelInRange, HotelOut, EventOut, TravelRequest
from app.calculations.haversine import haversine
from app.calculations.travel_time import travel_time

from sqlalchemy.orm import Session

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "",
    response_model=List[HotelInRange],
)
def list_hotels_in_range(
    db: Session = Depends(get_db),
    event_id: int = Query(..., description="ID of the event to search around"),
    radius_km: int = Query(
        10, ge=1, le=100, description="Search radius in kilometers"),
    modes: str = Query(
        "walking", description="Comma-separated list of travel modes"),
    sort_by: str = Query(
        "travel time", description="sort criteria: distance, travel time")
):

    hotels_in_range = []

    event = db.query(models.Events).filter(
        models.Events.eventID == event_id).one_or_none()

    if event is None:
        raise HTTPException(status_code=404, detail=f"Event {
                            event_id} not found")

    event_coordinates = (event.latitude, event.longitude)

    hotels = (db.query(models.Hotels).all())

    if not hotels:
        raise HTTPException(status_code=404, detail=f"No hotels found")

    modes_array = [m.strip() for m in modes.split(',')]

    for hotel in hotels:

        hotel_coordinates = (hotel.latitude, hotel.longitude)
        haversine_distance = (haversine(event_coordinates, hotel_coordinates))
        hotel.distance_km = haversine_distance

        if hotel.distance_km <= radius_km:
            hotels_in_range.append(hotel)

            try:
                travel_time_request = TravelRequest(
                    modes=modes_array, distance_km=hotel.distance_km)
            except ValidationError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid transport mode(s): {
                        modes_array}. Allowed: walking, driving, public_transport."
                )

            travel_time_response = travel_time(travel_time_request)
            hotel.estimated_travel = travel_time_response.travel_times

    return hotels_in_range


@router.get(
    "/hotels",
    response_model=List[HotelOut],
)
def list_hotels(
    db: Session = Depends(get_db),
):
    hotels = (
        db.query(models.Hotels).all()
    )

    if not hotels:
        raise HTTPException(status_code=404, detail="No hotels found")

    return hotels


@router.get(
    "/events",
    response_model=List[EventOut],
)
def list_events(
    db: Session = Depends(get_db),
):
    Events = (
        db.query(models.Events).all()
    )

    if not Events:
        raise HTTPException(status_code=404, detail="No Events found")

    return Events
