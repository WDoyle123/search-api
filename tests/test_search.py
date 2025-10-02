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
