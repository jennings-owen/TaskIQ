from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration for React frontend
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Agile TaskIQ API is running."}


# Import and include routers
from .tasks import router as tasks_router
from .ai import router as ai_router

app.include_router(tasks_router)
app.include_router(ai_router)

# Ensure database tables are created (safe when using an existing DB)
from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)
