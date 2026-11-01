# LocalPilot

LocalPilot is a local-first FastAPI application for local AI workflows with a governed agent engine, approval workflow, and React dashboard.

## Phase 1 Features
- FastAPI application structure
- Configuration management (pydantic-settings)
- SQLite database with SQLAlchemy (async)
- Logging with Loguru
- Ollama connectivity check
- Health endpoint
- Basic tests

## Phase 2 Features
- Governed AI agent engine with tool execution
- Task planner and tool registry with explicit allowlist
- Permission manager with approval workflow
- Persistent tasks, agent responses, execution logs, and approvals
- REST API for tasks and approvals
- Ollama inference via /api/chat with qwen2.5-coder:7b-fdm
- Workspace security guard for file operations
- No unrestricted shell/Python execution

## Phase 3 Features
- React + Vite dashboard
- Overview, AI Assistant, Tasks, Approvals, Activity Logs, Settings pages
- Dark/light theme support
- API integration with FastAPI backend
- Pending approvals management
- Real-time system status

## Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama installed locally (with qwen2.5-coder:7b-fdm)

## Installation

### Backend
1. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Copy environment
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

### Frontend
```bash
cd frontend
npm install
```

## Startup

### Backend (port 8001 for development)
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

### Frontend (port 5173)
```bash
cd frontend
npm run dev
```

## API
- GET /api/v1/health - Health check with Ollama status
- POST /api/v1/tasks - Submit task
- GET /api/v1/tasks - List tasks
- GET /api/v1/tasks/{id} - Task details
- GET /api/v1/approvals - List approvals
- POST /api/v1/approvals - Create approval request
- POST /api/v1/approvals/{id}/respond - Approve/reject

## Tests
```bash
pytest -v
```

## Security
- Application bound to 127.0.0.1 only
- No unrestricted shell or Python execution
- Explicit tool allowlist
- Approval required for sensitive actions
- Workspace-scoped file access
- No credentials in logs or frontend
