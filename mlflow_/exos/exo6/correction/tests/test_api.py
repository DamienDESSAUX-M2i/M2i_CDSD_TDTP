import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api"))


VALID_PAYLOAD = {
    "type": "M",
    "air_temperature": 298.1,
    "process_temperature": 308.6,
    "rotational_speed": 1551,
    "torque": 42.8,
    "tool_wear": 200,
}


@pytest.fixture(scope="module")
def mock_loader():
    with patch("api.model_loader.model_loader") as mock:
        mock.is_loaded = True
        mock.version = "test-v1"
        mock.predict_proba = MagicMock(return_value=np.array([0.8]))
        mock.predict = MagicMock(return_value=np.array([1]))
        yield mock


@pytest.fixture(scope="module")
def client(mock_loader):
    from api.main import app
    return TestClient(app)

class TestHealthEndpoint:

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_model_loaded(self, client):
        data = client.get("/health").json()
        assert data["model_loaded"] is True

    def test_health_has_version(self, client):
        data = client.get("/health").json()
        assert data["model_version"] == "test-v1"


class TestPredictEndpoint:

    def test_predict_returns_200(self, client):
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 200

    def test_predict_response_schema(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        for field in ("machine_failure", "failure_probability",
                      "risk_level", "recommendation", "model_version"):
            assert field in data, f"Champ manquant dans la reponse : {field}"

    def test_predict_probability_range(self, client):
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert 0.0 <= data["failure_probability"] <= 1.0

    def test_predict_high_proba_gives_critical(self, client, mock_loader):
        mock_loader.predict_proba = MagicMock(return_value=np.array([0.8]))
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["risk_level"] == "CRITICAL"

    def test_predict_low_proba_gives_low_risk(self, client, mock_loader):
        mock_loader.predict_proba = MagicMock(return_value=np.array([0.05]))
        data = client.post("/predict", json=VALID_PAYLOAD).json()
        assert data["risk_level"] == "LOW"
        assert data["machine_failure"] is False

class TestPredictValidation:

    def test_invalid_type_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "type": "X"}
        assert client.post("/predict", json=payload).status_code == 422

    def test_temperature_out_of_range_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "air_temperature": 999.0}
        assert client.post("/predict", json=payload).status_code == 422

    def test_negative_tool_wear_returns_422(self, client):
        payload = {**VALID_PAYLOAD, "tool_wear": -1}
        assert client.post("/predict", json=payload).status_code == 422

    def test_missing_field_returns_422(self, client):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "torque"}
        assert client.post("/predict", json=payload).status_code == 422

    def test_all_machine_types_accepted(self, client):
        for machine_type in ["L", "M", "H"]:
            payload = {**VALID_PAYLOAD, "type": machine_type}
            assert client.post("/predict", json=payload).status_code == 200


class TestBatchPredictEndpoint:

    def test_batch_returns_200(self, client):
        batch = [VALID_PAYLOAD, {**VALID_PAYLOAD, "type": "L"}]
        assert client.post("/predict/batch", json=batch).status_code == 200

    def test_batch_returns_correct_count(self, client):
        batch = [VALID_PAYLOAD] * 5
        data = client.post("/predict/batch", json=batch).json()
        assert len(data) == 5

    def test_batch_max_100(self, client):
        batch = [VALID_PAYLOAD] * 101
        assert client.post("/predict/batch", json=batch).status_code == 422


class TestMetricsEndpoint:

    def test_metrics_returns_200(self, client):
        assert client.get("/metrics").status_code == 200

    def test_metrics_schema(self, client):
        data = client.get("/metrics").json()
        for field in ("total_predictions", "failure_predictions",
                      "failure_rate", "uptime_seconds"):
            assert field in data

    def test_metrics_increments_after_predict(self, client, mock_loader):
        mock_loader.predict_proba = MagicMock(return_value=np.array([0.8]))
        before = client.get("/metrics").json()["total_predictions"]
        client.post("/predict", json=VALID_PAYLOAD)
        after = client.get("/metrics").json()["total_predictions"]
        assert after == before + 1
