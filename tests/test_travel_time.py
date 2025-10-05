import pytest
from app.calculations.travel_time import travel_time
from app.schemas import TravelRequest


@pytest.mark.parametrize(
    "modes, distance_km, expected",
    [
        (["walking"], 1, {"walking": 720}),
        (["driving"], 30, {"driving": 3600}),
        (["public_transport"], 25, {
         "public_transport": 4080}),
        (
            ["walking", "driving", "public_transport"],
            2,
            {
                "walking": 1440,
                "driving": 240,
                "public_transport": 768,
            },
        ),
    ],
)
def test_known_pairs(modes, distance_km, expected):
    request = TravelRequest(modes=modes, distance_km=distance_km)
    response = travel_time(request)

    assert set(response.travel_times.keys()) == set(modes)

    for mode, time_expected in expected.items():
        assert response.travel_times[mode] == time_expected
