"""
Ansible Job Mock Service
Simulates Ansible Tower job API responses
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)

# In-memory job storage (in production, use database)
_jobs_db: Dict = {}

class JobStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ERROR = "error"
    CANCELLED = "cancelled"

def create_mock_job(
    environment: str,
    server_name: Optional[str] = None,
    reason: Optional[str] = None
) -> dict:
    """
    Create a mock Ansible job
    
    Args:
        environment: Target environment
        server_name: Optional server name
        reason: Reason for restart
    
    Returns:
        Job details dictionary
    """
    
    job_id = f"JOB-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8]}"
    
    job = {
        "id": job_id,
        "template_id": 6782,
        "template_name": "Restart WebLogic Server",
        "status": JobStatus.PENDING.value,
        "environment": environment,
        "server": server_name or f"weblogic-{environment.lower()}",
        "reason": reason or "Auto-remediation of stuck thread",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "completed_at": None,
        "extra_vars": {
            "environment": environment,
            "restart_reason": reason,
            "auto_remediation": True
        },
        "output": None,
        "error": None,
        "duration": 0
    }
    
    _jobs_db[job_id] = job
    logger.info(f"Created mock job {job_id} for environment {environment}")
    
    return job

def get_job_status(job_id: str) -> Optional[dict]:
    """Get job status from mock database"""
    
    if job_id not in _jobs_db:
        return None
    
    job = _jobs_db[job_id]
    
    # Simulate job progression (for demo purposes)
    created_at = datetime.fromisoformat(job["created_at"])
    elapsed = (datetime.utcnow() - created_at).total_seconds()
    
    if job["status"] == JobStatus.PENDING.value:
        if elapsed > 2:
            job["status"] = JobStatus.RUNNING.value
            job["started_at"] = (created_at + timedelta(seconds=2)).isoformat()
            job["updated_at"] = datetime.utcnow().isoformat()
    
    if job["status"] == JobStatus.RUNNING.value:
        if elapsed > 15:
            # Simulate successful completion (90% success rate)
            import random
            success = random.random() > 0.1
            
            job["status"] = JobStatus.SUCCESS.value if success else JobStatus.FAILED.value
            job["completed_at"] = (created_at + timedelta(seconds=15)).isoformat()
            job["updated_at"] = datetime.utcnow().isoformat()
            job["duration"] = 15
            
            if success:
                job["output"] = f"Successfully restarted WebLogic server in {job['environment']} environment"
            else:
                job["error"] = "Server restart failed - unable to establish connection"
    
    return job

def cancel_job(job_id: str) -> bool:
    """Cancel a running job"""
    
    if job_id not in _jobs_db:
        return False
    
    job = _jobs_db[job_id]
    if job["status"] in [JobStatus.RUNNING.value, JobStatus.PENDING.value]:
        job["status"] = JobStatus.CANCELLED.value
        job["updated_at"] = datetime.utcnow().isoformat()
        logger.info(f"Cancelled job {job_id}")
        return True
    
    return False

def list_jobs(environment: Optional[str] = None) -> list:
    """List all jobs, optionally filtered by environment"""
    
    jobs = list(_jobs_db.values())
    
    if environment:
        jobs = [job for job in jobs if job["environment"] == environment]
    
    return jobs

def get_job_logs(job_id: str) -> Optional[str]:
    """Get job logs"""
    
    job = get_job_status(job_id)
    if not job:
        return None
    
    logs = f"""
    ========== Ansible Job Log ==========
    Job ID: {job['id']}
    Template: {job['template_name']}
    Environment: {job['environment']}
    Server: {job['server']}
    Status: {job['status']}
    
    --- Execution Timeline ---
    Created: {job['created_at']}
    Started: {job['started_at'] or 'Not started'}
    Completed: {job['completed_at'] or 'In progress'}
    Duration: {job['duration']}s
    
    --- Output ---
    {job['output'] or 'No output yet'}
    
    --- Errors ---
    {job['error'] or 'No errors'}
    
    --- Extra Variables ---
    {json.dumps(job['extra_vars'], indent=2)}
    ======================================
    """
    
    return logs.strip()
