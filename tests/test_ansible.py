"""
Test cases for Ansible Mock Service
"""

import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'services'))

from ansible_mock import (
    create_mock_job,
    get_job_status,
    cancel_job,
    list_jobs,
    get_job_logs,
    JobStatus
)

class TestAnsibleMockService:
    """Test cases for Ansible mock service"""

    def test_create_mock_job(self):
        """Test creating a mock job"""
        job = create_mock_job(
            environment="DEV",
            server_name="weblogic-01",
            reason="Test stuck thread"
        )

        assert job is not None
        assert job["environment"] == "DEV"
        assert job["server"] == "weblogic-01"
        assert job["reason"] == "Test stuck thread"
        assert job["status"] == JobStatus.PENDING.value
        assert "id" in job
        assert "created_at" in job

    def test_create_job_without_server_name(self):
        """Test creating job without server name"""
        job = create_mock_job(environment="TEST")

        assert job["server"].startswith("weblogic-")
        assert job["environment"] == "TEST"

    def test_get_job_status(self):
        """Test getting job status"""
        created_job = create_mock_job(environment="DEV")
        job_id = created_job["id"]

        job = get_job_status(job_id)

        assert job is not None
        assert job["id"] == job_id
        assert job["environment"] == "DEV"

    def test_get_nonexistent_job(self):
        """Test getting status of non-existent job"""
        job = get_job_status("NONEXISTENT")
        assert job is None

    def test_cancel_job(self):
        """Test cancelling a job"""
        created_job = create_mock_job(environment="DEV")
        job_id = created_job["id"]

        result = cancel_job(job_id)
        assert result is True

        job = get_job_status(job_id)
        assert job["status"] == JobStatus.CANCELLED.value

    def test_cancel_nonexistent_job(self):
        """Test cancelling non-existent job"""
        result = cancel_job("NONEXISTENT")
        assert result is False

    def test_list_jobs(self):
        """Test listing all jobs"""
        # Create a few jobs
        for i in range(3):
            create_mock_job(environment="DEV", reason=f"Test {i}")

        jobs = list_jobs()
        assert len(jobs) >= 3

    def test_list_jobs_by_environment(self):
        """Test listing jobs by environment"""
        # Create jobs in different environments
        create_mock_job(environment="DEV")
        create_mock_job(environment="TEST")

        dev_jobs = list_jobs(environment="DEV")
        assert all(job["environment"] == "DEV" for job in dev_jobs)

    def test_get_job_logs(self):
        """Test getting job logs"""
        created_job = create_mock_job(environment="DEV")
        job_id = created_job["id"]

        logs = get_job_logs(job_id)

        assert logs is not None
        assert job_id in logs
        assert "Ansible Job Log" in logs

    def test_get_logs_nonexistent_job(self):
        """Test getting logs for non-existent job"""
        logs = get_job_logs("NONEXISTENT")
        assert logs is None

    def test_job_progression(self):
        """Test job status progression over time"""
        import time

        job = create_mock_job(environment="DEV")
        job_id = job["id"]

        # Job should start as PENDING
        assert job["status"] == JobStatus.PENDING.value

        # After simulation, job should progress
        time.sleep(1)
        job = get_job_status(job_id)
        
        # Status should be pending or running or completed
        assert job["status"] in [
            JobStatus.PENDING.value,
            JobStatus.RUNNING.value,
            JobStatus.SUCCESS.value,
            JobStatus.FAILED.value
        ]

    def test_extra_vars_in_job(self):
        """Test that extra variables are properly set"""
        job = create_mock_job(
            environment="PREPROD",
            reason="Critical stuck thread"
        )

        assert "extra_vars" in job
        assert job["extra_vars"]["environment"] == "PREPROD"
        assert job["extra_vars"]["restart_reason"] == "Critical stuck thread"
        assert job["extra_vars"]["auto_remediation"] is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
