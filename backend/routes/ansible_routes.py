"""
Ansible API Routes
Mock endpoints for Ansible Tower job integration
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, List
import logging

from models import RestartRequest, RestartResponse, JobStatus, AnsibleJobStatus
from services import ansible_mock, llm_service

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/jobs/restart", response_model=RestartResponse)
async def trigger_restart(request: RestartRequest, background_tasks: BackgroundTasks):
    """
    Trigger a WebLogic server restart
    
    This endpoint simulates submitting a job to Ansible Tower
    for restarting a WebLogic server.
    """
    
    try:
        # Validate environment
        if request.environment.value not in ["DEV", "TEST", "PREPROD", "PROD"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid environment: {request.environment}"
            )
        
        # Get LLM analysis
        analysis = await llm_service.analyze_stuck_thread(
            environment=request.environment.value,
            server_name=request.server_name,
            escalation_level=request.escalation_level or 1
        )
        
        # Create mock Ansible job
        job = ansible_mock.create_mock_job(
            environment=request.environment.value,
            server_name=request.server_name,
            reason=request.reason
        )
        
        # Add background task to update job status
        background_tasks.add_task(ansible_mock.get_job_status, job["id"])
        
        return RestartResponse(
            job_id=job["id"],
            status=job["status"],
            environment=job["environment"],
            message=f"Restart job submitted successfully for {request.environment.value} environment",
            llm_analysis=analysis
        )
    
    except Exception as e:
        logger.error(f"Error triggering restart: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}/status")
async def get_job_status(job_id: str):
    """Get the status of a specific job"""
    
    job = ansible_mock.get_job_status(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return job

@router.get("/jobs/{job_id}/logs")
async def get_job_logs(job_id: str):
    """Get logs for a specific job"""
    
    logs = ansible_mock.get_job_logs(job_id)
    
    if not logs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    return {"job_id": job_id, "logs": logs}

@router.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a running job"""
    
    if not ansible_mock.cancel_job(job_id):
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found or cannot be cancelled")
    
    return {"job_id": job_id, "status": "cancelled", "message": "Job cancelled successfully"}

@router.get("/jobs", response_model=List[dict])
async def list_jobs(environment: Optional[str] = None):
    """List all jobs, optionally filtered by environment"""
    
    try:
        jobs = ansible_mock.list_jobs(environment=environment)
        return jobs
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/jobs/{job_id}/remediation-plan")
async def get_remediation_plan(job_id: str):
    """Get remediation plan for a job"""
    
    job = ansible_mock.get_job_status(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
    # Generate remediation plan
    plan = await llm_service.generate_remediation_plan(
        analysis="Stuck thread detected during normal operations",
        environment=job["environment"]
    )
    
    return {"job_id": job_id, "plan": plan}

@router.post("/template/{template_id}/launch")
async def launch_template(template_id: int, environment: str = None):
    """
    Launch a job from Ansible Tower template
    Mock endpoint for launching predefined templates
    """
    
    if template_id != 6782:
        raise HTTPException(
            status_code=404,
            detail=f"Template {template_id} not found"
        )
    
    if not environment:
        raise HTTPException(
            status_code=400,
            detail="Environment parameter required"
        )
    
    job = ansible_mock.create_mock_job(
        environment=environment,
        reason="Direct template launch"
    )
    
    return {
        "template_id": template_id,
        "job_id": job["id"],
        "status": job["status"],
        "message": "Job launched successfully"
    }
