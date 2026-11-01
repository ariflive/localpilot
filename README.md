# LocalPilot

LocalPilot is a local-first FastAPI application for local AI workflows.

## Phase 1 Features
- FastAPI application structure
- Configuration management
- SQLite database with SQLAlchemy (async)
- Logging with Loguru
- Ollama connectivity check
- Health endpoint
- Basic tests

## Setup
1. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
source .venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Copy environment
```bash
copy .env.example .env
```
4. Run the app
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

## API
- GET /health - Health check with Ollama status

## Tests
```bash
pytest -v
```
