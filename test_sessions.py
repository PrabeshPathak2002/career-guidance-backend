from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_start_session():
    response = client.post("/session")
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "question" in data

def test_get_next_question():
    session_resp = client.post("/session")
    data = session_resp.json()
    print("Session response:", data) 
    assert "session_id" in data, f"Unexpected response: {data}"
    if "session_id" not in data:
        return
    session_id = data["session_id"]
    resp = client.get(f"/question?session_id={session_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "question" in data or data.get("status") == "complete"

def test_reset_session():
    session_resp = client.post("/session")
    data = session_resp.json()
    print("Session response:", data) 
    assert "session_id" in data, f"Unexpected response: {data}"
    if "session_id" not in data:
        return
    session_id = data["session_id"]
    resp = client.post(f"/reset?session_id={session_id}")
    assert resp.status_code == 200
    assert resp.json()["status"] == "Session reset."