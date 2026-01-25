"""
FastAPI ana uygulama dosyası.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import Database
from app.routes import samples


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlatma ve kapatma işlemleri."""
    # Başlatma
    await Database.connect()
    yield
    # Kapatma
    await Database.disconnect()


# FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da değiştirilmeli
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(samples.router, prefix=f"/api/{settings.API_VERSION}", tags=["Samples"])


@app.get("/", tags=["Health"])
async def root():
    """Ana endpoint."""
    return {
        "message": "Mikroplastik Takip Sistemi API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Sistem sağlık kontrolü."""
    return {
        "status": "healthy",
        "database": "connected" if Database.db is not None else "disconnected"
    }
