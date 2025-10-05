def test_get_hotels_in_range_event_id(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1")
    assert response.status_code == 200


def test_get_hotels_in_range_no_event_id(client, seed_events):
    response = client.get("v1/search/")
    assert response.status_code == 400


def test_get_hotels_in_range_no_hotels_in_db(client, seed_events):
    response = client.get("v1/search/?event_id=1")
    assert response.status_code == 404


def test_get_hotels_in_range_no_hotels_in_range(client, seed_events, db_session):
    from app import models
    far_hotel = models.Hotels(hotelID=999, latitude=40.7128, longitude=-74.0060)
    db_session.add(far_hotel)
    db_session.commit()
    response = client.get("v1/search/?event_id=1&radius_km=1")
    assert response.status_code == 200
    assert response.json() == []


def test_get_hotels(client, seed_hotels):
    response = client.get("v1/search/hotels")
    assert response.status_code == 200
    assert response.json() == seed_hotels


def test_get_hotels_none(client):
    response = client.get("v1/search/hotels")
    assert response.status_code == 404


def test_get_events(client, seed_events):
    response = client.get("v1/search/events")
    assert response.status_code == 200
    assert response.json() == seed_events


def test_get_events_none(client):
    response = client.get("v1/search/events")
    assert response.status_code == 404


def test_get_hotels_in_range_event_not_found(client, seed_hotels):
    response = client.get("v1/search/?event_id=999")
    assert response.status_code == 404
    assert "Event 999 not found" in response.json()["detail"]


def test_get_hotels_in_range_with_hotels_in_range(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=10&modes=walking,driving")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for hotel in data:
        assert "hotelID" in hotel
        assert "latitude" in hotel
        assert "longitude" in hotel
        assert "distance" in hotel
        assert "travel_times" in hotel
        assert "walking" in hotel["travel_times"]
        assert "driving" in hotel["travel_times"]


def test_get_hotels_in_range_invalid_modes(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=10&modes=invalid_mode")
    assert response.status_code == 400
    assert "Invalid transport mode" in response.json()["detail"]


def test_get_hotels_in_range_mixed_valid_invalid_modes(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=10&modes=walking,invalid_mode")
    assert response.status_code == 400
    assert "Invalid transport mode" in response.json()["detail"]


def test_get_hotels_in_range_all_transport_modes(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=10&modes=walking,driving,public_transport")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for hotel in data:
        assert "travel_times" in hotel
        assert "walking" in hotel["travel_times"]
        assert "driving" in hotel["travel_times"]
        assert "public_transport" in hotel["travel_times"]


def test_get_hotels_in_range_single_mode(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=10&modes=public_transport")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for hotel in data:
        assert "travel_times" in hotel
        assert "public_transport" in hotel["travel_times"]
        assert len(hotel["travel_times"]) == 1


def test_get_hotels_in_range_small_radius(client, seed_events, seed_hotels):
    response = client.get("v1/search/?event_id=1&radius_km=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["hotelID"] == 101
