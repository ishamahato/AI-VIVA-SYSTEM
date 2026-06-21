"""FastAPI application entry point for the AI Viva System."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine
from . import models  # noqa: F401  (ensures models are registered before create_all)
from .routes import auth, questions, viva, evaluation, results, dashboard


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables if they don't exist (handy for dev; in prod use sql/schema.sql)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="AI Viva System API", version="1.0.0", lifespan=lifespan)

# CORS so the Vite frontend (http://localhost:5173) can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "service": "ai-viva-system"}


@app.get("/api/health", tags=["health"])
def health():
    return {"status": "healthy"}


# All feature routers live under /api
API_PREFIX = "/api"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(questions.router, prefix=API_PREFIX)
app.include_router(viva.router, prefix=API_PREFIX)
app.include_router(evaluation.router, prefix=API_PREFIX)
app.include_router(results.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
