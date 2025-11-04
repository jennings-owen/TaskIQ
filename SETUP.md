# Project Development Setup Guide

This guide walks you through setting up both the backend (FastAPI) and frontend (React) development environments, installing dependencies, configuring environment variables, and running everything locally.

---

## 1. Prerequisites

Install the following before proceeding:

| Tool | Recommended Version | Check Command |
|------|---------------------|---------------|
| Python | 3.11+ (3.11.9 preferred) | `python --version` |
| Node.js | 18+ LTS | `node --version` |
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

Run the backend (uses uvicorn):
```powershell
uvicorn main:app --reload --port ${env:BACKEND_PORT}
```
If `BACKEND_PORT` isn't set, fallback:
```powershell
uvicorn main:app --reload --port 8000
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

## 6. Running Both Concurrently

Option A: Two terminals (recommended during development)
1. Terminal A → backend: activate venv, run uvicorn.
2. Terminal B → frontend: run `npm start`.

Option B: Use PowerShell background job (optional):
```powershell
Start-Job -ScriptBlock { Set-Location backend; ./.venv/Scripts/Activate.ps1; uvicorn main:app --reload --port 8000 }
Set-Location frontend
npm start
```

Option C: Create a simple root `dev.ps1` script (future enhancement) to orchestrate both.

Already implemented: see Section 9 for usage.

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

## 9. One-Command Dev Start (PowerShell & Bash)

To streamline starting both backend and frontend, this repo includes helper scripts at the project root:

### PowerShell (Recommended on Windows)

Script: `dev.ps1`

Features:
- Creates/activates `backend/.venv` if missing
- Installs Python deps if `uvicorn` absent (uses `requirements.txt`)
- Loads `backend/.env` automatically
- Starts backend (`uvicorn main:app --reload --port <port>`) then frontend (`npm start`)
- Graceful shutdown of backend when you exit React or press Ctrl+C

Usage (from repo root):
```powershell
./dev.ps1               # start on default port 8000
./dev.ps1 -BackendPort 8081       # custom backend port
./dev.ps1 -ReinstallPython        # force re-install Python deps
./dev.ps1 -Quiet                  # minimal logging
```

Environment precedence:
- If `backend/.env` contains `BACKEND_PORT`, it overrides `-BackendPort`.
- Sets default `FRONT_END_URL` to `http://localhost:3000` if not present.
- Sets `REACT_APP_API_BASE_URL` for the frontend if missing.

Verification endpoints after start:
```text
Backend:  http://localhost:<PORT>/status
Frontend: http://localhost:3000
```

Requirements:
- Run inside Git Bash or WSL (not plain Windows PowerShell)
- Creates `backend/.venv`, installs deps, loads `.env`, starts both services

If you see `/bin/bash not found`, install Git for Windows and use the bundled Git Bash or enable WSL.

### Choosing a Script
- Use `dev.ps1` for native Windows development.

---

## 10. Quick Start Summary

Backend:
```powershell
cd backend
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend (new terminal):
```powershell
cd frontend
npm install
npm start
```

---