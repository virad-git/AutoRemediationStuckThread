"""
Data models for the application
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EnvironmentType(str, Enum):
    """Supported environments"""
    DEV = "DEV"
    TEST = "TEST"
    PREPROD = "PREPROD"
    PROD = "PROD"

class RestartRequest(BaseModel):
    """Model for WebLogic server restart request"""
    environment: EnvironmentType = Field(..., description="Target environment")
    server_name: Optional[str] = Field(None, description="Specific server name (optional)")
    reason: Optional[str] = Field(None, description="Reason for restart")
    escalation_level: Optional[int] = Field(1, ge=1, le=5, description="Escalation level for LLM analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "environment": "DEV",
                "server_name": "weblogic-01",
                "reason": "Stuck thread detected",
                "escalation_level": 2
            }
        }

class RestartResponse(BaseModel):
    """Model for restart operation response"""
    job_id: str = Field(..., description="Unique job ID")
    status: str = Field(..., description="Job status")
    environment: str = Field(..., description="Target environment")
    message: str = Field(..., description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    llm_analysis: Optional[str] = Field(None, description="LLM analysis of the situation")

    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "JOB-2024-001",
                "status": "pending",
                "environment": "DEV",
                "message": "Restart job submitted successfully",
                "timestamp": "2024-01-15T10:30:00",
                "llm_analysis": "Stuck threads detected. Escalation recommended."
            }
        }

class JobStatus(BaseModel):
    """Model for job status"""
    job_id: str
    status: str
    environment: str
    created_at: datetime
    updated_at: datetime
    output: Optional[str] = None
    error: Optional[str] = None

class HealthStatus(BaseModel):
    """Model for health check response"""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: dict = {}

class AnsibleJobStatus(str, Enum):
    """Ansible job statuses"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ERROR = "error"
    CANCELLED = "cancelled"
