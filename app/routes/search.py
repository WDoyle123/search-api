from typing import List

from app import models
from app.db import get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from app.schemas import HotelInRange, HotelOut, EventOut
from app.calculations import haversine

from sqlalchemy.orm import Session

router = APIRouter(prefix="/search", tags=["Search"])

@router.get(
    "",
)
def list_hotels_in_range(
    db: Session = Depends(get_db),
    event_id: int = Query(..., description="ID of the event to search around"),
    radius_km: int = Query(10, ge=1, le=100, description="Search radius in kilometers"),
    modes: str = Query("walking", description="Comma-separated list of travel modes"),
    sort_by: str = Query("travel time", description="sort criteria: distance, travel time")
):

    return event_id

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
