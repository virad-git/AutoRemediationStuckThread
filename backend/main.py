"""
Auto Remediation Stuck Thread - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from config import Settings
from routes import ansible_routes, health_routes
from services.llm_service import initialize_llm

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Auto Remediation Stuck Thread API",
    description="API for automating WebLogic stuck thread remediation",
    version="1.0.0"
)

# Initialize settings
settings = Settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM service
@app.on_event("startup")
async def startup_event():
    """Initialize LLM service on application startup"""
    try:
        initialize_llm()
        print("✓ LLM service initialized successfully")
    except Exception as e:
        print(f"⚠ Warning: LLM service initialization failed: {e}")

# Include routes
app.include_router(ansible_routes.router, prefix="/api/ansible", tags=["Ansible"])
app.include_router(health_routes.router, prefix="/api", tags=["Health"])

# Mount frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auto Remediation Stuck Thread API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
