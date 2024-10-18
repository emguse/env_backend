# test_app.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from app.main import app  # Adjust the import path based on your project structure
from app.models.sensor_models import ReceiveEnv, RecieveLog
from app.cruds.cruds import bulk_insert_env_data

client = TestClient(app)


def test_root():
    """Test the root endpoint GET '/'."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello. World!"}


def test_hello():
    """Test the '/hello' endpoint GET '/hello'."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello. World!"}


def test_post_env4():
    """Test the '/post-env4' endpoint POST '/post-env4'."""
    env_data = {
        "timestamp": [2023, 10, 1, 12, 0, 0],
        "sensor_id": "sensor123",
        "temperature": 25.5,
        "humidity": 60.0,
        "pressure": 1013.25,
    }

    expected_response = {
        "env_data": {
            "timestamp": "2023-10-01T12:00:00",
            "sensor_id": "sensor123",
            "temperature": 25.5,
            "humidity": 60.0,
            "pressure": 1013.25,
        }
    }

    with patch("app.routers.endpoints.bulk_insert_env_data") as mock_bulk_insert:
        response = client.post("/post-env4", json=env_data)
        assert response.status_code == 200
        # Verify that the response contains the same data sent, with timestamp formatted
        assert response.json() == expected_response
        # Ensure that the bulk_insert_env_data function was called
        assert mock_bulk_insert.called


def test_post_log_info():
    """Test the '/post-log' endpoint with level 'info'."""
    log_data = {"level": "info", "message": "Test log message"}

    with patch("app.routers.endpoints.logger.info") as mock_info:
        response = client.post("/post-log", json=log_data)
        assert response.status_code == 200
        # Verify that logger.info was called correctly
        mock_info.assert_called_with("Test log message")


def test_post_log_error():
    """Test the '/post-log' endpoint with level 'error'."""
    log_data = {"level": "error", "message": "Test error message"}

    # logger.errorをモック
    with patch("app.routers.endpoints.logger.error") as mock_error:
        response = client.post("/post-log", json=log_data)
        assert response.status_code == 200
        # Verify that logger.error was called correctly
        mock_error.assert_called_with("Test error message")


def test_post_test():
    """Test the '/post-test' endpoint POST '/post-test'."""
    test_body = {"key": "value"}
    response = client.post("/post-test", json=test_body)
    assert response.status_code == 200
    # Verify that the response contains the body sent
    assert response.json() == {"body": test_body}
