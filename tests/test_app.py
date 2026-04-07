import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_random_dog_returns_dog_data(client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "abc123", "url": "https://example.com/dog.jpg"}]

    with patch("app.requests.get", return_value=mock_response), \
         patch("app.get_conn") as mock_conn:

        mock_cursor = MagicMock()
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        response = client.get("/random-dog")
        assert response.status_code == 200
        data = response.get_json()
        assert "url" in data


def test_random_dog_returns_error_when_api_fails(client):
    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("app.requests.get", return_value=mock_response):
        response = client.get("/random-dog")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_stats_returns_count(client):
    with patch("app.get_conn") as mock_conn:
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [42]
        mock_conn.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        response = client.get("/stats")
        assert response.status_code == 200
        data = response.get_json()
        assert "total_dog_requests" in data


def test_stats_returns_error_when_db_fails(client):
    with patch("app.get_conn", side_effect=Exception("DB connection failed")):
        response = client.get("/stats")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


def test_status_returns_expected_fields(client):
    mock_db_response = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["2026-01-01 00:00:00"]
    mock_db_response.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    mock_api_response = MagicMock()
    mock_api_response.status_code = 200

    with patch("app.get_conn", return_value=mock_db_response), \
         patch("app.requests.get", return_value=mock_api_response):

        response = client.get("/status")
        assert response.status_code == 200
        data = response.get_json()
        assert "service" in data
        assert "uptime_seconds" in data
        assert "database" in data
        assert "dog_api" in data


def test_status_db_unavailable(client):
    mock_api_response = MagicMock()
    mock_api_response.status_code = 200

    with patch("app.get_conn", side_effect=Exception("DB down")), \
         patch("app.requests.get", return_value=mock_api_response):

        response = client.get("/status")
        assert response.status_code == 200
        data = response.get_json()
        assert data["database"] == "database unavailable"


def test_status_api_unavailable(client):
    mock_db_response = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["2026-01-01 00:00:00"]
    mock_db_response.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    with patch("app.get_conn", return_value=mock_db_response), \
         patch("app.requests.get", side_effect=Exception("API down")):

        response = client.get("/status")
        assert response.status_code == 200
        data = response.get_json()
        assert data["dog_api"] == "unavailable"


def test_stats_page_returns_200(client):
    response = client.get("/stats-page")
    assert response.status_code == 200