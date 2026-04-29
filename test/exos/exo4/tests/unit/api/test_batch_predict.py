def test_batch_predict_valid_input_returns_predictions(client):
    payload = {
        "features_list": [
            [25, 12, 10, 1],
            [40, 5, 3, 0],
        ]
    }

    response = client.post("/batch_predict", json=payload)

    assert response.status_code == 200
    data = response.get_json()

    assert len(data["satisfactions"]) == 2
    assert data["count"] == 2
    assert "timestamp" in data


def test_batch_predict_empty_list_returns_400(client):
    response = client.post("/batch_predict", json={"features_list": []})

    assert response.status_code == 400


def test_batch_predict_invalid_entry_returns_400(client):
    payload = {"features_list": [["invalid", 2, 3, 4]]}

    response = client.post("/batch_predict", json=payload)

    assert response.status_code == 400
