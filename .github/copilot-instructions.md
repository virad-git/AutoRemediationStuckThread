# Auto Remediation Stuck Thread - Project Setup

## Completion Checklist

- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## Project Summary

**Auto Remediation Stuck Thread** is a full-stack web application that automates the remediation of stuck threads on WebLogic servers.

### Technology Stack
- **Backend:** FastAPI, Python 3.x, LangChain, GEMINI 2.0
- **Frontend:** HTML5, CSS3, jQuery, JavaScript
- **Testing:** pytest, FastAPI TestClient
- **Infrastructure:** Mock Ansible Tower integration

### Project Structure
```
AutoRemediationStuckThread/
├── backend/              # FastAPI REST API
├── frontend/             # Web UI (HTML/CSS/JS)
├── tests/                # Test suite
├── .env.example          # Environment variables
└── README.md             # Documentation
```

## Quick Start Guide

### 1. Setup Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 2. Access Application

```
Frontend: http://localhost:8000
API Docs: http://localhost:8000/docs
```

### 3. Run Tests

```bash
cd tests
pytest -v
```

## Key Features

✅ REST API for WebLogic restart jobs  
✅ LLM-powered analysis (GEMINI + LangChain)  
✅ Real-time job monitoring  
✅ Multi-environment support (DEV/TEST/PREPROD/PROD)  
✅ Modern responsive UI  
✅ Comprehensive test coverage  
✅ Mock Ansible Tower integration  

## API Endpoints

- `POST /api/ansible/jobs/restart` - Submit restart job
- `GET /api/ansible/jobs` - List jobs
- `GET /api/ansible/jobs/{job_id}/status` - Job status
- `GET /api/health` - Health check
- `GET /docs` - Interactive API documentation

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `GEMINI_API_KEY` - Google GEMINI API key (optional)
- `HOST` - Server host (default: 127.0.0.1)
- `PORT` - Server port (default: 8000)

## Testing

```bash
# Run all tests
pytest -v

# Run specific test file
pytest test_api.py -v

# Run with coverage
pytest --cov=backend
```

## Important Notes

1. **Mock Ansible Service**: Current implementation uses mock Ansible responses. For production, integrate with actual Ansible Tower API.

2. **LLM Optional**: GEMINI integration is optional. Without API key, system uses mock responses.

3. **In-Memory Storage**: Job data stored in memory. For production, implement persistent database.

4. **CORS Enabled**: Current setup allows all origins. Configure for security in production.

## Troubleshooting

- **Port in use**: Change PORT in .env or use `--port 8001`
- **Import errors**: Ensure all dependencies installed: `pip install -r requirements.txt`
- **API not responding**: Verify backend is running on http://localhost:8000

## Next Steps

1. Start the backend server
2. Open browser to http://localhost:8000
3. Try submitting a test job
4. Check API documentation at /docs
5. Run test suite to verify installation

For detailed information, see [README.md](../README.md)
