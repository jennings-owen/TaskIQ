from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv
import time

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

# Dev run:
#   cd backend
#   python -m uvicorn main:app --reload --reload-include "*.env"