from typing import List

from app import models
from app.db import get_db
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.schemas import HotelOut, EventOut

from sqlalchemy.orm import Session

router = APIRouter(prefix="/search", tags=["Search"])


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
