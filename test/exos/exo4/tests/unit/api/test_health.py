def test_health_endpoint_returns_status_ok_and_model_flag(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "ok"
    assert "model_loaded" in data
    assert "timestamp" in data
