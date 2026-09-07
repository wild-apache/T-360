from fastapi.testclient import TestClient

from t360.api.main import app


def test_health_endpoint() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["mode"] == "backtest"
    assert payload["broker"] == "upstox"
