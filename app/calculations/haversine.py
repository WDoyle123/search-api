import math

def haversine(coordinate_1, coordinate_2):
    """
    φ = latitude
    λ = longitude

    a = sin²(φB - φA/2) + cos φA * cos φB * sin²(λB - λA/2)
    c = 2 * atan2( √a, √(1−a) )
    d = R ⋅ c
    """
    # Radius of Earth in meteres (IUGG Mean Radius)
    R = 6371008.7714

    latitude_1, longitude_1 = coordinate_1
    latitude_2, longitude_2 = coordinate_2

    # Convert decimal degrees to radians
    phi_1 = math.radians(latitude_1)
    phi_2 = math.radians(latitude_2)

    delta_phi = phi_1 - phi_2
    delta_lambda = math.radians(longitude_2 - longitude_1)

    a = (math.sin(delta_phi / 2) ** 2) + (math.cos(phi_1) *
                                          math.cos(phi_2) * math.sin(delta_lambda / 2) ** 2)
    a_clamped = max(0.0, min(1.0, a))

    c = 2 * math.atan2(math.sqrt(a_clamped), math.sqrt(1 - a_clamped))
    distance_in_km = (R * c) / 1000

    return round(distance_in_km, 1)
