import pytest
from pydantic import ValidationError
from app.schemas import TravelRequest, TravelResponse, HotelInRange, HotelOut, EventOut


def test_travel_request_valid():
    """Test TravelRequest with valid data"""
    request = TravelRequest(
        modes=["walking", "driving"], 
        distance_km=5.5
    )
    assert request.modes == ["walking", "driving"]
    assert request.distance_km == 5.5


def test_travel_request_invalid_modes():
    """Test TravelRequest with invalid modes"""
    with pytest.raises(ValidationError):
        TravelRequest(
            modes=["invalid_mode"], 
            distance_km=5.5
        )


def test_travel_request_negative_distance():
    """Test TravelRequest with negative distance"""
    with pytest.raises(ValidationError):
        TravelRequest(
            modes=["walking"], 
            distance_km=-1.0
        )


def test_travel_request_zero_distance():
    """Test TravelRequest with zero distance"""
    with pytest.raises(ValidationError):
        TravelRequest(
            modes=["walking"], 
            distance_km=0.0
        )


def test_travel_response():
    """Test TravelResponse creation"""
    response = TravelResponse(
        travel_times={"walking": 1.5, "driving": 0.3}
    )
    assert response.travel_times == {"walking": 1.5, "driving": 0.3}


def test_hotel_in_range():
    """Test HotelInRange schema"""
    hotel = HotelInRange(
        hotelID=101,
        latitude=51.5033,
        longitude=-0.1195,
        distance=0.5,
        travel_times={"walking": 0.1}
    )
    assert hotel.hotelID == 101
    assert hotel.latitude == 51.5033
    assert hotel.longitude == -0.1195
    assert hotel.distance == 0.5
    assert hotel.travel_times == {"walking": 0.1}


def test_hotel_out():
    """Test HotelOut schema"""
    hotel = HotelOut(
        hotelID=101,
        latitude=51.5033,
        longitude=-0.1195
    )
    assert hotel.hotelID == 101
    assert hotel.latitude == 51.5033
    assert hotel.longitude == -0.1195


def test_event_out():
    """Test EventOut schema"""
    event = EventOut(
        eventID=1,
        latitude=51.5007,
        longitude=-0.1246
    )
    assert event.eventID == 1
    assert event.latitude == 51.5007
    assert event.longitude == -0.1246


def test_travel_request_all_modes():
    """Test TravelRequest with all valid modes"""
    request = TravelRequest(
        modes=["walking", "driving", "public_transport"], 
        distance_km=10.0
    )
    assert len(request.modes) == 3
    assert "walking" in request.modes
    assert "driving" in request.modes
    assert "public_transport" in request.modes


def test_travel_request_single_mode():
    """Test TravelRequest with single mode"""
    for mode in ["walking", "driving", "public_transport"]:
        request = TravelRequest(
            modes=[mode], 
            distance_km=1.0
        )
        assert request.modes == [mode]


def test_travel_request_duplicate_modes():
    """Test TravelRequest with duplicate modes"""
    request = TravelRequest(
        modes=["walking", "walking"], 
        distance_km=1.0
    )
    # Pydantic should allow duplicates (though it's not ideal)
    assert request.modes == ["walking", "walking"]


def test_travel_request_mixed_valid_invalid():
    """Test TravelRequest with mix of valid and invalid modes"""
    with pytest.raises(ValidationError):
        TravelRequest(
            modes=["walking", "invalid"], 
            distance_km=1.0
        )