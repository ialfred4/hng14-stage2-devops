import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Patch redis.Redis before importing main
with patch("redis.Redis") as mock_redis_class:
    mock_redis_instance = MagicMock()
    mock_redis_class.return_value = mock_redis_instance
    from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mock():
    mock_redis_instance.reset_mock()
    yield


class TestCreateJob:
    def test_create_job_returns_job_id(self):
        """POST /jobs should return a valid job_id"""
        mock_redis_instance.lpush.return_value = 1
        mock_redis_instance.hset.return_value = 1

        response = client.post("/jobs")

        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data

    def test_create_job_pushes_to_queue(self):
        """POST /jobs should push job_id into Redis queue"""
        mock_redis_instance.lpush.return_value = 1
        mock_redis_instance.hset.return_value = 1

        response = client.post("/jobs")
        job_id = response.json()["job_id"]

        mock_redis_instance.lpush.assert_called_once_with("job_queue", job_id)

    def test_create_job_sets_queued_status(self):
        """POST /jobs should set job status to queued"""
        mock_redis_instance.lpush.return_value = 1
        mock_redis_instance.hset.return_value = 1

        response = client.post("/jobs")
        job_id = response.json()["job_id"]

        mock_redis_instance.hset.assert_called_once_with(
            f"job:{job_id}", "status", "queued"
        )


class TestGetJob:
    def test_get_existing_job(self):
        """GET /jobs/{id} should return status for known job"""
        mock_redis_instance.hget.return_value = b"queued"

        response = client.get("/jobs/test-job-123")

        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == "test-job-123"
        assert data["status"] == "queued"

    def test_get_completed_job(self):
        """GET /jobs/{id} should return completed status"""
        mock_redis_instance.hget.return_value = b"completed"

        response = client.get("/jobs/finished-job")

        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_get_nonexistent_job_returns_404(self):
        """GET /jobs/{id} should return 404 for unknown jobs"""
        mock_redis_instance.hget.return_value = None

        response = client.get("/jobs/does-not-exist")

        assert response.status_code == 404


class TestHealthz:
    def test_healthz_returns_ok(self):
        """GET /healthz should return 200 with status ok"""
        mock_redis_instance.ping.return_value = True

        response = client.get("/healthz")

        assert response.status_code == 200
        assert response.json()["status"] == "ok"
