def test_default_path(client):
    response = client.get("v1/docs")
    assert response.status_code == 200


def test_bad_path(client):
    response = client.get("/v1/bad-path")
    assert response.status_code == 404

