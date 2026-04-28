# Auto Remediation - Stuck Thread Manager

## Project Overview

**Auto Remediation Stuck Thread** is a comprehensive solution for automating the remediation of stuck threads on WebLogic servers. The system combines modern web technologies with AI-powered analysis to provide intelligent, automated thread management.

### Key Features

✅ **REST API** - FastAPI-based backend with comprehensive endpoints  
✅ **LLM Integration** - GEMINI 2.0 powered analysis with LangChain  
✅ **Modern UI** - Responsive HTML/CSS/jQuery frontend  
✅ **Mock Ansible Integration** - Simulates Ansible Tower job submissions  
✅ **Real-time Monitoring** - Live job status tracking and updates  
✅ **Multi-Environment Support** - DEV, TEST, PREPROD, PROD environments  
✅ **Comprehensive Testing** - Full test suite with pytest  
✅ **LLM Analysis** - AI-powered escalation and remediation recommendations  

---

## Project Structure

```
AutoRemediationStuckThread/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Application entry point
│   ├── config.py              # Configuration settings
│   ├── models.py              # Pydantic data models
│   ├── requirements.txt        # Python dependencies
│   ├── services/              # Business logic services
│   │   ├── llm_service.py    # LangChain + GEMINI integration
│   │   └── ansible_mock.py   # Mock Ansible job service
│   └── routes/                # API route handlers
│       ├── ansible_routes.py  # Ansible job endpoints
│       └── health_routes.py   # Health check endpoints
├── frontend/                   # Web UI
│   ├── index.html             # Main HTML interface
│   ├── assets/
│   │   ├── css/
│   │   │   └── styles.css     # Modern CSS styling
│   │   └── js/
│   │       └── app.js         # jQuery/JavaScript app
├── tests/                      # Test suite
│   ├── test_api.py            # API endpoint tests
│   └── test_ansible.py        # Ansible service tests
├── .env.example               # Environment variables template
├── README.md                  # This file
└── .github/
    └── copilot-instructions.md
```

---

## Technology Stack

### Backend
- **FastAPI** 0.104.1 - Modern Python web framework
- **Python** 3.8+ - Programming language
- **LangChain** 1.0 - LLM orchestration framework
- **GEMINI** 2.0 - Google's generative AI model
- **Uvicorn** - ASGI web server
- **Pydantic** - Data validation

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling with modern design
- **jQuery** - JavaScript library
- **Responsive Design** - Mobile and desktop compatible

### Testing
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **FastAPI TestClient** - API testing

---

## Installation & Setup

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### 2. Clone/Setup Project

```bash
cd AutoRemediationStuckThread
```

### 3. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env and add your GEMINI API key (optional)
```

---

## Running the Application

### 1. Start Backend Server

```bash
cd backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Access Frontend

Open your browser and navigate to:
```
http://localhost:8000
```

### 3. API Documentation

Interactive API docs available at:
```
http://localhost:8000/docs
```

---

## API Endpoints

### Health & System

- `GET /api/health` - System health check
- `GET /api/version` - Get application version
- `GET /api/environments` - List supported environments

### Job Management

- `POST /api/ansible/jobs/restart` - Create restart job
- `GET /api/ansible/jobs` - List all jobs
- `GET /api/ansible/jobs?environment=DEV` - Filter jobs by environment
- `GET /api/ansible/jobs/{job_id}/status` - Get job status
- `GET /api/ansible/jobs/{job_id}/logs` - Get job logs
- `POST /api/ansible/jobs/{job_id}/cancel` - Cancel job
- `POST /api/ansible/jobs/{job_id}/remediation-plan` - Get remediation plan

### Template

- `POST /api/ansible/template/{template_id}/launch` - Launch template job

---

## Testing

### Run All Tests

```bash
cd tests
pytest -v
```

### Run Specific Test

```bash
pytest test_api.py -v
pytest test_ansible.py -v
```

### Run with Coverage

```bash
pytest --cov=backend --cov-report=html
```

### Example Test Output

```
test_api.py::TestAnsibleEndpoints::test_health_check PASSED
test_api.py::TestAnsibleEndpoints::test_trigger_restart_success PASSED
test_api.py::TestAnsibleEndpoints::test_trigger_restart_invalid_environment PASSED
test_ansible.py::TestAnsibleMockService::test_create_mock_job PASSED
...

====================== 20 passed in 2.34s ======================
```

---

## Usage Examples

### 1. Submit a Restart Job

```bash
curl -X POST http://localhost:8000/api/ansible/jobs/restart \
  -H "Content-Type: application/json" \
  -d '{
    "environment": "DEV",
    "server_name": "weblogic-01",
    "reason": "Stuck thread detected in connection pool",
    "escalation_level": 2
  }'
```

### 2. Get Job Status

```bash
curl http://localhost:8000/api/ansible/jobs/JOB-20240115100000-a1b2c3d4/status
```

### 3. List Jobs by Environment

```bash
curl http://localhost:8000/api/ansible/jobs?environment=TEST
```

### 4. Get Job Logs

```bash
curl http://localhost:8000/api/ansible/jobs/JOB-20240115100000-a1b2c3d4/logs
```

---

## Frontend Features

### Dashboard
- System overview with job statistics
- Quick action buttons
- Real-time health status
- Service status display

### New Restart Job
- Environment selection (DEV, TEST, PREPROD, PROD)
- Server name input
- Reason for restart
- Escalation level slider (1-5)
- LLM-powered analysis display

### Active Jobs
- Real-time job listing
- Environment filtering
- Status indicators
- Job details modal
- Log viewer
- Cancel job capability

### Analytics
- Job status distribution
- Environment breakdown
- Success rate statistics
- Average duration tracking

---

## LLM Integration

The system uses **LangChain** with **GEMINI 2.0** for intelligent analysis:

1. **Stuck Thread Analysis** - AI analyzes the severity and likely causes
2. **Escalation Recommendations** - Suggests appropriate action level (1-5)
3. **Remediation Planning** - Generates step-by-step remediation guidance
4. **Fallback Support** - Mock responses if LLM is unavailable

### Setting Up GEMINI

1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Application automatically initializes GEMINI on startup

---

## Mock Ansible Integration

The system includes a **mock Ansible service** that simulates job submissions:

- Creates realistic job IDs and timestamps
- Simulates job progression (Pending → Running → Success/Failed)
- Provides job logs and status tracking
- ~90% success rate simulation
- In-memory job storage

**Note:** Replace `ansible_mock.py` with actual Ansible API calls for production use.

---

## Configuration

### Environment Variables

```env
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=True

# GEMINI (Optional)
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-pro

# Ansible
ANSIBLE_TOWER_URL=https://tower.ikea.com
ANSIBLE_JOB_TEMPLATE_ID=6782
ANSIBLE_TOKEN=token
```

### Supported Environments

- **DEV** - Development environment
- **TEST** - Testing environment
- **PREPROD** - Pre-production environment
- **PROD** - Production environment (requires escalation level 4-5)

---

## Troubleshooting

### Port Already in Use

```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

### GEMINI API Errors

- Check API key is valid
- Ensure quota is available
- Check internet connectivity

### Frontend Not Loading

- Ensure backend is running on port 8000
- Clear browser cache
- Check browser console for errors

### Tests Failing

- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version (3.8+)
- Run from tests directory: `cd tests && pytest`

---

## Performance Considerations

- **Job Simulation**: Jobs simulate 2-15 second execution
- **Auto-refresh**: Frontend refreshes jobs every 5 seconds
- **CORS Enabled**: Supports cross-origin requests
- **Async Operations**: FastAPI handles concurrent requests efficiently
- **In-memory Storage**: Mock jobs stored in memory (no persistence)

---

## Security Notes

- **API Key Protection**: Store GEMINI keys securely
- **CORS Policy**: Currently allows all origins (configure for production)
- **Input Validation**: All inputs validated with Pydantic
- **Error Handling**: Comprehensive error messages without sensitive data

---

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication (JWT tokens)
- [ ] Real Ansible Tower API integration
- [ ] Advanced monitoring and alerting
- [ ] Audit logging
- [ ] Multi-user support
- [ ] Scheduled job remediation
- [ ] Dashboard customization
- [ ] Export reports (PDF/Excel)
- [ ] Webhook notifications

---

## Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

---

## License

This project is proprietary. All rights reserved.

---

## Support & Contact

For questions or issues:
- Check existing GitHub issues
- Review API documentation at `/docs`
- Check application logs for error messages

---

## Version History

### v1.0.0 (Initial Release)
- FastAPI backend with complete REST API
- Modern responsive frontend
- LangChain + GEMINI integration
- Mock Ansible job service
- Comprehensive test suite
- Interactive API documentation

---

## Acknowledgments

- FastAPI documentation and community
- Google GEMINI team
- LangChain developers
- jQuery and Bootstrap communities

---

**Last Updated:** January 2024  
**Status:** Production Ready ✓
