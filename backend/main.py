from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv

app = FastAPI()
load_dotenv(find_dotenv())

origins = [
    "http://localhost:3000",
    os.getenv("FRONT_END_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all standard HTTP methods
    allow_headers=["*"],  # Allows all standard HTTP headers
)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/status")
async def get_status():
    return {
        "status": "healthy",
        "message": "API is running successfully",
        "version": "1.0.0"
    }

# To run:
# cd backend
# uvicorn main:app --reload