import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_signup_and_unregister():
    activity = "Chess Club"
    test_email = "test@example.com"

    # Ensure test_email is not in participants
    if test_email in app.activities[activity]["participants"]:
        app.activities[activity]["participants"].remove(test_email)

    # Test signup
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Test duplicate signup
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    # Test unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Test unregister not signed up
    response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"

    # Test activity not found
    response = client.post("/activities/nonexistent/signup", params={"email": test_email})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
