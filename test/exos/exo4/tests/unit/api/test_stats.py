def test_stats_no_predictions_returns_zero(client):
    response = client.get("/stats")

    data = response.get_json()

    assert response.status_code == 200
    assert data["total_predictions"] == 0


def test_stats_with_predictions_returns_metrics(client):
    client.post("/predict", json={"features": [25, 12, 10, 1]})
    client.post("/predict", json={"features": [40, 5, 3, 0]})

    response = client.get("/stats")

    data = response.get_json()

    assert data["total_predictions"] == 2
    assert "average_satisfaction" in data
    assert "min_satisfaction" in data
    assert "max_satisfaction" in data
    assert "std_satisfaction" in data
