import pytest
from app.calculations.haversine import haversine


@pytest.mark.parametrize(
    "a,b,expected_km",
    [
        # Same point -> 0
        ((10.0, 10.0), (10.0, 10.0), 0.0),
        # Antipodes
        ((0.0, 0.0), (0.0, 180.0), 20015.1),
        # Antimeridian crossing
        ((10.0, 179.9), (10.0, -179.9), 21.9),
        # Poles
        ((90.0, 0.0), (-90.0, 0.0), 20015.1),
        # event_id=1 and hotel_id=101
        ((51.5007, -0.1246), (51.5033, -0.1195), 0.5),
        # event_id=1 and hotel_id=102
        ((51.5007, -0.1246), (51.5094, -0.1183), 1.1),
        # event_id=1 and hotel_id=103
        ((51.5007, -0.1246), (51.4952, -0.1469), 1.7),
        # event_id=1 and hotel_id=104
        ((51.5007, -0.1246), (51.5155, -0.0720), 4.0),
        # event_id=1 and hotel_id=105
        ((51.5007, -0.1246), (51.4700, -0.4543), 23.1),
    ],
)
def test_known_pairs(a, b, expected_km):
    assert haversine(a, b) == expected_km


def test_commutativity():
    a = (51.5074, -0.1278)
    b = (48.8566, 2.3522)
    assert haversine(a, b) == haversine(b, a)


def test_rounding_to_one_decimals():
    d = haversine((51.5074, -0.1278), (48.8566, 2.3522))
    assert round(d, 1) == d
