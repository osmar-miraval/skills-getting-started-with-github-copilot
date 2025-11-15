def test_unregister_from_activity_success():
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    # Asegurarse de que el participante esté registrado
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]

def test_unregister_from_activity_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Asegurarse de que el participante NO esté registrado
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"

def test_unregister_from_activity_not_found():
    response = client.post("/activities/UnknownActivity/unregister?email=test@mergington.edu")
    assert response.status_code == 404
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Estado original de participantes para cada actividad
ORIGINAL_PARTICIPANTS = {
    k: v["participants"][:]
    for k, v in activities.items()
}

def setup_function(function):
    # Restaurar los participantes originales antes de cada test
    for k, v in ORIGINAL_PARTICIPANTS.items():
        activities[k]["participants"] = v[:]

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_for_activity_duplicate():
    email = "daniel@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_for_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=test@mergington.edu")
    assert response.status_code == 404