# Project Development Setup Guide

This guide walks you through setting up both the backend (FastAPI) and frontend (React) development environments, installing dependencies, configuring environment variables, and running everything locally.

## Quick Start with Docker (Recommended)

The fastest way to get started is using Docker:

```powershell
# Windows PowerShell
.\docker-start.ps1

# Linux/macOS
./docker-start.sh
```

This starts both frontend and backend in containers. See [DOCKER_README.md](DOCKER_README.md) for full Docker documentation.

---

## Manual Setup (Alternative)

If you prefer to run services directly on your machine without Docker, follow the instructions below.

---

## 1. Prerequisites

Install the following before proceeding:

| Tool | Recommended Version | Check Command |
|------|---------------------|---------------|
| Python | 3.11+ (3.11.9 preferred) | `python --version` |
| Node.js | 22.19.0+ | `node --version` |
| npm | Comes with Node.js | `npm --version` |

---

## 2. Clone the Repository

```powershell
git clone <REPO_URL>
cd 220372-AG-AISOFTDEV-Team-4-SynapseSquad
```

If already cloned, pull latest:
```powershell
git pull origin master
```

---

## 3. Environment Variables

The list and format of required environment variables are defined in `ENV_FORMAT.md`. Create a `.env` file based on that format.

If you add new variables, also update `ENV_FORMAT.md` so the team has a single source of truth.

Frontend optional environment variables (if you later consume the API from React):
Create `frontend/.env`:
```env
REACT_APP_API_BASE_URL=http://localhost:8000
```
Note: CRA (Create React App) only exposes variables prefixed with `REACT_APP_` at build time.

---

## 4. Backend Setup (FastAPI)

Move into the backend directory:
```powershell
cd backend
```

Create and activate a virtual environment (Windows PowerShell):
```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

Install dependencies:
```powershell
pip install -r ../requirements.txt
```

(If `requirements.txt` lives at root, the above relative path is correct.)

Run the backend (via Python entrypoint that internally starts uvicorn and reads `BACKEND_PORT` with fallback 8000):
```powershell
# Optional: override default port
$env:BACKEND_PORT=8010
python .\main.py
```

Test in browser or curl:
```powershell
curl http://localhost:8000/status
```

Expected JSON:
```json
{"status":"healthy","message":"API is running successfully","version":"1.0.0"}
```

Leave this terminal running.

---

## 5. Frontend Setup (React)

Open a new terminal (keep backend running) and navigate:
```powershell
cd frontend
```

Install dependencies:
```powershell
npm install
```

Run the development server:
```powershell
npm start
```

Default URL: http://localhost:3000

If consuming the API, ensure CORS is configured (already allows `http://localhost:3000`).

---

## 7. Directory Overview

| Path | Purpose |
|------|---------|
| `backend/` | FastAPI application (`main.py`). |
| `frontend/` | React application (Create React App). |
| `requirements.txt` | Python dependency manifest. |
| `ENV_FORMAT.md` | Canonical environment variable definitions (update as needed). |
| `SETUP.md` | This setup guide. |
| `README.md` | Project description. |

---

## 8. Common Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| CORS errors | Missing/incorrect `FRONT_END_URL` | Set in `.env` and restart backend. |
| React can't reach API | Wrong base URL | Confirm `REACT_APP_API_BASE_URL` matches backend port. |
| Uvicorn not found | venv not activated / install failed | Re-run activation; reinstall requirements. |
| Port already in use | Another process on 8000/3000 | Change port (`--port 8001`) or stop conflicting process. |
| Env vars not loading | `.env` misplaced | Ensure file is inside `backend/` and named `.env`. |

Check active environment variables:
```powershell
Get-Content .env
```

---

## 10. Quick Start Summary

Backend:
```powershell
cd backend
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r ../requirements.txt
python .\main.py   # uses BACKEND_PORT if set, else 8000
```

Frontend (new terminal):
```powershell
cd frontend
npm install
npm start
```

---