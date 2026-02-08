import pytest
import requests
import time

BASE_URL = "http://localhost:8080"
endpoint = "api/records"

record = {
    "title": "Test Album",
    "artist": "Test Artist",
    "year": 2024,
    "genre": "Rock",
    "condition": "Very Good"
}

@pytest.fixture(scope="session")
def base_url():
    """Fixture to provide base URL"""
    # Give server a moment to start
    time.sleep(1)
    return BASE_URL

@pytest.fixture(scope="session")
def records_endpoint(base_url):
    return f"{base_url}/{endpoint}"

@pytest.fixture
def created_record_location(records_endpoint):
    """Fixture to create a test record and clean it up after test"""
    response = requests.post(records_endpoint, json=record)
    
    assert response.status_code == 201
    location = response.headers.get("Location")
    
    yield location  # Provide record location to test

    # Teardown: Delete the record (if it still exists)
    try:
        if location:
            requests.delete(f"{BASE_URL}{location}")
    except:
        pass


class TestRecordsAPI:
    def test_create_record(self, records_endpoint, base_url):
        """Test POST - Create new record"""
        response = requests.post(records_endpoint, json=record)

        assert response.status_code == 201
        assert "Location" in response.headers
        
        location = response.headers["Location"]
        assert "records" in location

        # Cleanup
        requests.delete(f"{base_url}{location}")

    def test_get_all_records(self, records_endpoint, created_record_location):
        """Test GET all records"""
        response = requests.get(records_endpoint)
        response_data = response.json()

        assert response.status_code == 200
        assert isinstance(response_data, list)
        assert any(
            i["title"] == record["title"] and i["artist"] == record["artist"]
            for i in response_data
        )

    def test_get_specific_record(self, base_url, created_record_location):
        """Test GET specific record"""
        response = requests.get(f"{base_url}{created_record_location}")

        assert response.status_code == 200
        assert "title" in response.json()
        assert "artist" in response.json()

    def test_update_record(self, base_url, created_record_location):
        """Test PUT - Update record"""
        new_title = "Updated Album Title"
        new_condition = "Excellent"

        updated_data = {"title": new_title, "condition": new_condition}

        response = requests.put(f"{base_url}{created_record_location}", json=updated_data)

        assert response.status_code == 200

        get_response = requests.get(f"{base_url}{created_record_location}")
        updated_data = get_response.json()
        assert updated_data["title"] == new_title
        assert updated_data["condition"] == new_condition

    def test_delete_record(self, base_url, created_record_location):
        """Test DELETE record"""
        response = requests.delete(f"{base_url}{created_record_location}")

        assert response.status_code == 200

        # Verify record is deleted
        get_response = requests.get(f"{base_url}{created_record_location}")
        assert get_response.status_code == 404

    def test_create_record_missing_fields(self, records_endpoint):
        """Test POST with missing required fields"""
        incomplete_record = {"title": "Only Title"}
        response = requests.post(records_endpoint, json=incomplete_record)

        assert response.status_code == 400
        assert "required" in response.json()["error"].lower()
