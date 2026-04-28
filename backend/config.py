"""
Configuration settings for the application
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # FastAPI settings
    APP_NAME: str = "Auto Remediation Stuck Thread"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # GEMINI API settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Ansible settings
    ANSIBLE_TOWER_URL: str = os.getenv("ANSIBLE_TOWER_URL", "https://tower.ikea.com")
    ANSIBLE_JOB_TEMPLATE_ID: int = int(os.getenv("ANSIBLE_JOB_TEMPLATE_ID", 6782))
    ANSIBLE_TOKEN: str = os.getenv("ANSIBLE_TOKEN", "mock-token")
    
    # Environments
    SUPPORTED_ENVIRONMENTS: list = ["DEV", "TEST", "PREPROD", "PROD"]
    
    # LangChain settings
    LANGCHAIN_DEBUG: bool = os.getenv("LANGCHAIN_DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
