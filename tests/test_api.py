"""
Test cases for Ansible API endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

client = TestClient(app)

class TestAnsibleEndpoints:
    """Test cases for Ansible job endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_trigger_restart_success(self):
        """Test successful restart job submission"""
        payload = {
            "environment": "DEV",
            "server_name": "weblogic-01",
            "reason": "Stuck thread detected",
            "escalation_level": 2
        }

        response = client.post("/api/ansible/jobs/restart", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert data["environment"] == "DEV"
        assert "job_id" in data
        assert "llm_analysis" in data

    def test_trigger_restart_invalid_environment(self):
        """Test restart with invalid environment"""
        payload = {
            "environment": "INVALID",
            "reason": "Test"
        }

        response = client.post("/api/ansible/jobs/restart", json=payload)
        assert response.status_code == 422  # Validation error

    def test_trigger_restart_missing_environment(self):
        """Test restart with missing environment"""
        payload = {
            "reason": "Test"
        }

        response = client.post("/api/ansible/jobs/restart", json=payload)
        assert response.status_code == 422  # Validation error

    def test_get_job_status(self):
        """Test getting job status"""
        # First create a job
        payload = {
            "environment": "TEST",
            "reason": "Test job"
        }

        create_response = client.post("/api/ansible/jobs/restart", json=payload)
        job_id = create_response.json()["job_id"]

        # Get status
        response = client.get(f"/api/ansible/jobs/{job_id}/status")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == job_id
        assert data["environment"] == "TEST"

    def test_get_nonexistent_job(self):
        """Test getting status of non-existent job"""
        response = client.get("/api/ansible/jobs/NONEXISTENT/status")
        assert response.status_code == 404

    def test_list_jobs(self):
        """Test listing all jobs"""
        response = client.get("/api/ansible/jobs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_jobs_by_environment(self):
        """Test listing jobs filtered by environment"""
        # Create some jobs
        for env in ["DEV", "TEST", "PREPROD"]:
            payload = {"environment": env, "reason": f"Test for {env}"}
            client.post("/api/ansible/jobs/restart", json=payload)

        # Filter by environment
        response = client.get("/api/ansible/jobs?environment=DEV")
        assert response.status_code == 200
        jobs = response.json()
        assert all(job["environment"] == "DEV" for job in jobs)

    def test_cancel_job(self):
        """Test cancelling a job"""
        # Create a job
        payload = {"environment": "DEV", "reason": "Test"}
        create_response = client.post("/api/ansible/jobs/restart", json=payload)
        job_id = create_response.json()["job_id"]

        # Cancel job
        response = client.post(f"/api/ansible/jobs/{job_id}/cancel")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelled"

    def test_cancel_nonexistent_job(self):
        """Test cancelling non-existent job"""
        response = client.post("/api/ansible/jobs/NONEXISTENT/cancel")
        assert response.status_code == 404

    def test_get_job_logs(self):
        """Test getting job logs"""
        # Create a job
        payload = {"environment": "DEV", "reason": "Test"}
        create_response = client.post("/api/ansible/jobs/restart", json=payload)
        job_id = create_response.json()["job_id"]

        # Get logs
        response = client.get(f"/api/ansible/jobs/{job_id}/logs")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert "logs" in data

    def test_launch_template(self):
        """Test launching job from template"""
        response = client.post("/api/ansible/template/6782/launch", 
                              params={"environment": "DEV"})
        assert response.status_code == 200
        data = response.json()
        assert data["template_id"] == 6782
        assert "job_id" in data

    def test_launch_invalid_template(self):
        """Test launching invalid template"""
        response = client.post("/api/ansible/template/9999/launch", 
                              params={"environment": "DEV"})
        assert response.status_code == 404

    def test_remediation_plan(self):
        """Test getting remediation plan"""
        # Create a job
        payload = {"environment": "DEV", "reason": "Test"}
        create_response = client.post("/api/ansible/jobs/restart", json=payload)
        job_id = create_response.json()["job_id"]

        # Get remediation plan
        response = client.post(f"/api/ansible/jobs/{job_id}/remediation-plan")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        assert "plan" in data
        assert "steps" in data["plan"]

    def test_get_supported_environments(self):
        """Test getting supported environments"""
        response = client.get("/api/environments")
        assert response.status_code == 200
        data = response.json()
        assert "supported_environments" in data
        assert "DEV" in data["supported_environments"]
        assert "TEST" in data["supported_environments"]
        assert "PREPROD" in data["supported_environments"]
        assert "PROD" in data["supported_environments"]

    def test_all_environments(self):
        """Test submitting jobs for all environments"""
        environments = ["DEV", "TEST", "PREPROD", "PROD"]

        for env in environments:
            payload = {
                "environment": env,
                "reason": f"Test for {env}"
            }
            response = client.post("/api/ansible/jobs/restart", json=payload)
            assert response.status_code == 200
            assert response.json()["environment"] == env

    def test_escalation_levels(self):
        """Test different escalation levels"""
        for level in range(1, 6):
            payload = {
                "environment": "DEV",
                "escalation_level": level,
                "reason": f"Test level {level}"
            }
            response = client.post("/api/ansible/jobs/restart", json=payload)
            assert response.status_code == 200
            data = response.json()
            assert "llm_analysis" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
