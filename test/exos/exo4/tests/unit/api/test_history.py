def test_history_empty_returns_empty_list(client):
    response = client.get("/history")

    assert response.status_code == 200
    data = response.get_json()

    assert data["history"] == []
    assert data["total"] == 0


def test_history_after_prediction_returns_entries(client):
    client.post("/predict", json={"features": [25, 12, 10, 1]})

    response = client.get("/history")

    data = response.get_json()

    assert len(data["history"]) == 1
    assert data["total"] == 1
