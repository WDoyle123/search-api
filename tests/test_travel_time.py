import pytest
from app.calculations.travel_time import travel_time, TravelRequest


@pytest.mark.parametrize(
    "modes, distance_km, expected",
    [
        (["walking"], 1, {"walking": pytest.approx(0.2)}),
        (["driving"], 30, {"driving": pytest.approx(1.0)}),
        (["public_transport"], 25, {
         "public_transport": pytest.approx(1 + 8/60)}),
        (
            ["walking", "driving", "public_transport"],
            2,
            {
                "walking": pytest.approx(2/5),
                "driving": pytest.approx(2/30),
                "public_transport": pytest.approx(2/25 + 8/60),
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
