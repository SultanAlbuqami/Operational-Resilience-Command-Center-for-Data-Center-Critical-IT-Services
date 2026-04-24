import pytest
from fastapi.testclient import TestClient

from app.db.seed import seed_data
from app.main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    seed_data()
    yield


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_read_services():
    response = client.get("/api/v1/services/")
    assert response.status_code == 200
    services = response.json()
    assert len(services) >= 11
    assert any(s["name"] == "Customer Identity Platform" for s in services)


def test_trigger_incident():
    payload = {
        "name": "Cooling Failure",
        "description": "Test cooling failure simulation",
    }
    response = client.post("/api/v1/incidents/trigger", json=payload)
    assert response.status_code == 200
    incident = response.json()
    assert incident["name"] == "Cooling Failure"
    assert len(incident["affected_services"]) > 0


def test_recovery_prioritization():
    # First trigger an incident to have affected services
    payload = {
        "name": "Primary Data Center Power Failure",
        "description": "Power failure",
    }
    inc_resp = client.post("/api/v1/incidents/trigger", json=payload)
    incident_id = inc_resp.json()["id"]

    response = client.get(f"/api/v1/recovery/prioritization/{incident_id}")
    assert response.status_code == 200
    scores = response.json()
    assert len(scores) > 0
    # Check if recovery_order is present and correct
    assert scores[0]["recovery_order"] == 1
    assert "total_score" in scores[0]
    assert "business_impact_score" in scores[0]["rationale"]


def test_executive_brief():
    # Reuse an incident
    incidents = client.get("/api/v1/incidents/").json()
    incident_id = incidents[0]["id"]

    response = client.get(f"/api/v1/incidents/{incident_id}/executive-brief")
    assert response.status_code == 200
    brief = response.json()
    assert "incident_summary" in brief
    assert "top_business_impacts" in brief
    assert "escalation_recommendation" in brief
