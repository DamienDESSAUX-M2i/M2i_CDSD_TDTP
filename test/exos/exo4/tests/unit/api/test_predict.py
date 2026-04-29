def test_predict_valid_features_returns_satisfaction(client):
    payload = {"features": [25, 12, 10, 1]}

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert "satisfaction" in data
    assert isinstance(data["satisfaction"], float)
    assert data["timestamp"] is not None


def test_predict_missing_features_returns_400(client):
    response = client.post("/predict", json={})

    assert response.status_code == 400


def test_predict_invalid_features_type_returns_400(client):
    response = client.post("/predict", json={"features": "invalid"})

    assert response.status_code == 400


def test_predict_wrong_length_features_returns_400(client):
    response = client.post("/predict", json={"features": [1, 2]})

    assert response.status_code == 400
