"""
LLM Service using LangChain and GEMINI
Handles AI-powered analysis of stuck threads
"""

import os
from typing import Optional
from config import Settings
import logging

logger = logging.getLogger(__name__)

# Global LLM instance
_llm_instance = None

def initialize_llm():
    """Initialize the LLM instance"""
    global _llm_instance
    
    try:
        settings = Settings()
        
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set. LLM functionality will be limited.")
            return
        
        # Import LangChain components
        try:
            from langchain.llms import GoogleGenerativeAI
            from langchain.prompts import PromptTemplate
            from langchain.chains import LLMChain
            
            # Initialize GEMINI LLM
            _llm_instance = GoogleGenerativeAI(
                model_name=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.3,
                max_output_tokens=500
            )
            logger.info(f"✓ LLM initialized with {settings.GEMINI_MODEL}")
        except ImportError:
            logger.warning("LangChain not fully configured. Using mock LLM.")
            _llm_instance = "mock"
            
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        _llm_instance = "mock"

def get_llm():
    """Get the LLM instance"""
    return _llm_instance

async def analyze_stuck_thread(
    environment: str,
    server_name: Optional[str] = None,
    escalation_level: int = 1
) -> str:
    """
    Analyze stuck thread situation using GEMINI/LangChain
    
    Args:
        environment: Target environment (DEV, TEST, PREPROD, PROD)
        server_name: Optional server name
        escalation_level: Escalation level (1-5)
    
    Returns:
        LLM analysis response
    """
    
    try:
        settings = Settings()
        
        # Create analysis prompt
        prompt_template = """
        You are a WebLogic administrator analyzing a stuck thread issue.
        
        Environment: {environment}
        Server: {server}
        Escalation Level: {level}/5
        
        Provide a brief analysis of:
        1. Likely causes of stuck threads in {environment}
        2. Recommended immediate action
        3. Any additional checks needed
        
        Keep response concise (2-3 sentences per point).
        """
        
        # Use LangChain if available
        llm = get_llm()
        
        if llm and llm != "mock":
            try:
                from langchain.prompts import PromptTemplate
                
                prompt = PromptTemplate(
                    input_variables=["environment", "server", "level"],
                    template=prompt_template
                )
                
                analysis = llm.predict(
                    environment=environment,
                    server=server_name or "Unknown",
                    level=escalation_level
                )
                return analysis
            except Exception as e:
                logger.warning(f"LangChain analysis failed: {e}. Using mock response.")
        
        # Fallback mock response
        mock_responses = {
            1: "Low escalation: Monitor and document the issue. Perform standard restart procedure.",
            2: "Medium escalation: Review logs for thread deadlocks. Coordinate with development team.",
            3: "High escalation: Immediate action required. Escalate to senior administration team.",
            4: "Critical: Urgent escalation needed. Consider cluster failover if available.",
            5: "Emergency: Maximum escalation. Engage system architecture team immediately."
        }
        
        return mock_responses.get(escalation_level, mock_responses[1])
        
    except Exception as e:
        logger.error(f"Error in analyze_stuck_thread: {e}")
        return "Unable to perform analysis at this time."

async def generate_remediation_plan(
    analysis: str,
    environment: str
) -> dict:
    """
    Generate a remediation plan based on analysis
    
    Args:
        analysis: LLM analysis result
        environment: Target environment
    
    Returns:
        Remediation plan dictionary
    """
    
    plan = {
        "steps": [
            "Enable detailed logging for stuck thread detection",
            "Identify affected thread pools",
            "Gracefully drain connections",
            "Restart WebLogic server",
            "Monitor recovery and thread health",
            "Verify no thread leaks in new session"
        ],
        "rollback_plan": [
            "Monitor error logs during restart",
            "If restart fails, revert to previous known good state",
            "Restore from latest backup if necessary"
        ],
        "monitoring": [
            "Thread pool status",
            "Memory usage",
            "Request latency",
            "Error rate in logs"
        ],
        "environment": environment,
        "analysis": analysis
    }
    
    return plan
