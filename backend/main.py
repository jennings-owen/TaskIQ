from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
import time
import uvicorn

# Load .env with override so stale env vars from prior shell sessions don't persist
load_dotenv(find_dotenv(), override=True)

app = FastAPI()

def _build_origins():
    # Filter out None values to avoid CORS warning
    base_origins = [
        os.getenv("FRONT_END_URL")
    ]
    return [o for o in base_origins if o]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_build_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/status")
async def get_status():
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": "1.0.0",
        "timestamp": time.time()
    }

# Dev run options (PowerShell):
#   cd backend
#   $env:BACKEND_PORT=8010      # optional override (defaults to 8000)
#   python backend/main.py      # uses BACKEND_PORT if set
#   # OR directly with uvicorn (requires env already set):
#   uvicorn main:app --reload --reload-include "*.env" --port $env:BACKEND_PORT

if __name__ == "__main__":
    # Resolve port from environment with safe fallback
    raw_port = os.getenv("BACKEND_PORT", "8000")
    try:
        port = int(raw_port)
    except ValueError:
        raise ValueError(f"Invalid BACKEND_PORT '{raw_port}' (must be an integer).")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)