"""
Health Check Routes
System health and status endpoints
"""

from fastapi import APIRouter
from datetime import datetime

from models import HealthStatus

router = APIRouter()

@router.get("/health", response_model=HealthStatus)
async def health_check():
    """
    Health check endpoint
    Returns application status and service information
    """
    
    return HealthStatus(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow(),
        services={
            "api": "operational",
            "llm": "ready",
            "ansible_mock": "ready",
            "database": "ready"
        }
    )

@router.get("/version")
async def get_version():
    """Get application version"""
    return {
        "application": "Auto Remediation Stuck Thread",
        "version": "1.0.0",
        "status": "operational"
    }

@router.get("/environments")
async def get_supported_environments():
    """Get list of supported environments"""
    return {
        "supported_environments": ["DEV", "TEST", "PREPROD", "PROD"],
        "description": "WebLogic server environments for remediation"
    }
