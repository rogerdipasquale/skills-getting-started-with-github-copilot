from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_succeeds():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    # Cleanup
    cleanup_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert cleanup_response.status_code == 200


def test_signup_duplicate_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup?email={email}"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_activity_not_found_returns_404():
    # Arrange
    endpoint = "/activities/Nonexistent%20Activity/signup?email=testuser@mergington.edu"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_succeeds():
    # Arrange
    activity_name = "Programming Class"
    email = "tempuser@mergington.edu"
    signup_endpoint = f"/activities/{activity_name}/signup?email={email}"
    remove_endpoint = f"/activities/{activity_name}/participants?email={email}"

    signup_response = client.post(signup_endpoint)
    assert signup_response.status_code == 200

    # Act
    response = client.delete(remove_endpoint)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_remove_participant_not_found_returns_404():
    # Arrange
    activity_name = "Programming Class"
    email = "missing@mergington.edu"
    endpoint = f"/activities/{activity_name}/participants?email={email}"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
