import pytest

import numpy as np


@pytest.fixture
def client():
    from app_satisfaction import app, model, prediction_history

    # Reset global state before each test session
    prediction_history.clear()

    # Inject a deterministic fake model if missing
    class FakeModel:
        def predict(self, X):
            return np.array([7.5 for _ in range(len(X))])

    # Override model for testing stability
    app.model = model if model is not None else FakeModel()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
