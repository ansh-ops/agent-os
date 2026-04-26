from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_system_status_endpoint() -> None:
    response = client.get("/api/system/status")
    assert response.status_code == 200
    payload = response.json()
    assert "mode" in payload
    assert "provider_name" in payload
    assert "provider_reachable" in payload


def test_create_planning_task() -> None:
    response = client.post(
        "/api/tasks",
        data={
            "prompt": "Plan a small MVP launch for an AI analytics tool.",
            "task_type": "planning",
            "context_text": "The team is two engineers and one designer.",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "queued"
    assert payload["task_type"] == "planning"
