import sys
from pathlib import Path

# Ensure src can be imported when tests run from repository root
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_activities():
    """Test that GET /activities returns available activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_post_signup_success():
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Drama Club/signup",
        params={"email": "testuser@example.com"}
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_post_signup_duplicate_rejection():
    """Test that duplicate signup returns 400"""
    email = "duplicate@example.com"
    first = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert first.status_code == 200

    second = client.post(
        "/activities/Chess Club/signup",
        params={"email": email}
    )
    assert second.status_code == 400
    assert "already signed up" in second.json()["detail"]


def test_delete_participant_success():
    """Test successful removal of an existing participant"""
    email = "remove-me@example.com"

    client.post(
        "/activities/Swimming Club/signup",
        params={"email": email}
    )

    response = client.delete(f"/activities/Swimming Club/participants/{email}")
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]


def test_delete_participant_not_found():
    """Test deleting a non-existent participant returns 404"""
    response = client.delete(
        "/activities/Art Studio/participants/nonexistent@example.com"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
